import os
import json
import time
import uuid
import random
from flask import Flask, request, jsonify
import threading
from collections import defaultdict, deque

try:
    from iqoptionapi.stable_api import IQ_Option
    print("✅ IQ Option API importada correctamente")
except ImportError as e:
    print(f"❌ Error importando IQ Option API: {e}")
    exit(1)

class IQClient:
    def __init__(self):
        self.api = None
        self.connected = False
        self.balance_type = "PRACTICE"
        self.current_balance = 0
        self.email = None
        self.password = None
        
        # Cache para velas REALES
        self.candles_cache = defaultdict(lambda: deque(maxlen=500))
        self.real_candles_available = False
        
        # Configuración
        self.symbols_to_watch = ['EURUSD-OTC', 'GBPUSD-OTC', 'USDJPY-OTC', 'EURJPY-OTC']
        self.candles_updater_running = False
        
        print("🚀 IQ Client inicializado - Versión Mejorada")

    def connect(self, email=None, password=None, balance_type=None):
        """Conectar a IQ Option con credenciales REALES"""
        try:
            # Usar credenciales del dashboard
            if email and password:
                self.email = email
                self.password = password
            if balance_type:
                self.balance_type = balance_type.upper()
                
            if not self.email or not self.password:
                return {"success": False, "error": "Credenciales requeridas"}
            
            print(f"🔌 Conectando a IQ Option como: {self.email}")
            print(f"💰 Tipo de cuenta: {self.balance_type}")
            
            # Crear conexión
            self.api = IQ_Option(self.email, self.password)
            
            # Intentar login con timeout
            print("⏳ Realizando login...")
            check, reason = self.api.connect()
            
            if check:
                print("✅ Login exitoso a IQ Option")
                
                # Cambiar tipo de balance
                account_type = "REAL" if self.balance_type == "REAL" else "PRACTICE"
                result = self.api.change_balance(account_type)
                print(f"✅ Balance cambiado a: {account_type} - Resultado: {result}")
                
                # Obtener balance real
                balance = self.api.get_balance()
                self.current_balance = balance
                print(f"💰 Balance obtenido: ${balance}")
                
                # Verificar conexión real
                self.verify_real_connection()
                
                self.connected = True
                self.start_real_time_updates()
                
                return {
                    "success": True, 
                    "balance": balance,
                    "balance_type": self.balance_type,
                    "message": f"Conectado exitosamente a IQ Option - Balance: ${balance}"
                }
            else:
                error_msg = f"Error de login: {reason}"
                print(f"❌ {error_msg}")
                return {"success": False, "error": error_msg}
                
        except Exception as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(f"💥 {error_msg}")
            return {"success": False, "error": error_msg}

    def verify_real_connection(self):
        """Verificar que tenemos datos reales, no fake"""
        try:
            print("🔍 Verificando conexión real...")
            
            # Intentar obtener velas reales
            test_symbol = self.symbols_to_watch[0]
            candles = self.api.get_candles(test_symbol, 300, 10, time.time())
            
            if candles and len(candles) > 0:
                self.real_candles_available = True
                print(f"✅ Conexión REAL verificada - {len(candles)} velas obtenidas")
                
                # Mostrar información de velas reales
                latest_candle = candles[-1]
                print(f"📊 Última vela real: Time: {latest_candle['from']}, Close: {latest_candle['close']}")
            else:
                print("⚠️  No se pudieron obtener velas reales, usando datos de respaldo")
                self.real_candles_available = False
                
        except Exception as e:
            print(f"❌ Error verificando conexión real: {e}")
            self.real_candles_available = False

    def start_real_time_updates(self):
        """Iniciar actualización en tiempo real"""
        if self.candles_updater_running:
            return
            
        self.candles_updater_running = True
        
        def real_time_updater():
            update_count = 0
            while self.candles_updater_running and self.connected:
                try:
                    for symbol in self.symbols_to_watch:
                        self.update_real_candles(symbol)
                    
                    update_count += 1
                    if update_count % 10 == 0:  # Log cada 10 actualizaciones
                        print(f"🔄 Actualización #{update_count} completada")
                    
                    time.sleep(3)  # Actualizar cada 3 segundos
                    
                except Exception as e:
                    print(f"❌ Error en actualizador: {e}")
                    time.sleep(5)
        
        threading.Thread(target=real_time_updater, daemon=True).start()
        print("🔄 Iniciado actualizador de velas en tiempo real")

    def update_real_candles(self, symbol, timeframe="M5", limit=100):
        """Actualizar velas REALES desde IQ Option"""
        if not self.connected or not self.api:
            return
            
        try:
            # Mapear timeframe
            tf_map = {"M1": 1, "M5": 5, "M15": 15, "M30": 30, "H1": 60}
            minutes = tf_map.get(timeframe, 5)
            
            # Obtener velas REALES
            candles = self.api.get_candles(symbol, minutes * 60, limit, time.time())
            
            if candles and len(candles) > 0:
                formatted_candles = []
                for candle in candles:
                    formatted_candle = {
                        "time": int(candle["from"] * 1000),
                        "open": candle["open"],
                        "high": candle["max"],
                        "low": candle["min"],
                        "close": candle["close"],
                        "volume": candle.get("volume", 0),
                        "real": True  # Marcar como datos reales
                    }
                    formatted_candles.append(formatted_candle)
                
                # Actualizar cache
                self.candles_cache[symbol].extend(formatted_candles)
                
                # Log primera actualización
                if len(formatted_candles) > 0 and not hasattr(self, f'first_update_{symbol}'):
                    setattr(self, f'first_update_{symbol}', True)
                    print(f"✅ Primeras velas REALES obtenidas para {symbol}: {len(formatted_candles)} velas")
                    
        except Exception as e:
            print(f"❌ Error actualizando velas reales para {symbol}: {e}")

    def get_candles(self, symbol, timeframe="M5", limit=200):
        """Obtener velas - PRIORIDAD a datos REALES"""
        try:
            # Intentar obtener datos REALES primero
            if symbol in self.candles_cache and len(self.candles_cache[symbol]) > 0:
                real_candles = list(self.candles_cache[symbol])[-limit:]
                print(f"📊 Devolviendo {len(real_candles)} velas REALES para {symbol}")
                return real_candles
            
            # Si no hay datos reales, usar demo PERO avisar
            print(f"⚠️  No hay datos REALES para {symbol}, usando datos demo")
            return self.generate_realistic_demo_candles(symbol, limit)
            
        except Exception as e:
            print(f"❌ Error obteniendo velas: {e}")
            return self.generate_realistic_demo_candles(symbol, limit)

    def generate_realistic_demo_candles(self, symbol, limit=200):
        """Generar velas demo realistas basadas en precios actuales"""
        print(f"🎭 Generando {limit} velas DEMO realistas para {symbol}")
        
        # Precios base realistas por símbolo
        base_prices = {
            'EURUSD-OTC': 1.08500,
            'GBPUSD-OTC': 1.26500, 
            'USDJPY-OTC': 148.500,
            'EURJPY-OTC': 157.800
        }
        
        base_price = base_prices.get(symbol, 1.08500)
        candles = []
        current_time = int(time.time() * 1000)
        
        # Crear velas con variación realista
        for i in range(limit):
            # Variación más realista para Forex
            variation = random.uniform(-0.002, 0.002)
            open_price = base_price + variation
            close_variation = random.uniform(-0.001, 0.001)
            close_price = open_price + close_variation
            
            # High y Low realistas
            high_price = max(open_price, close_price) + abs(random.uniform(0, 0.0008))
            low_price = min(open_price, close_price) - abs(random.uniform(0, 0.0008))
            
            candle = {
                "time": current_time - (limit - i - 1) * 5 * 60 * 1000,
                "open": round(open_price, 5),
                "high": round(high_price, 5),
                "low": round(low_price, 5),
                "close": round(close_price, 5),
                "volume": random.randint(500, 2000),
                "demo": True  # Marcar como demo
            }
            
            candles.append(candle)
            base_price = close_price  # Mantener continuidad
        
        return candles

    def get_real_balance(self):
        """Obtener balance REAL de IQ Option"""
        if not self.connected or not self.api:
            return {"error": "No conectado", "balance": 0, "demo": True}
        
        try:
            balance = self.api.get_balance()
            self.current_balance = balance
            
            return {
                "balance": balance,
                "balance_type": self.balance_type,
                "currency": "USD",
                "real": True
            }
        except Exception as e:
            print(f"❌ Error obteniendo balance real: {e}")
            return {"error": str(e), "balance": 0, "demo": True}

    def place_real_order(self, symbol, direction, amount, duration=1):
        """Enviar orden REAL a IQ Option"""
        if not self.connected or not self.api:
            return {"success": False, "error": "No conectado a IQ Option", "demo": True}
        
        try:
            print(f"📈 Enviando orden REAL: {direction} {symbol} ${amount}")
            
            action = "call" if direction.upper() == "CALL" else "put"
            order_id = self.api.buy(amount, symbol, action, duration)
            
            if order_id and isinstance(order_id, (int, str)) and str(order_id).isdigit():
                print(f"✅ Orden REAL ejecutada. ID: {order_id}")
                return {
                    "success": True,
                    "order_id": order_id,
                    "symbol": symbol,
                    "direction": direction,
                    "amount": amount,
                    "duration": duration,
                    "real": True,
                    "message": "Orden REAL ejecutada en IQ Option"
                }
            else:
                error_msg = f"Error en IQ Option: {order_id}"
                print(f"❌ {error_msg}")
                return {"success": False, "error": error_msg, "demo": True}
                
        except Exception as e:
            error_msg = f"Error ejecutando orden: {str(e)}"
            print(f"💥 {error_msg}")
            return {"success": False, "error": error_msg, "demo": True}

# Instancia global
iq_client = IQClient()

# Flask app
app = Flask(__name__)

@app.route('/api/iq/login', methods=['POST'])
def login():
    """Endpoint de login MEJORADO"""
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({"success": False, "error": "Datos JSON requeridos"}), 400
        
        print("📨 Login request recibido:")
        print(f"   Email: {data.get('email', 'No proporcionado')}")
        print(f"   Balance Type: {data.get('balance_type', 'No proporcionado')}")
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        balance_type = data.get('balance_type', 'PRACTICE')
        
        if not email or not password:
            return jsonify({"success": False, "error": "Email y password requeridos"}), 400
        
        # Realizar conexión
        result = iq_client.connect(email, password, balance_type)
        return jsonify(result)
        
    except Exception as e:
        error_msg = f"Error en login endpoint: {str(e)}"
        print(f"💥 {error_msg}")
        return jsonify({"success": False, "error": error_msg}), 500

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
        "real_data_available": iq_client.real_candles_available,
        "balance_type": iq_client.balance_type,
        "service": "IQ Client API"
    })

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 STC TRADING - IQ CLIENT MEJORADO")
    print("📍 Conectando con IQ Option API REAL")
    print("=" * 60)
    
    app.run(host="0.0.0.0", port=5002, debug=False, use_reloader=False)