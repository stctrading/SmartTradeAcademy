#!/usr/bin/env python3
"""
Test de órdenes IQ Option
Sistema para probar envío de órdenes de trading
"""
import os
import json
import time
import requests
from datetime import datetime

# Configuración
API_BASE_URL = "http://localhost:5002"

def test_order_system():
    """Prueba el sistema completo de órdenes"""
    print("🎯 TEST SISTEMA DE ÓRDENES IQ OPTION")
    print("=" * 50)
    
    # 1. Verificar que el backend esté activo
    print("1. 🔍 Verificando backend...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ Backend API activo")
        else:
            print(f"   ❌ Backend error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Backend no disponible: {e}")
        return False
    
    # 2. Verificar símbolos disponibles
    print("\n2. 📊 Verificando símbolos...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/iq/symbols", timeout=5)
        if response.status_code == 200:
            symbols_data = response.json()
            symbols = symbols_data.get('symbols', [])
            print(f"   ✅ {len(symbols)} símbolos disponibles")
            if symbols:
                print(f"   📋 Ejemplos: {[s.get('symbol', s) for s in symbols[:3]]}")
        else:
            print(f"   ⚠️ No se pudieron obtener símbolos: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️ Error obteniendo símbolos: {e}")
    
    # 3. Verificar balance
    print("\n3. 💰 Verificando balance...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/iq/balance", timeout=5)
        if response.status_code == 200:
            balance_data = response.json()
            balance = balance_data.get('balance', 0)
            currency = balance_data.get('currency', 'USD')
            balance_type = balance_data.get('balance_type', 'PRACTICE')
            print(f"   ✅ Balance: {balance} {currency} ({balance_type})")
        else:
            print(f"   ⚠️ No se pudo obtener balance: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️ Error obteniendo balance: {e}")
    
    # 4. Enviar orden de prueba
    print("\n4. 🚀 Enviando orden de prueba...")
    
    # Orden de prueba con parámetros conservadores
    test_order = {
        "symbol": "EURUSD",
        "action": "BUY",  # CALL
        "amount": 1.0,    # Mínimo $1
        "duration": 5,    # 5 minutos
        "option_type": "binary"
    }
    
    print(f"   📋 Orden: {test_order}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/iq/order", 
            json=test_order,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            order_id = result.get('order_id')
            print(f"   ✅ Orden enviada exitosamente")
            print(f"   🆔 ID: {order_id}")
            
            # Esperar un poco para que se procese
            print("\n5. ⏳ Esperando procesamiento (10 segundos)...")
            time.sleep(10)
            
            # 6. Verificar resultados
            print("\n6. 📊 Verificando resultados...")
            try:
                results_response = requests.get(f"{API_BASE_URL}/api/iq/order_results", timeout=5)
                if results_response.status_code == 200:
                    results_data = results_response.json()
                    results = results_data.get('results', [])
                    
                    if results:
                        print(f"   ✅ {len(results)} resultado(s) encontrado(s)")
                        for result in results[-3:]:  # Últimos 3 resultados
                            status = result.get('status', 'unknown')
                            symbol = result.get('symbol', 'N/A')
                            action = result.get('action', 'N/A')
                            amount = result.get('amount', 'N/A')
                            
                            if status == 'executed':
                                iq_order_id = result.get('iq_order_id', 'N/A')
                                print(f"   ✅ {symbol} {action} ${amount} -> Ejecutada (ID: {iq_order_id})")
                            elif status == 'failed':
                                error = result.get('error', 'Unknown error')
                                print(f"   ❌ {symbol} {action} ${amount} -> Falló: {error}")
                            else:
                                print(f"   ⏳ {symbol} {action} ${amount} -> Estado: {status}")
                    else:
                        print("   ⏳ No hay resultados aún (puede estar procesándose)")
                else:
                    print(f"   ⚠️ No se pudieron obtener resultados: {results_response.status_code}")
            except Exception as e:
                print(f"   ⚠️ Error obteniendo resultados: {e}")
                
            return True
            
        else:
            error_text = response.text
            print(f"   ❌ Error enviando orden: {response.status_code}")
            print(f"   📄 Respuesta: {error_text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error enviando orden: {e}")
        return False

def interactive_trading():
    """Modo interactivo para trading"""
    print("\n" + "="*50)
    print("🎮 MODO TRADING INTERACTIVO")
    print("="*50)
    
    while True:
        print("\n📋 Opciones:")
        print("1. 📈 Enviar orden CALL (BUY)")
        print("2. 📉 Enviar orden PUT (SELL)")
        print("3. 💰 Ver balance")
        print("4. 📊 Ver resultados de órdenes")
        print("5. ❌ Salir")
        
        choice = input("\n👉 Elige una opción (1-5): ").strip()
        
        if choice == "1":
            send_order("CALL")
        elif choice == "2":
            send_order("PUT")
        elif choice == "3":
            check_balance()
        elif choice == "4":
            check_order_results()
        elif choice == "5":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida")

def send_order(direction):
    """Enviar orden de trading"""
    print(f"\n🚀 Enviando orden {direction}")
    
    # Obtener parámetros del usuario
    symbol = input("📊 Símbolo (EURUSD): ").strip().upper() or "EURUSD"
    
    try:
        amount = float(input("💰 Monto ($1-1000): ").strip() or "1")
        if amount < 1 or amount > 1000:
            print("❌ Monto debe estar entre $1 y $1000")
            return
    except ValueError:
        print("❌ Monto inválido")
        return
        
    try:
        duration = int(input("⏰ Duración en minutos (1-60): ").strip() or "5")
        if duration < 1 or duration > 60:
            print("❌ Duración debe estar entre 1 y 60 minutos")
            return
    except ValueError:
        print("❌ Duración inválida")
        return
    
    # Preparar orden
    order = {
        "symbol": symbol,
        "action": "BUY" if direction == "CALL" else "SELL",
        "amount": amount,
        "duration": duration,
        "option_type": "binary"
    }
    
    print(f"\n📋 Orden preparada:")
    print(f"   📊 Símbolo: {symbol}")
    print(f"   🎯 Dirección: {direction}")
    print(f"   💰 Monto: ${amount}")
    print(f"   ⏰ Duración: {duration} minutos")
    
    confirm = input("\n❓ ¿Confirmar orden? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Orden cancelada")
        return
    
    # Enviar orden
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/iq/order",
            json=order,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            order_id = result.get('order_id')
            print(f"✅ Orden enviada exitosamente!")
            print(f"🆔 ID de orden: {order_id}")
            print("⏳ La orden se procesará en unos segundos...")
        else:
            print(f"❌ Error enviando orden: {response.status_code}")
            print(f"📄 Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error enviando orden: {e}")

def check_balance():
    """Verificar balance actual"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/iq/balance", timeout=5)
        if response.status_code == 200:
            balance_data = response.json()
            balance = balance_data.get('balance', 0)
            currency = balance_data.get('currency', 'USD')
            balance_type = balance_data.get('balance_type', 'PRACTICE')
            source = balance_data.get('source', 'unknown')
            
            print(f"\n💰 BALANCE ACTUAL")
            print(f"   💵 Monto: {balance} {currency}")
            print(f"   🏦 Tipo: {balance_type}")
            print(f"   📡 Fuente: {source}")
        else:
            print(f"❌ Error obteniendo balance: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_order_results():
    """Verificar resultados de órdenes"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/iq/order_results", timeout=5)
        if response.status_code == 200:
            results_data = response.json()
            results = results_data.get('results', [])
            
            if results:
                print(f"\n📊 RESULTADOS DE ÓRDENES ({len(results)} total)")
                print("-" * 50)
                for i, result in enumerate(results[-10:], 1):  # Últimos 10
                    status = result.get('status', 'unknown')
                    symbol = result.get('symbol', 'N/A')
                    action = result.get('action', 'N/A')
                    amount = result.get('amount', 'N/A')
                    timestamp = result.get('executed_at', result.get('failed_at', 0))
                    
                    time_str = datetime.fromtimestamp(timestamp).strftime("%H:%M:%S") if timestamp else "N/A"
                    
                    status_icon = "✅" if status == "executed" else "❌" if status == "failed" else "⏳"
                    print(f"{i:2}. {status_icon} {symbol} {action} ${amount} - {status} ({time_str})")
                    
                    if status == "failed":
                        error = result.get('error', 'Unknown error')
                        print(f"     💬 Error: {error}")
            else:
                print("\n📊 No hay resultados de órdenes disponibles")
        else:
            print(f"❌ Error obteniendo resultados: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🎯 STC TRADING SYSTEM - TEST DE ÓRDENES")
    print("⚠️  CUENTA: PRACTICE (Dinero virtual)")
    print("=" * 50)
    
    # Ejecutar test automático primero
    success = test_order_system()
    
    if success:
        print("\n✅ Test automático completado exitosamente")
        
        # Ofrecer modo interactivo
        interactive_mode = input("\n❓ ¿Quieres usar el modo interactivo? (y/N): ").strip().lower()
        if interactive_mode == 'y':
            interactive_trading()
    else:
        print("\n❌ Test automático falló")
        print("💡 Asegúrate de que:")
        print("   - El backend esté corriendo en puerto 5002")
        print("   - El cliente IQ Option esté conectado")
        print("   - Las credenciales en .env sean correctas")
