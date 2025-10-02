import os
import time
import logging
from flask import Flask, request, jsonify
import threading
from collections import defaultdict, deque

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from iqoptionapi.stable_api import IQ_Option

app = Flask(__name__)

class FinalIQClient:
    def __init__(self):
        self.api = None
        self.connected = False
        self.balance_type = "PRACTICE"
        self.current_balance = 0
        self.email = None
        self.password = None
        
        # Cache para velas reales
        self.candles_cache = defaultdict(lambda: deque(maxlen=1000))
        self.symbols = ['EURUSD-OTC', 'GBPUSD-OTC', 'USDJPY-OTC', 'EURJPY-OTC']
        self.real_time_updater_running = False
        
        logger.info("🚀 Final IQ Client - 100% REAL")

    def connect(self, email, password, balance_type="PRACTICE"):
        """Conexión directa con las credenciales del dashboard"""
        logger.info(f"🎯 CONEXIÓN SOLICITADA desde dashboard")
        logger.info(f"📧 Email recibido: {email}")
        logger.info(f"💰 Balance type: {balance_type}")
        
        self.email = email
        self.password = password
        self.balance_type = balance_type.upper()

        try:
            # 1. Crear instancia API
            logger.info("1. Creando API IQ_Option...")
            self.api = IQ_Option(self.email, self.password)
            
            # 2. Conectar
            logger.info("2. Estableciendo conexión...")
            check, reason = self.api.connect()
            
            if not check:
                error_msg = f"Error conexión: {reason}"
                logger.error(f"❌ {error_msg}")
                return {"success": False, "error": error_msg}
            
            logger.info("✅ Conexión IQ Option establecida")
            
            # 3. Configurar balance
            logger.info(f"3. Configurando cuenta {self.balance_type}...")
            account_type = "REAL" if self.balance_type == "REAL" else "PRACTICE"
            self.api.change_balance(account_type)
            
            # 4. Obtener balance real
            balance = self.api.get_balance()
            self.current_balance = balance
            logger.info(f"💰 Balance real: ${balance}")
            
            # 5. Verificar datos
            if self.verify_real_data():
                self.connected = True
                self.start_real_time_updater()
                
                return {
                    "success": True,
                    "balance": balance,
                    "balance_type": self.balance_type,
                    "message": f"Conexión REAL exitosa - Balance: ${balance}",
                    "real_data": True
                }
            else:
                return {"success": False, "error": "No se pudieron verificar datos reales"}
                
        except Exception as e:
            error_msg = f"Error crítico: {str(e)}"
            logger.error(f"💥 {error_msg}")
            return {"success": False, "error": error_msg}

    def verify_real_data(self):
        """Verificar que obtenemos datos reales"""
        try:
            logger.info("🔍 Verificando datos reales...")
            candles = self.api.get_candles("EURUSD-OTC", 300, 3, time.time())
            
            if candles and len(candles) > 0:
                logger.info(f"✅ Datos reales verificados: {len(candles)} velas")
                for candle in candles:
                    logger.info(f"   📊 Vela: {candle['close']}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error verificando datos: {e}")
            return False

    def start_real_time_updater(self):
        """Iniciar actualización en tiempo real"""
        if self.real_time_updater_running:
            return
            
        self.real_time_updater_running = True
        
        def updater():
            logger.info("🔄 Iniciando actualizador REAL...")
            while self.connected:
                try:
                    for symbol in self.symbols:
                        self.update_candles(symbol)
                    time.sleep(2)  # Actualizar cada 2 segundos
                except Exception as e:
                    logger.error(f"Error en actualizador: {e}")
                    time.sleep(5)
        
        threading.Thread(target=updater, daemon=True).start()

    def update_candles(self, symbol):
        """Actualizar velas reales"""
        try:
            candles = self.api.get_candles(symbol, 300, 20, time.time())
            if candles:
                for candle in candles:
                    formatted = {
                        "time": int(candle["from"] * 1000),
                        "open": candle["open"],
                        "high": candle["max"],
                        "low": candle["min"],
                        "close": candle["close"],
                        "volume": candle.get("volume", 0),
                        "real": True
                    }
                    self.candles_cache[symbol].append(formatted)
        except Exception as e:
            logger.error(f"Error actualizando {symbol}: {e}")

    def get_candles(self, symbol, timeframe="M5", limit=200):
        """Obtener velas REALES"""
        if not self.connected:
            logger.error("❌ No conectado para obtener velas")
            return []
        
        try:
            # Usar cache o obtener directamente
            if symbol in self.candles_cache and len(self.candles_cache[symbol]) > 0:
                candles = list(self.candles_cache[symbol])[-limit:]
                logger.info(f"📊 Velas desde cache: {len(candles)} para {symbol}")
                return candles
            else:
                # Obtener directamente
                return self.get_direct_candles(symbol, limit)
        except Exception as e:
            logger.error(f"❌ Error obteniendo velas: {e}")
            return []

    def get_direct_candles(self, symbol, limit=200):
        """Obtener velas directamente"""
        try:
            candles = self.api.get_candles(symbol, 300, limit, time.time())
            if candles:
                formatted = []
                for candle in candles:
                    formatted.append({
                        "time": int(candle["from"] * 1000),
                        "open": candle["open"],
                        "high": candle["max"],
                        "low": candle["min"],
                        "close": candle["close"],
                        "volume": candle.get("volume", 0),
                        "real": True
                    })
                logger.info(f"✅ Velas directas: {len(formatted)} para {symbol}")
                return formatted
            return []
        except Exception as e:
            logger.error(f"❌ Error velas directas: {e}")
            return []

    def get_balance(self):
        """Obtener balance REAL"""
        if not self.connected:
            return {"error": "No conectado", "balance": 0}
        
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
            logger.error(f"❌ Error balance: {e}")
            return {"error": str(e), "balance": 0}

    def place_trade(self, symbol, direction, amount, duration=1):
        """Operación REAL"""
        if not self.connected:
            return {"success": False, "error": "No conectado"}
        
        try:
            logger.info(f"📈 Orden REAL: {direction} {symbol} ${amount}")
            action = "call" if direction.upper() == "CALL" else "put"
            order_id = self.api.buy(amount, symbol, action, duration)
            
            if order_id and str(order_id).isdigit():
                logger.info(f"✅ Orden REAL ejecutada: {order_id}")
                return {
                    "success": True,
                    "order_id": order_id,
                    "symbol": symbol,
                    "direction": direction,
                    "amount": amount,
                    "duration": duration,
                    "real": True
                }
            else:
                error_msg = f"Error IQ: {order_id}"
                logger.error(f"❌ {error_msg}")
                return {"success": False, "error": error_msg}
                
        except Exception as e:
            error_msg = f"Error orden: {str(e)}"
            logger.error(f"💥 {error_msg}")
            return {"success": False, "error": error_msg}

# Instancia global
iq_client = FinalIQClient()

@app.route('/api/iq/login', methods=['POST'])
def login():
    """Endpoint de login MEJORADO"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON data"}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        balance_type = data.get('balance_type', 'PRACTICE')
        
        logger.info(f"🔐 Login endpoint llamado con email: {email}")
        
        if not email or not password:
            return jsonify({"success": False, "error": "Email y password requeridos"}), 400
        
        result = iq_client.connect(email, password, balance_type)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"💥 Error en login endpoint: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/iq/balance', methods=['GET'])
def get_balance():
    result = iq_client.get_balance()
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
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data"}), 400
    
    symbol = data.get('symbol', 'EURUSD-OTC')
    direction = data.get('direction', 'CALL')
    amount = float(data.get('amount', 1))
    duration = int(data.get('duration', 1))
    
    result = iq_client.place_trade(symbol, direction, amount, duration)
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "connected": iq_client.connected,
        "service": "IQ Client FINAL - 100% REAL"
    })

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 STC TRADING - IQ CLIENT FINAL")
    print("📍 100% CONEXIÓN REAL - SIN FALLBACKS")
    print("=" * 60)
    
    app.run(host="0.0.0.0", port=5002, debug=False, use_reloader=False)