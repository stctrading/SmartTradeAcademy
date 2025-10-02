#!/usr/bin/env python3
"""
Trading OTC - Símbolos disponibles 24/7
Usa símbolos OTC que están siempre disponibles
"""
import requests
from datetime import datetime

API_BASE = "http://localhost:5002"

# Símbolos OTC principales (disponibles 24/7)
OTC_SYMBOLS = [
    "EURUSD-OTC",
    "GBPUSD-OTC", 
    "USDJPY-OTC",
    "EURJPY-OTC",
    "AUDUSD-OTC",
    "USDCAD-OTC"
]

def send_otc_order(symbol, direction):
    """Enviar orden con símbolo OTC específico"""
    print(f"🎯 ORDEN OTC {direction}")
    print("-" * 30)
    
    order = {
        "symbol": symbol,
        "action": "BUY" if direction == "CALL" else "SELL",
        "amount": 1.0,      # $1 mínimo
        "duration": 5,      # 5 minutos
        "option_type": "binary"
    }
    
    print(f"📊 Símbolo: {symbol}")
    print(f"🎯 Dirección: {direction}")
    print(f"💰 Monto: ${order['amount']}")
    print(f"⏰ Duración: {order['duration']} min")
    print(f"🏷️  Tipo: OTC (24/7 disponible)")
    
    try:
        response = requests.post(
            f"{API_BASE}/api/iq/order",
            json=order,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Orden OTC {direction} enviada!")
            print(f"🆔 ID: {result.get('order_id')}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def quick_call_otc():
    """Orden CALL rápida con EURUSD-OTC"""
    return send_otc_order("EURUSD-OTC", "CALL")

def quick_put_otc():
    """Orden PUT rápida con EURUSD-OTC"""
    return send_otc_order("EURUSD-OTC", "PUT")

def select_symbol_and_trade(direction):
    """Seleccionar símbolo OTC y hacer trading"""
    print(f"\n📊 SÍMBOLOS OTC DISPONIBLES:")
    for i, symbol in enumerate(OTC_SYMBOLS, 1):
        print(f"  {i}. {symbol}")
    
    try:
        choice = int(input(f"\n👉 Elige símbolo (1-{len(OTC_SYMBOLS)}) o 0 para EURUSD-OTC: ").strip())
        
        if choice == 0 or choice < 1 or choice > len(OTC_SYMBOLS):
            symbol = "EURUSD-OTC"
        else:
            symbol = OTC_SYMBOLS[choice - 1]
            
        return send_otc_order(symbol, direction)
        
    except ValueError:
        print("❌ Opción inválida, usando EURUSD-OTC")
        return send_otc_order("EURUSD-OTC", direction)

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
                    elif status == "executed":
                        iq_order_id = result.get('iq_order_id', 'N/A')
                        print(f"      🎯 ID IQ: {iq_order_id}")
                        
            else:
                print("📊 No hay resultados disponibles")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def show_otc_info():
    """Mostrar información sobre OTC"""
    print("🏷️  INFORMACIÓN SÍMBOLOS OTC")
    print("-" * 30)
    print("✅ Ventajas de OTC:")
    print("   • Disponibles 24/7")
    print("   • No dependen de horarios de mercado")
    print("   • Siempre activos para trading")
    print("   • Ideales para práctica")
    print()
    print("📊 Símbolos OTC configurados:")
    for symbol in OTC_SYMBOLS:
        base_pair = symbol.replace('-OTC', '')
        print(f"   • {symbol} ({base_pair})")
    print()
    now = datetime.now()
    print(f"🕒 Hora actual: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("🟢 Estado: OTC siempre disponible")

if __name__ == "__main__":
    print("🏷️  STC TRADING - MODO OTC 24/7")
    print("⚠️  Cuenta PRACTICE (dinero virtual)")
    print("🌍 Símbolos OTC disponibles las 24 horas")
    print("=" * 50)
    
    # Mostrar info OTC
    show_otc_info()
    
    # Verificar balance
    balance = check_balance()
    
    if balance > 0:
        print(f"\n✅ Sistema OTC listo para trading")
        
        while True:
            print(f"\n{'='*40}")
            print("🏷️  TRADING OTC 24/7")
            print("1. 📈 CALL rápido (EURUSD-OTC)")
            print("2. 📉 PUT rápido (EURUSD-OTC)")
            print("3. 🎯 CALL personalizado (elegir símbolo)")
            print("4. 🎯 PUT personalizado (elegir símbolo)")
            print("5. 💰 Ver balance")
            print("6. 📊 Ver resultados")
            print("7. 🏷️  Info OTC")
            print("8. ❌ Salir")
            
            choice = input("\n👉 Opción (1-8): ").strip()
            
            if choice == "1":
                success = quick_call_otc()
                if success:
                    print("⏳ Orden CALL OTC enviada, procesándose...")
            elif choice == "2":
                success = quick_put_otc()
                if success:
                    print("⏳ Orden PUT OTC enviada, procesándose...")
            elif choice == "3":
                success = select_symbol_and_trade("CALL")
                if success:
                    print("⏳ Orden CALL personalizada enviada, procesándose...")
            elif choice == "4":
                success = select_symbol_and_trade("PUT")
                if success:
                    print("⏳ Orden PUT personalizada enviada, procesándose...")
            elif choice == "5":
                check_balance()
            elif choice == "6":
                check_results()
            elif choice == "7":
                show_otc_info()
            elif choice == "8":
                print("👋 ¡Trading OTC finalizado!")
                break
            else:
                print("❌ Opción inválida")
    else:
        print("❌ No se pudo obtener el balance")
        print("💡 Verifica que el sistema IQ Option esté conectado")
