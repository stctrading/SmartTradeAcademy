#!/usr/bin/env python3
"""
Test rápido del sistema OTC - STC Trading System
Prueba automática sin interacción del usuario
"""

import requests
import time
import json
from datetime import datetime

# Configuración
SERVER_BASE = 'http://localhost:5002'

def test_otc_system():
    """Test completo del sistema OTC"""
    print("="*60)
    print("🧪 TEST AUTOMÁTICO SISTEMA OTC")
    print("="*60)
    
    # 1. Verificar API Server
    print("\n1️⃣ Verificando API Server...")
    try:
        response = requests.get(f'{SERVER_BASE}/api/status', timeout=5)
        if response.status_code == 200:
            print("   ✅ API Server funcionando")
        else:
            print(f"   ❌ API Server error: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ No se puede conectar al API Server: {e}")
        print("   💡 Asegúrate de que el servidor esté corriendo: python iq_client.py")
        return False
    
    # 2. Verificar conexión IQ Option
    print("\n2️⃣ Verificando conexión IQ Option...")
    try:
        response = requests.get(f'{SERVER_BASE}/api/iq/status', timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('connected'):
                print("   ✅ IQ Option conectado")
            else:
                print("   ❌ IQ Option desconectado")
                return False
        else:
            print(f"   ❌ Error verificando IQ: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error verificando IQ: {e}")
        return False
    
    # 3. Obtener balance
    print("\n3️⃣ Obteniendo balance...")
    try:
        response = requests.get(f'{SERVER_BASE}/api/iq/balance', timeout=10)
        if response.status_code == 200:
            balance = response.json()
            print(f"   💰 Balance actual: ${balance:.2f}")
        else:
            print(f"   ❌ Error obteniendo balance: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error obteniendo balance: {e}")
        return False
    
    # 4. Verificar símbolos OTC
    print("\n4️⃣ Verificando símbolos OTC...")
    otc_symbols = ['EURUSD-OTC', 'GBPUSD-OTC', 'USDJPY-OTC', 'EURJPY-OTC']
    available_symbols = []
    
    for symbol in otc_symbols:
        try:
            response = requests.get(f'{SERVER_BASE}/api/iq/candles/{symbol}/M5', timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    last_candle = data[-1]
                    timestamp = datetime.fromtimestamp(last_candle['time']).strftime('%H:%M:%S')
                    print(f"   ✅ {symbol}: Vela {timestamp}, Precio: {last_candle['close']:.5f}")
                    available_symbols.append(symbol)
                else:
                    print(f"   ❌ {symbol}: Sin datos")
            else:
                print(f"   ❌ {symbol}: Error {response.status_code}")
        except Exception as e:
            print(f"   ❌ {symbol}: Error {e}")
    
    if not available_symbols:
        print("   ❌ No hay símbolos OTC disponibles")
        return False
    
    print(f"   ✅ Símbolos OTC activos: {len(available_symbols)}")
    
    # 5. Prueba de orden OTC
    print("\n5️⃣ Enviando orden de prueba OTC...")
    test_symbol = available_symbols[0]  # Usar el primer símbolo disponible
    
    try:
        order_data = {
            'action': 'call',
            'amount': 1,
            'asset': test_symbol,
            'duration': 1
        }
        
        print(f"   📤 Enviando: {test_symbol} CALL $1 por 1 minuto...")
        response = requests.post(
            f'{SERVER_BASE}/api/iq/order',
            json=order_data,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            order_id = result.get('id', 'N/A')
            print(f"   ✅ ¡ORDEN EXITOSA!")
            print(f"      🆔 ID: {order_id}")
            print(f"      📊 Símbolo: {test_symbol}")
            print(f"      📈 Dirección: CALL")
            print(f"      💰 Cantidad: $1")
            print(f"      ⏰ Duración: 1 minuto")
            
            # Esperar un poco para ver el resultado
            print("\n   ⏳ Esperando resultado de la orden...")
            time.sleep(65)  # Esperar 65 segundos para que expire la orden de 1 minuto
            
            # Verificar balance final
            try:
                response = requests.get(f'{SERVER_BASE}/api/iq/balance', timeout=10)
                if response.status_code == 200:
                    new_balance = response.json()
                    balance_change = new_balance - balance
                    print(f"   💰 Balance final: ${new_balance:.2f}")
                    if balance_change > 0:
                        print(f"   🎉 ¡GANASTE! +${balance_change:.2f}")
                    elif balance_change < 0:
                        print(f"   📉 Perdiste: ${balance_change:.2f}")
                    else:
                        print(f"   ⚖️ Sin cambio en balance")
            except:
                print("   ❓ No se pudo verificar balance final")
            
            return True
            
        else:
            error_msg = response.text
            print(f"   ❌ Error en orden: {response.status_code}")
            print(f"      📝 Respuesta: {error_msg}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error enviando orden: {e}")
        return False

def main():
    success = test_otc_system()
    
    print("\n" + "="*60)
    if success:
        print("🎉 ¡TEST COMPLETADO EXITOSAMENTE!")
        print("✅ El sistema OTC está funcionando correctamente")
        print("💡 Puedes usar 'python trading_otc.py' para trading interactivo")
    else:
        print("❌ TEST FALLÓ")
        print("🔧 Revisa los errores anteriores y corrige la configuración")
    print("="*60)

if __name__ == "__main__":
    main()
