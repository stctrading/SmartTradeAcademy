#!/usr/bin/env python3
"""
iq_routes_redis_patch.py - IQ API (puerto 5002)
- Encola logins y órdenes en Redis
- Endpoint de velas mock
- CORS habilitado para que el dashboard en 5001 pueda consumir esta API
"""

from flask import request, jsonify
from candles_store import store_batch, read_last

import os, json, time, uuid, random
from flask import Flask, Blueprint, request, jsonify
import threading
from collections import defaultdict, deque

# --- NUEVOS ENDPOINTS V2, libres de conflicto con rutas antiguas ---

from flask import request, jsonify
from candles_store import store_batch, read_last

# @app.post("/api/iq/candles_v2")
def post_candles_v2():
    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({"error": "JSON requerido"}), 400

    if isinstance(data, dict) and "candles" in data:
        candles = data["candles"]
    elif isinstance(data, list):
        candles = data
    elif isinstance(data, dict):
        candles = [data]
    else:
        candles = []

    symbol = request.args.get("symbol")
    timeframe = (request.args.get("timeframe") or "M5").upper()

    if not symbol and candles and isinstance(candles[0], dict):
        symbol = candles[0].get("symbol")

    if not symbol:
        return jsonify({"error": "symbol requerido (query ?symbol=... o dentro de cada vela)"}), 400

    info = store_batch(symbol, timeframe, candles)
    return jsonify({"status": "ok", "saved": info["inserted"], "size": info["size"], "csv_written": info["csv_written"]})

# @app.get("/api/iq/candles_v2")
def get_candles_v2():
    symbol = request.args.get("symbol")
    tf = (request.args.get("timeframe") or "M5").upper()
    try:
        limit = int(request.args.get("limit", "200"))
    except ValueError:
        limit = 200

    if not symbol:
        return jsonify({"error": "symbol requerido"}), 400

    arr = read_last(symbol, tf, limit=limit)
    # Para distinguir que estás en la ruta nueva, puedes añadir meta si quieres:
    # return jsonify({"source":"v2","data":arr})
    return jsonify(arr)

# Cache en memoria que simula Redis
class MemoryRedis:
    def __init__(self):
        self.data = {}
        self.lists = defaultdict(deque)
        self.lock = threading.Lock()
        self.candles_data = {}
        self.symbols_data = []
        self.balance_data = {"balance": 10000.0, "currency": "USD"}
        print("[MemoryRedis] Inicializado - Cache en memoria")


    def setex(self, key, time, value):
        """Simula SETEX de Redis: guarda con expiración en segundos"""
        self.set(key, value)
        print(f"[MemoryRedis] SETEX {key} = {value} (TTL: {time}s)")


    def setex(self, key, time, value):
        """Simula SETEX de Redis: guarda con expiración en segundos"""
        self.set(key, value)
        print(f"[MemoryRedis] SETEX {key} = {value} (TTL: {time}s)")

    
    def get(self, key):
        with self.lock:
            return self.data.get(key)
    
    def set(self, key, value):
        with self.lock:
            self.data[key] = value
    
    def lpush(self, key, value):
        with self.lock:
            self.lists[key].appendleft(value)
    
    def rpush(self, key, value):
        with self.lock:
            self.lists[key].append(value)
    
    def lpop(self, key):
        with self.lock:
            try:
                return self.lists[key].popleft()
            except IndexError:
                return None
    
    def llen(self, key):
        with self.lock:
            return len(self.lists[key])

try:
    # CORS es opcional pero recomendado cuando el dashboard está en 5001
    from flask_cors import CORS
    USE_CORS = True
except Exception:
    USE_CORS = False

app = Flask(__name__)

# Añadir soporte para CORS solo si está disponible
if USE_CORS:
    CORS(app, 
         resources={r"/*": {"origins": "*"}}, 
         allow_headers=["Content-Type", "Accept", "Authorization", "Access-Control-Allow-Origin"],
         methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"])
else:
    # CORS manual si no está disponible flask-cors
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

# Usar cache en memoria en lugar de Redis
r = MemoryRedis()

bp = Blueprint("iq", __name__, url_prefix="/api/iq")

@bp.route("/login", methods=["GET", "POST"])
def iq_login():
    if request.method == "GET":
        # GET request - retornar información del endpoint
        return jsonify({
            "endpoint": "/api/iq/login",
            "method": "POST",
            "description": "IQ Option login endpoint",
            "required_fields": ["email", "password"],
            "optional_fields": ["balance_type"],
            "example": {
                "email": "user@example.com",
                "password": "your_password",
                "balance_type": "PRACTICE"
            }
        })
    
    # POST request - procesar login
    data = request.get_json(force=True, silent=True) or {}
    email = (data.get("email") or "").strip()
    password = data.get("password") or ""
    balance = data.get("balance_type") or "PRACTICE"
    
    if not email or not password:
        return jsonify(error="missing credentials"), 400

    payload = {
        "id": str(uuid.uuid4()),
        "email": email,
        "password": password,
        "balance": balance,
        "created_at": int(time.time())
    }
    r.rpush("logins", json.dumps(payload))
    
    # Guardar sesión activa en Redis
    session_key = "iq_active_session"
    session_data = {
        "login_id": payload["id"],
        "email": email,
        "balance_type": balance,
        "logged_in_at": int(time.time()),
        "status": "active"
    }
    r.setex(session_key, 7200, json.dumps(session_data))  # 2 horas
    
    return jsonify(ok=True, queued=True, id=payload["id"], session=session_data)

@bp.route("/logout", methods=["POST"])
def iq_logout():
    """Logout de IQ Option"""
    try:
        # Limpiar sesión activa
        session_key = "iq_active_session"
        r.delete(session_key)
        
        # Encolar comando de logout para el cliente
        logout_payload = {
            "id": str(uuid.uuid4()),
            "action": "logout",
            "created_at": int(time.time())
        }
        r.rpush("logouts", json.dumps(logout_payload))
        
        return jsonify({
            "ok": True,
            "message": "Logout successful",
            "logout_id": logout_payload["id"]
        })
        
    except Exception as e:
        return jsonify({"error": f"Error en logout: {str(e)}"}), 500

@bp.route("/session", methods=["GET"])
def iq_session():
    """Obtener información de sesión activa"""
    try:
        session_key = "iq_active_session"
        session_data = r.get(session_key)
        
        if session_data:
            try:
                session_info = json.loads(session_data)
                return jsonify({
                    "active": True,
                    "session": session_info
                })
            except json.JSONDecodeError:
                pass
        
        return jsonify({
            "active": False,
            "message": "No active session"
        })
        
    except Exception as e:
        return jsonify({"error": f"Error obteniendo sesión: {str(e)}"}), 500

@bp.route("/order", methods=["POST"])
def iq_order():
    data = request.get_json(force=True, silent=True) or {}
    sym = data.get("symbol")
    act = data.get("action")
    if not sym or not act:
        return jsonify(error="missing fields"), 400
    payload = {
        "id": str(uuid.uuid4()),
        "symbol": sym,
        "action": act,
        "amount": float(data.get("amount", 5)),
        "option_type": data.get("option_type", "binary"),
        "duration": int(data.get("duration", 5)),
        "created_at": int(time.time())
    }
    r.rpush("orders", json.dumps(payload))
    return jsonify(ok=True, order_id=payload["id"], type=payload["option_type"])

@bp.route("/trade", methods=["POST", "OPTIONS"])
def iq_trade_alias():
    """Alias para /order - compatibilidad con dashboard"""
    if request.method == "OPTIONS":
        return jsonify(ok=True)
        
    try:
        data = request.get_json(force=True, silent=True) or {}
        
        # Mapear nombres de campos del dashboard
        if "direction" in data:
            data["action"] = data["direction"].lower()
        if "symbol" in data:
            data["asset"] = data["symbol"]
        if "expiration" in data:
            data["duration"] = data["expiration"]
            
        # Usar la misma lógica que /order
        asset = data.get("asset", "EURUSD-OTC").upper()
        if not asset.endswith("-OTC"):
            asset += "-OTC"
            
        act = data.get("action", "call").lower()
        if act not in ["call", "put"]:
            return jsonify(success=False, message=f"Acción inválida: {act}"), 400

        payload = {
            "id": int(time.time() * 1000),
            "asset": asset,
            "action": act,
            "amount": float(data.get("amount", 1)),
            "option_type": data.get("option_type", "binary"),
            "duration": int(data.get("duration", 1)),
            "created_at": int(time.time())
        }
        
        r.rpush("orders", json.dumps(payload))
        
        return jsonify({
            "success": True,
            "trade_id": payload["id"],
            "message": f"Orden {act.upper()} enviada para {asset}",
            "order_id": payload["id"],
            "type": payload["option_type"]
        })
        
    except Exception as e:
        return jsonify(success=False, message=f"Error procesando trade: {str(e)}"), 500

@bp.route("/order_results", methods=["GET"])
def iq_order_results():
    """Endpoint para obtener resultados de órdenes ejecutadas"""
    try:
        # Obtener todos los resultados
        results = []
        while True:
            result_data = r.lpop("order_results")
            if not result_data:
                break
            try:
                result = json.loads(result_data)
                results.append(result)
            except json.JSONDecodeError:
                continue
        
        return jsonify({
            "results": results,
            "count": len(results)
        })
        
    except Exception as e:
        return jsonify({"error": f"Error obteniendo resultados: {str(e)}"}), 500

@bp.route("/symbols", methods=["GET"])
def iq_symbols():
    """Endpoint para obtener símbolos disponibles desde IQ Option"""
    try:
        # Intentar obtener desde cache en memoria
        if r.symbols_data:
            return jsonify({
                "symbols": r.symbols_data,
                "count": len(r.symbols_data),
                "source": "iq_client"
            })
        
        # No hay símbolos disponibles - devolver símbolos por defecto
        default_symbols = [
            {"symbol": "EURUSD", "displayName": "EUR/USD", "active": True, "category": "forex"},
            {"symbol": "GBPUSD", "displayName": "GBP/USD", "active": True, "category": "forex"},
            {"symbol": "USDJPY", "displayName": "USD/JPY", "active": True, "category": "forex"},
            {"symbol": "EURJPY", "displayName": "EUR/JPY", "active": True, "category": "forex"}
        ]
        r.symbols_data = default_symbols
        return jsonify({
            "symbols": default_symbols,
            "count": len(default_symbols),
            "source": "default"
        })
        
    except Exception as e:
        return jsonify({"error": f"Error obteniendo símbolos: {str(e)}"}), 500

@bp.route("/balance", methods=["GET", "POST"])
def iq_balance():
    """Endpoint para obtener/actualizar el saldo de la cuenta IQ Option"""
    balance_key = "iq_session_balance"
    
    if request.method == "POST":
        # Actualizar balance (viene del iq_client.py)
        try:
            data = request.get_json(force=True, silent=True) or {}
            balance_data = data.get("balance_data")
            
            if balance_data:
                # Guardar en cache en memoria
                r.balance_data = balance_data
                print(f"💰 Balance IQ guardado: ${balance_data.get('balance', 0):.2f}")
                return jsonify({"status": "success", "balance": balance_data})
            else:
                return jsonify({"error": "No balance data provided"}), 400
                
        except Exception as e:
            return jsonify({"error": f"Error actualizando balance: {str(e)}"}), 500
    
    # GET - Obtener balance
    try:
        # Intentar obtener desde cache en memoria
        if r.balance_data:
            return jsonify(r.balance_data)
        
        # No hay datos reales disponibles - devolver balance por defecto
        default_balance = {
            "balance": 10000.0,
            "currency": "USD",
            "balance_type": "PRACTICE"
        }
        r.balance_data = default_balance
        return jsonify(default_balance)
        
    except Exception as e:
        return jsonify(error=f"Error obteniendo balance: {str(e)}"), 500

@bp.route("/candles", methods=["GET", "POST"])
def iq_candles():
    if request.method == "POST":
        # Recibir velas desde iq_client.py
        try:
            data = request.get_json(force=True, silent=True) or {}
            symbol = data.get("symbol", "EURUSD-OTC")
            timeframe = data.get("timeframe", "M5") 
            candles = data.get("candles", [])
            
            if candles:
                # Guardar velas en cache en memoria
                candles_key = f"{symbol}_{timeframe}"
                r.candles_data[candles_key] = candles
                print(f"✅ Guardadas {len(candles)} velas: {symbol} {timeframe}")
                
            return jsonify({"status": "success", "candles_stored": len(candles)})
            
        except Exception as e:
            return jsonify({"error": f"Error procesando velas: {str(e)}"}), 500
    
    # GET - Servir velas (mock o desde Redis)
    symbol = request.args.get("symbol", "EURUSD-OTC")
    timeframe = request.args.get("timeframe", "M5")
    limit = int(request.args.get("limit", 200))
    
    # Intentar obtener velas desde cache en memoria
    candles_key = f"{symbol}_{timeframe}"
    real_candles = r.candles_data.get(candles_key)
    
    if real_candles:
        print(f"🔄 Sirviendo {len(real_candles)} velas: {symbol}")
        return jsonify(real_candles)
    
    # No hay velas reales disponibles - generar velas mock
    print(f"📊 Generando velas mock para {symbol} {timeframe}")
    
    # Generar velas mock simples
    base_prices = {"EURUSD": 1.0850, "GBPUSD": 1.2650, "USDJPY": 150.25}
    base_price = base_prices.get(symbol.replace("-OTC", ""), 1.0000)
    
    tf_seconds = {"M1": 60, "M5": 300, "M15": 900}.get(timeframe, 300)
    now = int(time.time())
    candle_start = (now // tf_seconds) * tf_seconds
    
    mock_candles = []
    for i in range(50):
        start_time = candle_start - (tf_seconds * (49 - i))
        end_time = start_time + tf_seconds
        price_var = random.uniform(-0.001, 0.001) * base_price
        open_price = base_price + price_var
        close_price = open_price + random.uniform(-0.0005, 0.0005) * base_price
        high_price = max(open_price, close_price) + random.uniform(0, 0.0002) * base_price
        low_price = min(open_price, close_price) - random.uniform(0, 0.0002) * base_price
        
        mock_candles.append({
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
        })
    
    r.candles_data[candles_key] = mock_candles
    return jsonify(mock_candles)

@app.route("/health")
def health():
    return {"status": "ok", "redis": True}

# CORS manual - Agregar headers CORS a todas las respuestas
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = (
        'Content-Type,Authorization,Accept,X-Requested-With')
    response.headers['Access-Control-Allow-Methods'] = (
        'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    response.headers['Access-Control-Max-Age'] = '86400'
    return response

# Manejar preflight OPTIONS requests para todos los endpoints
@app.route('/api/iq/login', methods=['OPTIONS'])
@app.route('/api/iq/logout', methods=['OPTIONS'])
@app.route('/api/iq/session', methods=['OPTIONS'])
@app.route('/api/iq/order', methods=['OPTIONS'])  
@app.route('/api/iq/order_results', methods=['OPTIONS'])
@app.route('/api/iq/symbols', methods=['OPTIONS'])
@app.route('/api/iq/balance', methods=['OPTIONS'])
@app.route('/api/iq/candles', methods=['OPTIONS'])
@app.route('/health', methods=['OPTIONS'])
def handle_options():
    response = jsonify({'status': 'ok'})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = (
        'Content-Type,Authorization,Accept,X-Requested-With')
    response.headers['Access-Control-Allow-Methods'] = (
        'GET,PUT,POST,DELETE,OPTIONS,HEAD')
    response.headers['Access-Control-Max-Age'] = '86400'
    return response

app.register_blueprint(bp)

def get_redis_candles(symbol: str, limit: int = 200) -> list:
    """Obtener velas desde Redis"""
    try:
        # Implementar lógica para obtener desde Redis
        # Por ahora retornamos lista vacía ya que usamos CSV
        return []
    except Exception as e:
        print(f"Error obteniendo velas desde Redis: {e}")
        return []

@app.get("/api/iq/candles")
def get_candles():
    """
    Devuelve las últimas N velas en orden ascendente.
    """
    symbol = request.args.get("symbol")
    tf = (request.args.get("timeframe") or "M5").upper()
    try:
        limit = int(request.args.get("limit", "200"))
    except ValueError:
        limit = 200

    if not symbol:
        return jsonify({"error": "symbol requerido"}), 400

    # Obtener velas desde el almacén CSV
    csv_candles = read_last(symbol, tf, limit=limit)
    
    if csv_candles:
        print(f"✅ Devolviendo {len(csv_candles)} velas desde CSV para {symbol}")
        return jsonify(csv_candles)
    
    # Si no hay en CSV, obtener desde Redis
    redis_candles = get_redis_candles(symbol, limit)
    
    if redis_candles:
        print(f"✅ Devolviendo {len(redis_candles)} velas desde Redis para {symbol}")
        return jsonify(redis_candles)
    
    print(f"⚠️ No se encontraron velas para {symbol}")
    return jsonify([])


if __name__ == "__main__":
    print("[IQ ROUTES] on http://127.0.0.1:5002 (Cache: Memoria)")
    app.run(host="0.0.0.0", port=5002, debug=True, use_reloader=False)