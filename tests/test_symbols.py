#!/usr/bin/env python3
"""
Test del endpoint de símbolos disponibles
"""
import requests
import json

def test_symbols_endpoint():
    """Prueba el endpoint de símbolos disponibles"""
    
    print("🧪 TEST ENDPOINT DE SÍMBOLOS")
    print("=" * 40)
    
    try:
        url = "http://127.0.0.1:5002/api/iq/symbols"
        print(f"🔗 URL: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            symbols = data.get('symbols', [])
            count = data.get('count', 0)
            source = data.get('source', 'unknown')
            
            print(f"✅ ÉXITO!")
            print(f"📊 Total símbolos: {count}")
            print(f"🔗 Fuente: {source}")
            print(f"📋 Primeros 10 símbolos:")
            
            for i, symbol in enumerate(symbols[:10], 1):
                print(f"   {i:2d}. {symbol}")
            
            if len(symbols) > 10:
                print(f"   ... y {len(symbols) - 10} más")
                
            return True
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📝 Respuesta: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"💥 Excepción: {e}")
        return False

def main():
    success = test_symbols_endpoint()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 ENDPOINT DE SÍMBOLOS FUNCIONANDO!")
        print("\n💡 Instrucciones:")
        print("1. Los símbolos se cargan automáticamente al conectar")
        print("2. Usa el botón 🔄 para refrescar la lista")
        print("3. Selecciona un símbolo del dropdown")
        print("4. El dashboard obtendrá velas para ese símbolo")
    else:
        print("❌ ENDPOINT REQUIERE ATENCIÓN")
        print("- Verificar que iq_routes_redis_patch.py esté corriendo")
        print("- Verificar que iq_client.py esté enviando símbolos")

if __name__ == "__main__":
    main()
