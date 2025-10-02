#!/usr/bin/env python3
"""
Trading Inteligente con Detección de Símbolos
Detecta automáticamente símbolos disponibles y horarios de mercado
"""
import requests
import json
from datetime import datetime, timezone

API_BASE = "http://localhost:5002"

def get_available_symbols():
    """Obtener símbolos realmente disponibles"""
    try:
        response = requests.get(f"{API_BASE}/api/iq/symbols", timeout=5)
        if response.status_code == 200:
            data = response.json()
            symbols = data.get('symbols', [])
            
            # Extraer nombres de símbolos
            symbol_names = []
            for symbol in symbols:
                if isinstance(symbol, dict):
                    name = symbol.get('symbol', symbol.get('displayName', ''))
                else:
                    name = str(symbol)
                if name:
                    symbol_names.append(name)
                    
            return symbol_names
        return []
    except:
        return []

def find_best_symbol():
    """Encontrar el mejor símbolo disponible para trading"""
    symbols = get_available_symbols()
    
    # Lista de prioridades (de mejor a peor)
    priority_symbols = [
        'EURUSD-OTC', 'EURUSD', 
        'GBPUSD-OTC', 'GBPUSD',
        'USDJPY-OTC', 'USDJPY',
        'BTCUSD', 'BTC/USD',
        'ETHUSD', 'ETH/USD'
    ]
    
    for preferred in priority_symbols:
        for available in symbols:
            if preferred.upper() in available.upper():
                return available
                
    # Si no encuentra ninguno de los preferidos, usar el primero disponible
    return symbols[0] if symbols else "EURUSD"

def send_smart_order(direction):
    """Enviar orden inteligente con el mejor símbolo disponible"""
    print(f"🧠 ORDEN INTELIGENTE {direction}")
    print("-" * 30)
    
    # Detectar mejor símbolo
    best_symbol = find_best_symbol()
    print(f"🎯 Símbolo seleccionado: {best_symbol}")
    
    # Configuración de orden
    order = {
        "symbol": best_symbol,
        "action": "BUY" if direction == "CALL" else "SELL",
        "amount": 1.0,
        "duration": 5,  # 5 minutos
        "option_type": "binary"
    }
    
    print(f"💰 Monto: ${order['amount']}")
    print(f"⏰ Duración: {order['duration']} min")
    print(f"🎯 Dirección: {direction}")
    
    try:
        response = requests.post(
            f"{API_BASE}/api/iq/order",
            json=order,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Orden {direction} enviada!")
            print(f"🆔 ID: {result.get('order_id')}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 {response.text}")
            
            # Si falla, intentar con símbolo OTC
            if not best_symbol.endswith('-OTC'):
                print(f"🔄 Reintentando con {best_symbol}-OTC...")
                order['symbol'] = f"{best_symbol}-OTC"
                
                response = requests.post(
                    f"{API_BASE}/api/iq/order",
                    json=order,
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Orden {direction} enviada con OTC!")
                    print(f"🆔 ID: {result.get('order_id')}")
                    return True
            
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def show_market_info():
    """Mostrar información del mercado"""
    print("🌍 INFORMACIÓN DEL MERCADO")
    print("-" * 30)
    
    # Obtener símbolos disponibles
    symbols = get_available_symbols()
    print(f"📊 Símbolos disponibles: {len(symbols)}")
    
    if symbols:
        print("🎯 Mejores opciones:")
        priority_symbols = ['EURUSD-OTC', 'GBPUSD-OTC', 'USDJPY-OTC', 'BTCUSD', 'ETHUSD']
        found_count = 0
        
        for priority in priority_symbols:
            for available in symbols:
                if priority.upper() in available.upper():
                    print(f"  ✅ {available}")
                    found_count += 1
                    break
        
        if found_count == 0:
            print("  📋 Primeros 3 disponibles:")
            for symbol in symbols[:3]:
                print(f"  📊 {symbol}")
    
    # Hora actual
    now = datetime.now(timezone.utc)
    day_name = now.strftime('%A')
    hour = now.hour
    
    print(f"\n🕒 Hora UTC: {now.strftime('%H:%M')} ({day_name})")
    
    # Estado del mercado simplificado
    is_weekend = now.weekday() >= 5
    if is_weekend:
        print("🔴 Fin de semana - Mercado Forex cerrado")
        print("💡 Prueba símbolos OTC o criptomonedas")
    else:
        print("🟢 Día hábil - Mercado puede estar abierto")

def check_results():
    """Ver últimos resultados"""
    try:
        response = requests.get(f"{API_BASE}/api/iq/order_results", timeout=5)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            if results:
                print(f"📊 Últimos {min(5, len(results))} resultados:")
                for result in results[-5:]:
                    status = result.get('status', 'unknown')
                    symbol = result.get('symbol', 'N/A')
                    action = result.get('action', 'N/A')
                    amount = result.get('amount', 'N/A')
                    
                    icon = "✅" if status == "executed" else "❌" if status == "failed" else "⏳"
                    print(f"   {icon} {symbol} {action} ${amount} - {status}")
                    
                    if status == "failed":
                        error = result.get('error', 'Unknown')
                        print(f"      💬 {error}")
                        
                        # Sugerencia basada en el error
                        if "cerrado" in error.lower() or "disponible" in error.lower():
                            print(f"      💡 Prueba con símbolos OTC o criptomonedas")
            else:
                print("📊 No hay resultados disponibles")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_balance():
    """Verificar balance"""
    try:
        response = requests.get(f"{API_BASE}/api/iq/balance", timeout=5)
        if response.status_code == 200:
            data = response.json()
            balance = data.get('balance', 0)
            currency = data.get('currency', 'USD')
            balance_type = data.get('balance_type', 'PRACTICE')
            
            print(f"💰 Balance: {balance} {currency} ({balance_type})")
            return balance
        else:
            print(f"❌ Error obteniendo balance: {response.status_code}")
            return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 0

if __name__ == "__main__":
    print("🧠 STC TRADING - SISTEMA INTELIGENTE")
    print("⚠️  Cuenta PRACTICE (dinero virtual)")
    print("🔍 Detección automática de símbolos disponibles")
    print("=" * 50)
    
    # Verificar balance y mercado
    balance = check_balance()
    show_market_info()
    
    if balance > 0:
        print(f"\n✅ Sistema listo para trading inteligente")
        
        while True:
            print(f"\n{'='*40}")
            print("🧠 TRADING INTELIGENTE")
            print("1. 📈 Orden CALL (detección automática)")
            print("2. 📉 Orden PUT (detección automática)")
            print("3. 🌍 Ver información de mercado")
            print("4. 💰 Ver balance")
            print("5. 📊 Ver resultados")
            print("6. ❌ Salir")
            
            choice = input("\n👉 Opción (1-6): ").strip()
            
            if choice == "1":
                success = send_smart_order("CALL")
                if success:
                    print("⏳ Orden enviada, procesándose...")
            elif choice == "2":
                success = send_smart_order("PUT")
                if success:
                    print("⏳ Orden enviada, procesándose...")
            elif choice == "3":
                show_market_info()
            elif choice == "4":
                check_balance()
            elif choice == "5":
                check_results()
            elif choice == "6":
                print("👋 ¡Trading finalizado!")
                break
            else:
                print("❌ Opción inválida")
    else:
        print("❌ No se pudo obtener el balance")
        print("💡 Verifica que el sistema IQ Option esté conectado")
