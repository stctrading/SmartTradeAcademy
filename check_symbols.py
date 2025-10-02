#!/usr/bin/env python3
"""
Verificar símbolos disponibles en IQ Option
"""
import requests
import json

API_BASE = "http://localhost:5002"

def check_available_symbols():
    """Verificar qué símbolos están disponibles"""
    print("🔍 VERIFICANDO SÍMBOLOS DISPONIBLES EN IQ OPTION")
    print("=" * 50)
    
    try:
        response = requests.get(f"{API_BASE}/api/iq/symbols", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            symbols = data.get('symbols', [])
            source = data.get('source', 'unknown')
            count = data.get('count', len(symbols))
            
            print(f"📊 Símbolos encontrados: {count}")
            print(f"🔗 Fuente: {source}")
            print("-" * 30)
            
            if symbols:
                print("📋 Lista de símbolos disponibles:")
                for i, symbol in enumerate(symbols[:20], 1):  # Primeros 20
                    if isinstance(symbol, dict):
                        symbol_name = symbol.get('symbol', symbol.get('displayName', 'N/A'))
                        active = symbol.get('active', True)
                        category = symbol.get('category', 'N/A')
                        status = "✅" if active else "❌"
                        print(f"  {i:2}. {status} {symbol_name} ({category})")
                    else:
                        print(f"  {i:2}. ✅ {symbol}")
                
                if len(symbols) > 20:
                    print(f"     ... y {len(symbols) - 20} más")
                    
                # Buscar símbolos comunes
                common_symbols = ['EURUSD', 'EURUSD-OTC', 'GBPUSD', 'GBPUSD-OTC', 'USDJPY', 'USDJPY-OTC']
                print(f"\n🎯 Verificando símbolos comunes:")
                
                for common in common_symbols:
                    found = False
                    for symbol in symbols:
                        symbol_name = symbol if isinstance(symbol, str) else symbol.get('symbol', '')
                        if common.upper() in symbol_name.upper():
                            print(f"  ✅ {common} -> Encontrado como '{symbol_name}'")
                            found = True
                            break
                    
                    if not found:
                        print(f"  ❌ {common} -> No disponible")
                        
            else:
                print("❌ No hay símbolos disponibles")
                if source == 'default':
                    print("💡 El cliente IQ Option puede no estar conectado")
        else:
            print(f"❌ Error obteniendo símbolos: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def check_market_status():
    """Verificar estado del mercado"""
    print(f"\n🕒 VERIFICANDO ESTADO DEL MERCADO")
    print("=" * 30)
    
    from datetime import datetime, timezone
    import pytz
    
    # Hora actual
    now = datetime.now(timezone.utc)
    
    # Horarios principales de mercados Forex
    markets = {
        'Sydney': pytz.timezone('Australia/Sydney'),
        'Tokyo': pytz.timezone('Asia/Tokyo'),
        'London': pytz.timezone('Europe/London'),
        'New York': pytz.timezone('America/New_York')
    }
    
    print(f"🌍 Hora UTC actual: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📅 Día de la semana: {now.strftime('%A')}")
    
    print(f"\n🏛️ Horarios de mercados principales:")
    for market_name, tz in markets.items():
        local_time = now.astimezone(tz)
        hour = local_time.hour
        day = local_time.weekday()  # 0=Monday, 6=Sunday
        
        # Forex generalmente opera L-V, con algunas excepciones
        if market_name == 'Sydney':
            is_open = day < 5 and (hour >= 21 or hour < 6)  # 21:00-06:00
        elif market_name == 'Tokyo': 
            is_open = day < 5 and hour >= 0 and hour < 9    # 00:00-09:00
        elif market_name == 'London':
            is_open = day < 5 and hour >= 8 and hour < 17   # 08:00-17:00
        elif market_name == 'New York':
            is_open = day < 5 and hour >= 13 and hour < 22  # 13:00-22:00
        
        status = "🟢 ABIERTO" if is_open else "🔴 CERRADO"
        print(f"  {market_name:10} {local_time.strftime('%H:%M')} {status}")
    
    # Verificar si es fin de semana
    if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
        print(f"\n⚠️  ES FIN DE SEMANA - Los mercados Forex están cerrados")
        print(f"💡 Los mercados abren el lunes a las 00:00 UTC")
    else:
        print(f"\n✅ Es día hábil - Algunos mercados pueden estar abiertos")

def suggest_solutions():
    """Sugerir soluciones para el problema"""
    print(f"\n💡 POSIBLES SOLUCIONES:")
    print("=" * 30)
    print("1. 🔄 Intentar con símbolos OTC (Over The Counter):")
    print("   - EURUSD-OTC en lugar de EURUSD")
    print("   - Los símbolos OTC a menudo están disponibles 24/7")
    print()
    print("2. ⏰ Verificar horarios de mercado:")
    print("   - Forex opera Lunes-Viernes principalmente")
    print("   - Algunos pares pueden tener horarios específicos")
    print()
    print("3. 🔧 Verificar configuración de IQ Option:")
    print("   - Cuenta debe estar activa y verificada")
    print("   - Región geográfica puede afectar símbolos disponibles")
    print()
    print("4. 💰 Verificar parámetros de orden:")
    print("   - Monto mínimo: $1 (ya correcto)")
    print("   - Duración: 1-60 minutos (usando 5min, correcto)")
    print()
    print("5. 🌍 Probar símbolos de criptomonedas o indices:")
    print("   - Pueden estar disponibles cuando Forex está cerrado")

if __name__ == "__main__":
    check_available_symbols()
    check_market_status()
    suggest_solutions()
