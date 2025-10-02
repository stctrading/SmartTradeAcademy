#!/usr/bin/env python3
"""
Test rápido de orden OTC - STC Trading System
"""

import requests
import json

# Configuración
SERVER_BASE = 'http://localhost:5002'

def test_otc_order():
    """Prueba rápida de orden OTC"""
    print("🧪 TEST RÁPIDO ORDEN OTC")
    print("=" * 40)
    
    # 1. Verificar conexión
    try:
        response = requests.get(f'{SERVER_BASE}/api/iq/status', timeout=5)
        if response.status_code == 200:
            status = response.json()
            if status.get('connected'):
                print("✅ IQ Option conectado")
            else:
                print("❌ IQ Option NO conectado")
                return
        else:
            print("❌ Error verificando estado")
            return
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return
    
    # 2. Obtener balance inicial
    try:
        response = requests.get(f'{SERVER_BASE}/api/iq/balance', timeout=5)
        if response.status_code == 200:
            balance = response.json()
            print(f"💰 Balance inicial: ${balance:.2f}")
        else:
            print("❌ No se pudo obtener balance")
            return
    except Exception as e:
        print(f"❌ Error obteniendo balance: {e}")
        return
    
    # 3. Enviar orden de prueba OTC
    print("\n🚀 Enviando orden OTC de prueba...")
    print("   Símbolo: EURUSD-OTC")
    print("   Dirección: CALL")
    print("   Cantidad: $1")
    print("   Duración: 1 minuto")
    
    try:
        order_data = {
            'action': 'call',
            'amount': 1,
            'asset': 'EURUSD-OTC',
            'duration': 1
        }
        
        response = requests.post(
            f'{SERVER_BASE}/api/iq/order',
            json=order_data,
            timeout=10
        )
        
        print(f"\n📤 Respuesta del servidor:")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ ¡ORDEN ENVIADA EXITOSAMENTE!")
            print(f"   ID: {result.get('id', 'N/A')}")
            print(f"   Success: {result.get('success', 'N/A')}")
            print(f"   Mensaje: {result.get('message', 'N/A')}")
            print(json.dumps(result, indent=2))
        else:
            print("❌ ERROR EN LA ORDEN")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error enviando orden: {e}")

if __name__ == "__main__":
    test_otc_order()
