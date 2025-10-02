import requests
import json
import time

def test_system():
    print("🔍 DIAGNÓSTICO COMPLETO DEL SISTEMA STC\n")
    
    # Test 1: Salud del API
    print("1. 📡 Testeando API Backend...")
    try:
        response = requests.get("http://localhost:5002/health", timeout=5)
        print(f"   ✅ API Backend: {response.status_code}")
        print(f"   📊 Respuesta: {response.json()}")
    except Exception as e:
        print(f"   ❌ API Backend no responde: {e}")
        return
    
    # Test 2: Salud del Dashboard
    print("\n2. 🌐 Testeando Dashboard...")
    try:
        response = requests.get("http://localhost:5001/health", timeout=5)
        print(f"   ✅ Dashboard: {response.status_code}")
        print(f"   📊 Respuesta: {response.json()}")
    except Exception as e:
        print(f"   ❌ Dashboard no responde: {e}")
    
    # Test 3: Test de velas
    print("\n3. 📊 Testeando endpoint de velas...")
    try:
        response = requests.get("http://localhost:5002/api/iq/candles?symbol=EURUSD-OTC&limit=5")
        data = response.json()
        print(f"   ✅ Velas endpoint: {response.status_code}")
        print(f"   📈 Velas obtenidas: {len(data)}")
        if data:
            for i, candle in enumerate(data[-3:]):  # Últimas 3 velas
                time_str = time.strftime('%H:%M:%S', time.localtime(candle['time']/1000))
                print(f"      Vela {i+1}: {time_str} - O:{candle['open']:.5f} H:{candle['high']:.5f} L:{candle['low']:.5f} C:{candle['close']:.5f}")
    except Exception as e:
        print(f"   ❌ Error en velas: {e}")
    
    # Test 4: Test de login simulado
    print("\n4. 🔐 Testeando sistema de login...")
    try:
        login_data = {
            "email": "test@example.com",
            "password": "testpassword", 
            "balance_type": "PRACTICE"
        }
        response = requests.post("http://localhost:5002/api/iq/login", 
                               json=login_data, timeout=10)
        print(f"   ✅ Login endpoint: {response.status_code}")
        print(f"   📋 Respuesta login: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error en login: {e}")

if __name__ == "__main__":
    test_system()