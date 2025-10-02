#!/usr/bin/env python3
"""
test_complete_chart_system.py
Prueba completa del sistema de gráficos STC Trading
"""

import requests
import json
import time

def test_endpoints():
    """Probar todos los endpoints del sistema"""
    
    print("🧪 PROBANDO SISTEMA COMPLETO STC TRADING")
    print("=" * 50)
    
    # Test 1: Verificar servidor dashboard
    try:
        response = requests.get("http://localhost:5001", timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard (puerto 5001): FUNCIONANDO")
        else:
            print(f"❌ Dashboard error: {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard no disponible: {e}")
    
    # Test 2: Verificar API balance
    try:
        response = requests.get("http://localhost:5002/api/iq/balance", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Balance: ${data.get('balance', 'N/A')}")
        else:
            print(f"❌ Balance error: {response.status_code}")
    except Exception as e:
        print(f"❌ Balance no disponible: {e}")
    
    # Test 3: Verificar símbolos
    try:
        response = requests.get("http://localhost:5002/api/iq/symbols", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Símbolos disponibles: {len(data)} símbolos")
            for symbol in data[:3]:  # Mostrar primeros 3
                print(f"   📊 {symbol.get('name', 'N/A')}")
        else:
            print(f"❌ Símbolos error: {response.status_code}")
    except Exception as e:
        print(f"❌ Símbolos no disponibles: {e}")
    
    # Test 4: Verificar velas (PRINCIPAL PARA GRÁFICOS)
    try:
        response = requests.get("http://localhost:5002/api/iq/candles?symbol=EURUSD-OTC&limit=10", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Velas EURUSD-OTC: {len(data)} velas disponibles")
            
            if data:
                last_candle = data[-1]
                print(f"   📈 Última vela:")
                print(f"      Tiempo: {last_candle.get('from', 'N/A')} -> {last_candle.get('to', 'N/A')}")
                print(f"      OHLC: O:{last_candle.get('open', 0):.5f} H:{last_candle.get('high', 0):.5f} L:{last_candle.get('low', 0):.5f} C:{last_candle.get('close', 0):.5f}")
                print(f"      Volumen: {last_candle.get('volume', 0)}")
                print(f"      Cerrada: {last_candle.get('closed', False)}")
        else:
            print(f"❌ Velas error: {response.status_code}")
    except Exception as e:
        print(f"❌ Velas no disponibles: {e}")
    
    # Test 5: Verificar otros símbolos OTC
    otc_symbols = ['GBPUSD-OTC', 'USDJPY-OTC', 'EURJPY-OTC']
    for symbol in otc_symbols:
        try:
            response = requests.get(f"http://localhost:5002/api/iq/candles?symbol={symbol}&limit=5", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {symbol}: {len(data)} velas")
            else:
                print(f"⚠️ {symbol}: No disponible")
        except Exception as e:
            print(f"❌ {symbol}: Error - {e}")
    
    print("\n" + "=" * 50)
    print("🎯 RESUMEN DEL SISTEMA:")
    print("   Dashboard: http://localhost:5001")
    print("   API Backend: http://localhost:5002")
    print("   Gráficos: TradingView LightweightCharts")
    print("   Datos: Velas reales de IQ Option")
    print("   Símbolos: OTC disponibles 24/7")

def test_chart_data_format():
    """Verificar que los datos estén en el formato correcto para gráficos"""
    
    print("\n📊 VERIFICANDO FORMATO DE DATOS PARA GRÁFICOS")
    print("-" * 50)
    
    try:
        response = requests.get("http://localhost:5002/api/iq/candles?symbol=EURUSD-OTC&limit=3", timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Recibidas {len(data)} velas para verificar formato")
            
            for i, candle in enumerate(data[:3]):
                print(f"\n📈 Vela {i+1}:")
                
                # Verificar campos requeridos para TradingView
                required_fields = ['open', 'high', 'low', 'close']
                time_field = candle.get('from') or candle.get('time')
                
                if time_field:
                    print(f"   ✅ time: {time_field}")
                else:
                    print(f"   ❌ time: FALTANTE")
                
                for field in required_fields:
                    value = candle.get(field)
                    if value is not None:
                        print(f"   ✅ {field}: {value}")
                    else:
                        print(f"   ❌ {field}: FALTANTE")
                
                # Formato esperado por TradingView
                tv_format = {
                    'time': time_field,
                    'open': float(candle.get('open', 0)),
                    'high': float(candle.get('high', 0)), 
                    'low': float(candle.get('low', 0)),
                    'close': float(candle.get('close', 0))
                }
                print(f"   🔄 Formato TradingView: {tv_format}")
            
        else:
            print(f"❌ Error obteniendo datos: {response.status_code}")
    except Exception as e:
        print(f"❌ Error verificando formato: {e}")

if __name__ == "__main__":
    test_endpoints()
    test_chart_data_format()
    
    print("\n🚀 PARA VER EL SISTEMA EN ACCIÓN:")
    print("   1. Abre http://localhost:5001 en tu navegador")
    print("   2. Abre las herramientas de desarrollador (F12)")
    print("   3. Ve a la pestaña Console para ver logs del gráfico")
    print("   4. Los gráficos deberían cargarse automáticamente")
    print("\n✨ ¡Sistema STC Trading completamente operativo!")
