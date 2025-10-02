#!/usr/bin/env python3
"""
Trading Directo IQ Option
Interfaz simple para enviar órdenes directamente
"""
import requests
import json
from datetime import datetime

API_BASE = "http://localhost:5002"

def send_call_order():
    """Enviar orden CALL (BUY) rápida"""
    print("📈 ENVIANDO ORDEN CALL (BUY)")
    print("-" * 30)
    
    # Parámetros por defecto para trading rápido
    order = {
        "symbol": "EURUSD",
        "action": "BUY",
        "amount": 1.0,      # $1 mínimo
        "duration": 5,      # 5 minutos
        "option_type": "binary"
    }
    
    print(f"📊 Símbolo: {order['symbol']}")
    print(f"🎯 Dirección: CALL (BUY)")
    print(f"💰 Monto: ${order['amount']}")
    print(f"⏰ Duración: {order['duration']} min")
    
    try:
        response = requests.post(
            f"{API_BASE}/api/iq/order",
            json=order,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Orden CALL enviada!")
            print(f"🆔 ID: {result.get('order_id')}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def send_put_order():
    """Enviar orden PUT (SELL) rápida"""
    print("📉 ENVIANDO ORDEN PUT (SELL)")
    print("-" * 30)
    
    # Parámetros por defecto para trading rápido
    order = {
        "symbol": "EURUSD",
        "action": "SELL",
        "amount": 1.0,      # $1 mínimo
        "duration": 5,      # 5 minutos
        "option_type": "binary"
    }
    
    print(f"📊 Símbolo: {order['symbol']}")
    print(f"🎯 Dirección: PUT (SELL)")
    print(f"💰 Monto: ${order['amount']}")
    print(f"⏰ Duración: {order['duration']} min")
    
    try:
        response = requests.post(
            f"{API_BASE}/api/iq/order",
            json=order,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Orden PUT enviada!")
            print(f"🆔 ID: {result.get('order_id')}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_balance():
    """Verificar balance actual"""
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
            else:
                print("📊 No hay resultados disponibles")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 STC TRADING - ENVÍO DIRECTO DE ÓRDENES")
    print("⚠️  Cuenta PRACTICE (dinero virtual)")
    print("=" * 50)
    
    # Verificar balance inicial
    balance = check_balance()
    
    if balance > 0:
        print(f"\n✅ Sistema listo para trading")
        
        while True:
            print(f"\n{'='*30}")
            print("💹 MENÚ TRADING RÁPIDO")
            print("1. 📈 Orden CALL (BUY) - $1, 5min")
            print("2. 📉 Orden PUT (SELL) - $1, 5min")
            print("3. 💰 Ver balance")
            print("4. 📊 Ver resultados")
            print("5. ❌ Salir")
            
            choice = input("\n👉 Opción (1-5): ").strip()
            
            if choice == "1":
                success = send_call_order()
                if success:
                    print("⏳ Orden enviada, procesándose...")
            elif choice == "2":
                success = send_put_order()
                if success:
                    print("⏳ Orden enviada, procesándose...")
            elif choice == "3":
                check_balance()
            elif choice == "4":
                check_results()
            elif choice == "5":
                print("👋 ¡Trading finalizado!")
                break
            else:
                print("❌ Opción inválida")
    else:
        print("❌ No se pudo obtener el balance")
        print("💡 Verifica que el sistema IQ Option esté conectado")
