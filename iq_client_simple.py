#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cliente IQ Option simplificado - Sin Redis, con cache en memoria
Para pruebas y depuración del sistema STC Trading
"""

import os, time, logging, json, threading
from contextlib import suppress
from typing import Dict, List, Tuple
from dotenv import load_dotenv
import httpx
from collections import defaultdict, deque

try:
    from iqoptionapi.stable_api import IQ_Option
except Exception as e:
    print("⚠️ IQ Option API no disponible. Usando modo simulación...")
    IQ_Option = None

# Cargar configuración
load_dotenv()

# Configuración
SERVER_BASE = os.getenv("SERVER_BASE", "http://127.0.0.1:5002").rstrip("/")
IQ_EMAIL = os.getenv("IQ_EMAIL", "")
IQ_PASSWORD = os.getenv("IQ_PASSWORD", "")
IQ_BALANCE_TYPE = os.getenv("IQ_BALANCE_TYPE", "PRACTICE")
IQ_SYMBOLS = [s.strip().upper() for s in os.getenv("IQ_SYMBOLS", "EURUSD").split(",") if s.strip()]
IQ_TIMEFRAMES = [s.strip().upper() for s in os.getenv("IQ_TIMEFRAMES", "M1,M5").split(",") if s.strip()]
IQ_PUSH_INTERVAL_SEC = float(os.getenv("IQ_PUSH_INTERVAL_SEC", "1.0"))
HTTP_TIMEOUT = float(os.getenv("HTTP_TIMEOUT", "4.0"))

TF_TO_SEC = {"M1": 60, "M5": 300, "M15": 900, "M30": 1800, "H1": 3600}

# Configurar logging
logging.basicConfig(level=logging.INFO, format="(iq_client) %(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger("iq-client")

def coerce_float(v, d=0.0):
    try: 
        return float(v)
    except: 
        return float(d)

class MemoryCache:
    """Cache en memoria para reemplazar Redis temporalmente"""
    def __init__(self):
        self.data = {}
        self.lists = defaultdict(deque)
        self.lock = threading.Lock()
        log.info("📦 Cache en memoria inicializado")
    
    def set(self, key, value):
        with self.lock:
            self.data[key] = str(value)
    
    def get(self, key):
        with self.lock:
            return self.data.get(key)
    
    def lpush(self, key, value):
        with self.lock:
            self.lists[key].appendleft(str(value))
    
    def lpop(self, key):
        with self.lock:
            try:
                return self.lists[key].popleft()
            except IndexError:
                return None

class IQFeedSimple:
    def __init__(self):
        self.cache = MemoryCache()
        self.http = httpx.Client(timeout=HTTP_TIMEOUT)
        self.last_sent_from: Dict[Tuple[str, int], int] = {}
        self.api = None
        self.connected = False
        
        # Datos de simulación
        self.sim_balance = 10000.0
        self.sim_base_prices = {
            "EURUSD": 1.0850, "GBPUSD": 1.2650, "USDJPY": 150.25, 
            "EURJPY": 162.30, "AUDUSD": 0.6580, "USDCAD": 1.3720
        }
        
        log.info("🔌 Cliente IQ Option inicializado")

    def connect(self):
        """Conectar a IQ Option API o usar modo simulación"""
        if IQ_Option and IQ_EMAIL and IQ_PASSWORD:
            try:
                log.info("🔐 Intentando conectar con IQ Option...")
                self.api = IQ_Option(IQ_EMAIL, IQ_PASSWORD)
                ok, reason = self.api.connect()
                if ok:
                    self.api.change_balance(IQ_BALANCE_TYPE)
                    time.sleep(1.0)
                    self.connected = True
                    log.info("✅ Conectado a IQ Option (%s)", IQ_BALANCE_TYPE)
                    return True
                else:
                    log.warning("⚠️ No se pudo conectar a IQ Option: %s", reason)
                    log.info("🔄 Cambiando a modo simulación...")
            except Exception as e:
                log.error("❌ Error conectando a IQ Option: %s", e)
                log.info("🔄 Cambiando a modo simulación...")
        else:
            log.info("🔄 Usando modo simulación (credenciales no configuradas)")
        
        self.connected = False
        return True

    def get_balance(self):
        """Obtener balance actual"""
        if self.connected and self.api:
            try:
                balance = self.api.get_balance()
                return coerce_float(balance, 10000.0)
            except:
                pass
        return self.sim_balance

    def get_available_symbols(self):
        """Obtener símbolos disponibles"""
        if self.connected and self.api:
            try:
                # Intentar obtener símbolos reales de IQ Option
                symbols = []
                for sym in IQ_SYMBOLS:
                    symbols.append({
                        "symbol": sym,
                        "displayName": sym.replace("USD", "/USD").replace("EUR", "EUR/").replace("GBP", "GBP/"),
                        "active": True,
                        "category": "forex"
                    })
                return symbols
            except:
                pass
        
        # Símbolos de simulación
        symbols = []
        for sym in IQ_SYMBOLS:
            symbols.append({
                "symbol": sym,
                "displayName": sym.replace("USD", "/USD").replace("EUR", "EUR/").replace("GBP", "GBP/"),
                "active": True,
                "category": "forex"
            })
        return symbols

    def fetch_realtime_candles(self, symbol, tf_sec):
        """Obtener velas en tiempo real"""
        if self.connected and self.api:
            try:
                # Intentar obtener datos reales
                candles = self.api.get_candles(symbol, tf_sec, 10, time.time())
                if candles:
                    result = []
                    for candle in candles:
                        result.append({
                            "symbol": symbol,
                            "timeframe": f"{tf_sec//60}min",
                            "from": int(candle["from"]),
                            "to": int(candle["to"]),
                            "open": coerce_float(candle["open"]),
                            "high": coerce_float(candle["max"]),
                            "low": coerce_float(candle["min"]),
                            "close": coerce_float(candle["close"]),
                            "volume": coerce_float(candle.get("volume", 1000))
                        })
                    return result
            except Exception as e:
                log.debug("Error obteniendo velas reales: %s", e)
        
        # Generar velas de simulación
        return self.generate_mock_candles(symbol, tf_sec)

    def generate_mock_candles(self, symbol, tf_sec):
        """Generar velas de simulación realistas"""
        import random
        
        base_price = self.sim_base_prices.get(symbol, 1.0000)
        now = int(time.time())
        candle_start = (now // tf_sec) * tf_sec
        
        candles = []
        for i in range(5):  # Últimas 5 velas
            start_time = candle_start - (tf_sec * (4 - i))
            end_time = start_time + tf_sec
            
            # Simular movimiento de precio realista
            price_change = random.uniform(-0.001, 0.001) * base_price
            open_price = base_price + price_change
            
            high_offset = random.uniform(0.0001, 0.0005) * base_price
            low_offset = random.uniform(0.0001, 0.0005) * base_price
            
            high_price = open_price + high_offset
            low_price = open_price - low_offset
            
            close_change = random.uniform(-0.0003, 0.0003) * base_price
            close_price = open_price + close_change
            
            # Asegurar que high/low sean coherentes
            high_price = max(high_price, open_price, close_price)
            low_price = min(low_price, open_price, close_price)
            
            candle = {
                "symbol": symbol,
                "timeframe": f"{tf_sec//60}min",
                "from": start_time,
                "to": end_time,
                "open": round(open_price, 5),
                "high": round(high_price, 5),
                "low": round(low_price, 5),
                "close": round(close_price, 5),
                "volume": random.randint(800, 1500)
            }
            candles.append(candle)
            
            # Actualizar precio base para siguiente vela
            base_price = close_price
        
        # Actualizar precio base para próxima vez
        self.sim_base_prices[symbol] = base_price
        
        return candles

    def push_to_api(self, endpoint, data):
        """Enviar datos al API backend"""
        try:
            url = f"{SERVER_BASE}{endpoint}"
            response = self.http.post(url, json=data, timeout=HTTP_TIMEOUT)
            if response.status_code == 200:
                log.debug("✅ Enviado a %s: %d registros", endpoint, len(data) if isinstance(data, list) else 1)
                return True
            else:
                log.warning("⚠️ Error en %s: HTTP %d", endpoint, response.status_code)
                return False
        except Exception as e:
            log.debug("❌ Error enviando a %s: %s", endpoint, e)
            return False

    def push_balance(self):
        """Enviar balance actual"""
        balance = self.get_balance()
        data = {
            "balance": balance,
            "currency": "USD",
            "account_type": IQ_BALANCE_TYPE,
            "timestamp": time.time()
        }
        self.push_to_api("/api/iq/balance", data)
        log.info("💰 Balance actual: $%.2f (%s)", balance, IQ_BALANCE_TYPE)

    def push_available_symbols(self):
        """Enviar símbolos disponibles"""
        symbols = self.get_available_symbols()
        if symbols:
            self.push_to_api("/api/iq/symbols", symbols)
            log.info("🏛️ Enviados %d símbolos disponibles", len(symbols))

    def push_candles(self, symbol, timeframe, candles_data):
        """Enviar datos de velas"""
        if not candles_data:
            return
        
        data = {
            "symbol": symbol,
            "timeframe": timeframe,
            "candles": candles_data,
            "timestamp": time.time()
        }
        
        success = self.push_to_api("/api/iq/candles", data)
        if success:
            log.info("📊 %s %s: %d velas (%.5f-%.5f)", 
                    symbol, timeframe, len(candles_data),
                    candles_data[0]["close"], candles_data[-1]["close"])

    def loop(self):
        """Bucle principal del cliente"""
        log.info("🚀 Iniciando cliente IQ Option...")
        
        # Conectar
        self.connect()
        
        # Enviar información inicial
        self.push_available_symbols()
        self.push_balance()
        
        last_balance_update = 0
        last_symbols_update = 0
        
        log.info("🔄 Iniciando bucle de datos (cada %.1fs)...", IQ_PUSH_INTERVAL_SEC)
        
        try:
            while True:
                t0 = time.time()
                
                # Actualizar balance cada 30 segundos
                if time.time() - last_balance_update >= 30:
                    self.push_balance()
                    last_balance_update = time.time()
                
                # Actualizar símbolos cada 5 minutos
                if time.time() - last_symbols_update >= 300:
                    self.push_available_symbols()
                    last_symbols_update = time.time()
                
                # Obtener y enviar velas para cada símbolo y timeframe
                for sym in IQ_SYMBOLS:
                    for tf in IQ_TIMEFRAMES:
                        tf_sec = TF_TO_SEC.get(tf, 60)
                        candles = self.fetch_realtime_candles(sym, tf_sec)
                        
                        if candles:
                            # Filtrar velas nuevas
                            key = (sym, tf_sec)
                            last_from = self.last_sent_from.get(key, 0)
                            
                            new_candles = [c for c in candles if c["from"] > last_from]
                            if not new_candles and candles:
                                new_candles = [candles[-1]]  # Al menos la última vela
                            
                            # Marcar velas cerradas
                            now = int(time.time())
                            for candle in new_candles:
                                candle["closed"] = (now >= candle["to"])
                            
                            # Enviar velas
                            self.push_candles(sym, tf, new_candles)
                            
                            # Actualizar último timestamp enviado
                            closed_candles = [c for c in new_candles if c.get("closed")]
                            if closed_candles:
                                self.last_sent_from[key] = max([c["from"] for c in closed_candles])
                
                # Pausa hasta el próximo ciclo
                elapsed = time.time() - t0
                sleep_time = max(0.0, IQ_PUSH_INTERVAL_SEC - elapsed)
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            log.info("🛑 Deteniendo cliente...")
        except Exception as e:
            log.error("❌ Error en bucle principal: %s", e)
        finally:
            if self.api and hasattr(self.api, 'close'):
                with suppress(Exception):
                    self.api.close()
            log.info("✅ Cliente IQ Option detenido")

if __name__ == "__main__":
    try:
        client = IQFeedSimple()
        client.loop()
    except KeyboardInterrupt:
        log.info("🛑 Programa interrumpido por el usuario")
    except Exception as e:
        log.error("❌ Error fatal: %s", e)
        raise
