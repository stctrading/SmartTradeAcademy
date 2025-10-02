#!/usr/bin/env python3
"""
iq_routes_no_redis.py - IQ API Backend sin Redis (puerto 5002)
- Cache en memoria para datos temporales
- Endpoints para velas, símbolos, balance, órdenes
- CORS habilitado para dashboard
"""

import os
import json
import time
import uuid
import random
import threading
from datetime import datetime, timedelta
from collections import defaultdict, deque
from flask import Flask, Blueprint, request, jsonify

try:
    from flask_cors import CORS
    USE_CORS = True
except ImportError:
    USE_CORS = False

# Cache global en memoria
class MemoryCache:
    def __init__(self):
        self.data = {}
        self.lists = defaultdict(deque)
        self.lock = threading.Lock()
        self.candles_cache = defaultdict(list)  # Cache específico para velas
        self.symbols_cache = []
        self.balance_cache = {"balance": 10000.0, "currency": "USD", "account_type": "PRACTICE"}
        self.orders_cache = []
        print(f"[MemoryCache] Inicializado - {datetime.now()}")
    
    def set(self, key, value):
        with self.lock:
            self.data[key] = value
    
    def get(self, key, default=None):
        with self.lock:
            return self.data.get(key, default)
    
    def lpush(self, key, value):
        with self.lock:
            self.lists[key].appendleft(value)
    
    def lpop(self, key):
        with self.lock:
            try:
                return self.lists[key].popleft()
            except IndexError:
                return None
    
    def set_candles(self, symbol, timeframe, candles):
        with self.lock:
            key = f"{symbol}_{timeframe}"
            self.candles_cache[key] = candles[-100:]  # Mantener últimas 100 velas
            print(f"[Cache] Velas actualizadas: {symbol} {timeframe} - {len(candles)} velas")
    
    def get_candles(self, symbol, timeframe):
        with self.lock:
            key = f"{symbol}_{timeframe}"
            return self.candles_cache.get(key, [])
    
    def set_symbols(self, symbols):
        with self.lock:
            self.symbols_cache = symbols
            print(f"[Cache] Símbolos actualizados: {len(symbols)} símbolos")
    
    def get_symbols(self):
        with self.lock:
            return self.symbols_cache.copy()
    
    def set_balance(self, balance_data):
        with self.lock:
            self.balance_cache.update(balance_data)
            print(f"[Cache] Balance actualizado: {balance_data}")
    
    def get_balance(self):
        with self.lock:
            return self.balance_cache.copy()

# Instancia global del cache
cache = MemoryCache()

app = Flask(__name__)

# Configurar CORS si está disponible
if USE_CORS:
    CORS(app, 
         resources={r"/api/*": {"origins": "*"}}, 
         allow_headers=["Content-Type", "Accept", "Authorization"],
         methods=["GET", "POST", "OPTIONS"])

# Blueprint para rutas IQ
bp = Blueprint("iq", __name__, url_prefix="/api/iq")

@bp.route("/health", methods=["GET"])
def health_check():
    """Endpoint de salud del servicio"""
    return jsonify({
        "status": "healthy",
        "service": "IQ Option API Backend",
        "timestamp": time.time(),
        "cache_stats": {
            "symbols_count": len(cache.get_symbols()),
            "candles_keys": len(cache.candles_cache),
            "balance": cache.get_balance()["balance"]
        }
    })

@bp.route("/login", methods=["GET", "POST"])
def iq_login():
    """Endpoint de login IQ Option"""
    if request.method == "GET":
        return jsonify({
            "endpoint": "/api/iq/login",
            "method": "POST", 
            "description": "IQ Option login endpoint",
            "status": "ready"
        })
    
    try:
        data = request.get_json()
        login_id = str(uuid.uuid4())
        
        # Simular proceso de login
        response = {
            "success": True,
            "login_id": login_id,
            "message": "Login request processed",
            "timestamp": time.time(),
            "balance_type": data.get("balance_type", "PRACTICE")
        }
        
        # Actualizar cache con datos de login simulados
        cache.set_balance({
            "balance": 10000.0,
            "currency": "USD", 
            "account_type": data.get("balance_type", "PRACTICE"),
            "logged_in": True,
            "login_time": time.time()
        })
        
        print(f"[API] Login procesado: {data.get('email', 'unknown')}")
        return jsonify(response)
        
    except Exception as e:
        print(f"[API] Error en login: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route("/symbols", methods=["GET", "POST"])
def iq_symbols():
    """Endpoint de símbolos disponibles"""
    if request.method == "POST":
        # Recibir símbolos del cliente IQ
        try:
            symbols_data = request.get_json()
            if isinstance(symbols_data, list):
                cache.set_symbols(symbols_data)
                return jsonify({"success": True, "count": len(symbols_data)})
            else:
                return jsonify({"success": False, "error": "Invalid data format"}), 400
        except Exception as e:
            print(f"[API] Error actualizando símbolos: {e}")
            return jsonify({"success": False, "error": str(e)}), 500
    
    # GET request - devolver símbolos
    symbols = cache.get_symbols()
    if not symbols:
        # Símbolos por defecto si no hay datos
        symbols = [
            {"symbol": "EURUSD", "displayName": "EUR/USD", "active": True, "category": "forex"},
            {"symbol": "GBPUSD", "displayName": "GBP/USD", "active": True, "category": "forex"},
            {"symbol": "USDJPY", "displayName": "USD/JPY", "active": True, "category": "forex"},
            {"symbol": "EURJPY", "displayName": "EUR/JPY", "active": True, "category": "forex"}
        ]
        cache.set_symbols(symbols)
    
    return jsonify(symbols)

@bp.route("/candles", methods=["GET", "POST"])
def iq_candles():
    """Endpoint de velas/candles"""
    if request.method == "POST":
        # Recibir velas del cliente IQ
        try:
            candles_data = request.get_json()
            symbol = candles_data.get("symbol", "UNKNOWN")
            timeframe = candles_data.get("timeframe", "M5")
            candles = candles_data.get("candles", [])
            
            if candles:
                cache.set_candles(symbol, timeframe, candles)
                return jsonify({"success": True, "count": len(candles)})
            else:
                return jsonify({"success": False, "error": "No candles provided"}), 400
                
        except Exception as e:
            print(f"[API] Error actualizando velas: {e}")
            return jsonify({"success": False, "error": str(e)}), 500
    
    # GET request - devolver velas
    symbol = request.args.get("symbol", "EURUSD")
    timeframe = request.args.get("timeframe", "M5")
    limit = int(request.args.get("limit", 50))
    
    candles = cache.get_candles(symbol, timeframe)
    
    if not candles:
        # Generar velas mock si no hay datos reales
        candles = generate_mock_candles(symbol, timeframe, limit)
        cache.set_candles(symbol, timeframe, candles)
    
    # Limitar número de velas devueltas
    limited_candles = candles[-limit:] if len(candles) > limit else candles
    
    return jsonify({
        "symbol": symbol,
        "timeframe": timeframe,
        "candles": limited_candles,
        "count": len(limited_candles),
        "source": "real" if cache.get_candles(symbol, timeframe) else "mock"
    })

@bp.route("/balance", methods=["GET", "POST"])
def iq_balance():
    """Endpoint de balance de cuenta"""
    if request.method == "POST":
        # Actualizar balance desde cliente IQ
        try:
            balance_data = request.get_json()
            cache.set_balance(balance_data)
            return jsonify({"success": True, "balance": balance_data})
        except Exception as e:
            print(f"[API] Error actualizando balance: {e}")
            return jsonify({"success": False, "error": str(e)}), 500
    
    # GET request - devolver balance actual
    balance = cache.get_balance()
    return jsonify(balance)

@bp.route("/orders", methods=["GET", "POST"])
def iq_orders():
    """Endpoint para órdenes de trading"""
    if request.method == "POST":
        # Procesar nueva orden
        try:
            order_data = request.get_json()
            order_id = str(uuid.uuid4())
            
            # Simular procesamiento de orden
            order = {
                "id": order_id,
                "symbol": order_data.get("symbol"),
                "direction": order_data.get("direction"),
                "amount": order_data.get("amount"),
                "status": "pending",
                "timestamp": time.time()
            }
            
            cache.orders_cache.append(order)
            print(f"[API] Nueva orden: {order}")
            
            return jsonify({"success": True, "order": order})
            
        except Exception as e:
            print(f"[API] Error procesando orden: {e}")
            return jsonify({"success": False, "error": str(e)}), 500
    
    # GET request - devolver órdenes
    return jsonify({"orders": cache.orders_cache})

def generate_mock_candles(symbol, timeframe, count=50):
    """Generar velas mock realistas"""
    base_prices = {
        "EURUSD": 1.0850, "GBPUSD": 1.2650, "USDJPY": 150.25,
        "EURJPY": 162.30, "AUDUSD": 0.6580, "USDCAD": 1.3720
    }
    
    base_price = base_prices.get(symbol, 1.0000)
    tf_seconds = {"M1": 60, "M5": 300, "M15": 900, "M30": 1800, "H1": 3600}.get(timeframe, 300)
    
    now = int(time.time())
    candle_start = (now // tf_seconds) * tf_seconds
    
    candles = []
    current_price = base_price
    
    for i in range(count):
        start_time = candle_start - (tf_seconds * (count - i - 1))
        end_time = start_time + tf_seconds
        
        # Simular movimiento realista
        price_change = random.uniform(-0.0005, 0.0005) * current_price
        open_price = current_price
        
        high_offset = random.uniform(0.0001, 0.0003) * current_price
        low_offset = random.uniform(0.0001, 0.0003) * current_price
        
        high_price = open_price + high_offset
        low_price = open_price - low_offset
        close_price = open_price + price_change
        
        # Asegurar coherencia high/low
        high_price = max(high_price, open_price, close_price)
        low_price = min(low_price, open_price, close_price)
        
        candle = {
            "symbol": symbol,
            "timeframe": timeframe,
            "from": start_time,
            "to": end_time,
            "open": round(open_price, 5),
            "high": round(high_price, 5),
            "low": round(low_price, 5),
            "close": round(close_price, 5),
            "volume": random.randint(500, 1500),
            "closed": end_time <= now
        }
        candles.append(candle)
        current_price = close_price
    
    return candles

# Registrar blueprint
app.register_blueprint(bp)

# Endpoint raíz para verificación
@app.route("/health")
def root_health():
    return jsonify({
        "service": "STC Trading System - IQ API Backend",
        "status": "running",
        "port": 5002,
        "endpoints": ["/api/iq/health", "/api/iq/symbols", "/api/iq/candles", "/api/iq/balance", "/api/iq/login", "/api/iq/orders"],
        "timestamp": time.time()
    })

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 STC TRADING SYSTEM - IQ API BACKEND")
    print("=" * 60)
    print("🔧 Servidor Flask iniciando...")
    print("🌐 Puerto: 5002")
    print("💾 Cache: Memoria (sin Redis)")
    print("📊 Endpoints disponibles:")
    print("   - GET  /health")
    print("   - GET  /api/iq/health")
    print("   - GET  /api/iq/symbols")
    print("   - GET  /api/iq/candles")
    print("   - GET  /api/iq/balance")
    print("   - POST /api/iq/login")
    print("   - POST /api/iq/orders")
    print("=" * 60)
    
    try:
        app.run(host="0.0.0.0", port=5002, debug=True, use_reloader=False)
    except Exception as e:
        print(f"❌ Error iniciando servidor: {e}")
