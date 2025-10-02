import os
import json
import time
import uuid
import random
from flask import Flask, Blueprint, request, jsonify
import threading
from collections import defaultdict, deque

# Importar candles_store
from candles_store import store_batch, read_last

try:
    from iqoptionapi.stable_api import IQ_Option
    print("✅ IQ Option API importada correctamente")
except ImportError as e:
    print(f"❌ Error importando IQ Option API: {e}")
    print("Instalando iqoptionapi...")
    os.system("pip install iqoptionapi")
    from iqoptionapi.stable_api import IQ_Option

class IQClient:
    def __init__(self):
        self.api = None
        self.connected = False
        self.balance_type = "PRACTICE"
        self.current_balance = 10000.0
        self.email = None
        self.password = None
        
        # Cache mejorado para velas
        self.candles_cache = defaultdict(lambda: deque(maxlen=2000))
        self.last_candle_time = defaultdict(int)
        
        # Sistema de actualización automática
        self.candles_updater_running = False
        self.symbols_to_watch = ['EURUSD-OTC', 'GBPUSD-OTC', 'USDJPY-OTC', 'EURJPY-OTC']
        
        # Cola para órdenes
        self.orders_queue = deque()
        self.processing_orders = False
        
        self.load_config()
        print("🚀 IQ Client inicializado")

    def load_config(self):
        """Cargar configuración desde variables de entorno"""
        self.email = os.getenv('IQ_EMAIL', '')
        self.password = os.getenv('IQ_PASSWORD', '')
        self.balance_type = os.getenv('IQ_BALANCE_TYPE', 'PRACTICE')
        
        if not self.email or not self.password:
            print("⚠️  Credenciales no configuradas en .env")

    def connect(self, email=None, password=None, balance_type=None):
        """Conectar a IQ Option con credenciales reales"""
        try:
            if email:
                self.email = email
            if password:
                self.password = password
            if balance_type:
                self.balance_type = balance_type.upper()
                
            if not self.email or not self.password:
                return {"success": False, "error": "Credenciales requeridas"}
            
            print(f"🔌 Conectando a IQ Option como {self.email}...")
            
            # Crear conexión
            self.api = IQ_Option(self.email, self.password)
            
            # Intentar login
            check, reason = self.api.connect()
            
            if check:
                print("✅ Conexión exitosa a IQ Option")
                
                # Cambiar tipo de balance
                if self.balance_type == "REAL":
                    self.api.change_balance("REAL")
                    print("💰 Cambiado a cuenta REAL")
                else:
                    self.api.change_balance("PRACTICE")
                    print("🎯 Cambiado a cuenta PRACTICE")
                
                # Obtener balance real
                balance = self.api.get_balance()
                self.current_balance = balance
                
                self.connected = True
                
                # INICIAR ACTUALIZACIÓN AUTOMÁTICA DE VELAS
                self.start_candles_updater()
                self.start_background_tasks()
                
                return {
                    "success": True, 
                    "balance": balance,
                    "balance_type": self.balance_type,
                    "message": "Conectado exitosamente"
                }
            else:
                print(f"❌ Error de conexión: {reason}")
                return {"success": False, "error": f"Error de login: {reason}"}
                
        except Exception as e:
            print(f"💥 Error conectando: {str(e)}")
            return {"success": False, "error": str(e)}

    def start_candles_updater(self):
        """Iniciar actualización automática de velas cada 2 segundos"""
        if self.candles_updater_running:
            return
            
        self.candles_updater_running = True
        
        def updater():
            while self.candles_updater_running and self.connected:
                try:
                    for symbol in self.symbols_to_watch:
                        self.update_candles_for_symbol(symbol)
                    time.sleep(2)  # Actualizar cada 2 segundos
                except Exception as e:
                    print(f"Error en actualizador de velas: {e}")
                    time.sleep(5)
        
        threading.Thread(target=updater, daemon=True).start()
        print("🔄 Iniciado actualizador automático de velas")

    def update_candles_for_symbol(self, symbol, timeframe="M5", limit=50):
        """Actualizar velas para un símbolo específico"""
        if not self.connected:
            return
            
        try:
            # Obtener velas actualizadas
            tf_map = {"M1": 1, "M5": 5, "M15": 15, "M30": 30, "H1": 60}
            minutes = tf_map.get(timeframe, 5)
            
            candles = self.api.get_candles(symbol, minutes * 60, limit, time.time())
            
            if candles and len(candles) > 0:
                formatted_candles = []
                for candle in candles:
                    candle_time = int(candle["from"] * 1000)
                    
                    # Solo procesar si es una vela nueva
                    if candle_time > self.last_candle_time[symbol]:
                        formatted_candle = {
                            "time": candle_time,
                            "open": candle["open"],
                            "high": candle["max"],
                            "low": candle["min"],
                            "close": candle["close"],
                            "volume": candle.get("volume", 0)
                        }
                        formatted_candles.append(formatted_candle)
                        self.last_candle_time[symbol] = candle_time
                
                # Actualizar cache
                if formatted_candles:
                    for candle in formatted_candles:
                        self.candles_cache[symbol].append(candle)
                    
                    # Guardar en CSV
                    store_batch(symbol, timeframe, formatted_candles)
                    
                    if len(formatted_candles) > 1:
                        print(f"📊 Actualizadas {len(formatted_candles)} velas para {symbol}")
                
        except Exception as e:
            print(f"Error actualizando velas para {symbol}: {e}")

    def get_candles(self, symbol, timeframe="M5", limit=200):
        """Obtener velas del cache"""
        try:
            # Si hay velas en cache, devolverlas
            if symbol in self.candles_cache and len(self.candles_cache[symbol]) > 0:
                candles = list(self.candles_cache[symbol])[-limit:]
                print(f"📈 Devolviendo {len(candles)} velas desde cache para {symbol}")
                return candles
            else:
                # Si no hay cache, obtener del API
                print(f"🔄 Cache vacío, obteniendo velas iniciales para {symbol}")
                return self.get_initial_candles(symbol, timeframe, limit)
                
        except Exception as e:
            print(f"Error obteniendo velas: {e}")
            return self.generate_demo_candles(symbol, limit)

    def get_initial_candles(self, symbol, timeframe="M5", limit=200):
        """Obtener velas iniciales del API"""
        if not self.connected:
            return self.generate_demo_candles(symbol, limit)
            
        try:
            tf_map = {"M1": 1, "M5": 5, "M15": 15, "M30": 30, "H1": 60}
            minutes = tf_map.get(timeframe, 5)
            
            candles = self.api.get_candles(symbol, minutes * 60, limit, time.time())
            
            if candles:
                formatted_candles = []
                for candle in candles:
                    candle_time = int(candle["from"] * 1000)
                    formatted_candle = {
                        "time": candle_time,
                        "open": candle["open"],
                        "high": candle["max"],
                        "low": candle["min"],
                        "close": candle["close"],
                        "volume": candle.get("volume", 0)
                    }
                    formatted_candles.append(formatted_candle)
                    self.last_candle_time[symbol] = candle_time
                
                # Ordenar y guardar en cache
                formatted_candles.sort(key=lambda x: x["time"])
                self.candles_cache[symbol].extend(formatted_candles)
                
                # Guardar en CSV
                store_batch(symbol, timeframe, formatted_candles)
                
                print(f"📊 Obtenidas {len(formatted_candles)} velas iniciales de {symbol}")
                return formatted_candles
            else:
                return self.generate_demo_candles(symbol, limit)
                
        except Exception as e:
            print(f"Error obteniendo velas iniciales: {e}")
            return self.generate_demo_candles(symbol, limit)

    def generate_demo_candles(self, symbol, limit=200):
        """Generar velas demo para desarrollo"""
        print(f"🎭 Generando {limit} velas demo para {symbol}")
        
        candles = []
        base_price = 1.08500 if 'EUR' in symbol else 1.25000 if 'GBP' in symbol else 150.00
        current_time = int(time.time() * 1000)
        
        for i in range(limit):
            variation = random.uniform(-0.001, 0.001)
            open_price = base_price + variation
            close_price = open_price + random.uniform(-0.0005, 0.0005)
            high_price = max(open_price, close_price) + random.uniform(0, 0.0003)
            low_price = min(open_price, close_price) - random.uniform(0, 0.0003)
            
            candle = {
                "time": current_time - (limit - i - 1) * 5 * 60 * 1000,
                "open": round(open_price, 5),
                "high": round(high_price, 5),
                "low": round(low_price, 5),
                "close": round(close_price, 5),
                "volume": random.randint(100, 1000)
            }
            
            candles.append(candle)
            base_price = close_price
        
        return candles

    def start_background_tasks(self):
        """Iniciar tareas en segundo plano"""
        if not self.processing_orders:
            self.processing_orders = True
            threading.Thread(target=self.process_orders_queue, daemon=True).start()
            print("🔄 Iniciado procesador de órdenes")

    def process_orders_queue(self):
        """Procesar cola de órdenes"""
        while self.processing_orders:
            try:
                if self.orders_queue and self.connected:
                    order_data = self.orders_queue.popleft()
                    result = self.place_real_order(**order_data)
                    print(f"Orden procesada: {result}")
                
                time.sleep(0.1)
            except Exception as e:
                print(f"Error procesando órdenes: {e}")
                time.sleep(1)

    def get_real_balance(self):
        """Obtener balance real actual"""
        if not self.connected:
            return {"error": "No conectado", "balance": 0}
        
        try:
            balance = self.api.get_balance()
            self.current_balance = balance
            return {
                "balance": balance,
                "balance_type": self.balance_type,
                "currency": "USD"
            }
        except Exception as e:
            print(f"Error obteniendo balance: {e}")
            return {"error": str(e), "balance": 0}

    def place_real_order(self, symbol, direction, amount, duration=1):
        """Enviar orden real a IQ Option"""
        if not self.connected:
            return {"success": False, "error": "No conectado a IQ Option"}
        
        try:
            print(f"📈 Enviando orden: {direction} {symbol} ${amount} por {duration}min")
            
            action = "call" if direction.upper() == "CALL" else "put"
            order_id = self.api.buy(amount, symbol, action, duration)
            
            if order_id and str(order_id).isdigit():
                print(f"✅ Orden enviada. ID: {order_id}")
                return {
                    "success": True,
                    "order_id": order_id,
                    "symbol": symbol,
                    "direction": direction,
                    "amount": amount,
                    "duration": duration,
                    "message": "Orden ejecutada"
                }
            else:
                print(f"❌ Error enviando orden: {order_id}")
                return {"success": False, "error": f"Error: {order_id}"}
                
        except Exception as e:
            print(f"💥 Error ejecutando orden: {str(e)}")
            return {"success": False, "error": str(e)}

# Instancia global
iq_client = IQClient()

# Flask app
app = Flask(__name__)

@app.route('/api/iq/login', methods=['POST'])
def login():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "JSON requerido"}), 400
    
    email = data.get('email')
    password = data.get('password')
    balance_type = data.get('balance_type', 'PRACTICE')
    
    result = iq_client.connect(email, password, balance_type)
    return jsonify(result)

@app.route('/api/iq/balance', methods=['GET'])
def get_balance():
    result = iq_client.get_real_balance()
    return jsonify(result)

@app.route('/api/iq/candles', methods=['GET'])
def get_candles():
    symbol = request.args.get('symbol', 'EURUSD-OTC')
    timeframe = request.args.get('timeframe', 'M5')
    limit = int(request.args.get('limit', 200))
    
    candles = iq_client.get_candles(symbol, timeframe, limit)
    return jsonify(candles)

@app.route('/api/iq/trade', methods=['POST'])
def place_trade():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "JSON requerido"}), 400
    
    symbol = data.get('symbol', 'EURUSD-OTC')
    direction = data.get('direction', 'CALL')
    amount = float(data.get('amount', 1))
    duration = int(data.get('duration', 1))
    
    result = iq_client.place_real_order(symbol, direction, amount, duration)
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "connected": iq_client.connected,
        "balance_type": iq_client.balance_type,
        "candles_updater": iq_client.candles_updater_running
    })

if __name__ == "__main__":
    print("🚀 Iniciando IQ Client con actualización automática de velas...")
    app.run(host="0.0.0.0", port=5002, debug=True, use_reloader=False)