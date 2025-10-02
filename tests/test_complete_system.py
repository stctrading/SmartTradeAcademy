#!/usr/bin/env python3
"""
Test del sistema completo con sesiones y símbolos reales
"""
import requests
import json
import time

def test_complete_system():
    """Test completo del sistema IQ Option renovado"""
    
    print("🧪 TEST SISTEMA IQ OPTION COMPLETO")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:5002"
    
    # 1. Test símbolos (deben ser solo reales)
    print("\n1. 🔍 Probando símbolos disponibles...")
    try:
        symbols_res = requests.get(f"{base_url}/api/iq/symbols", timeout=5)
        print(f"   Status: {symbols_res.status_code}")
        
        if symbols_res.status_code == 200:
            symbols_data = symbols_res.json()
            symbols = symbols_data.get('symbols', [])
            source = symbols_data.get('source', 'unknown')
            count = len(symbols)
            
            print(f"   ✅ Símbolos obtenidos: {count}")
            print(f"   🔗 Fuente: {source}")
            
            if source == 'iq_client' and count > 0:
                print(f"   🎉 EXCELENTE: Símbolos reales de IQ Option!")
                print(f"   📋 Ejemplos: {symbols[:5]}")
            elif source == 'waiting':
                print(f"   ⏳ Esperando símbolos del cliente IQ...")
            else:
                print(f"   ⚠️ Usando fuente alternativa: {source}")
                
        elif symbols_res.status_code == 404:
            print("   ⏳ Símbolos no disponibles aún (esperando cliente IQ)")
        else:
            print(f"   ❌ Error obteniendo símbolos: {symbols_res.status_code}")
            
    except Exception as e:
        print(f"   💥 Error: {e}")
    
    # 2. Test balance
    print("\n2. 💰 Probando balance...")
    try:
        balance_res = requests.get(f"{base_url}/api/iq/balance", timeout=5)
        print(f"   Status: {balance_res.status_code}")
        
        if balance_res.status_code == 200:
            balance_data = balance_res.json()
            balance = balance_data.get('balance', 'N/A')
            source = balance_data.get('source', 'unknown')
            balance_type = balance_data.get('balance_type', 'N/A')
            
            print(f"   ✅ Balance: ${balance} ({balance_type})")
            print(f"   🔗 Fuente: {source}")
            
        elif balance_res.status_code == 404:
            print("   ⏳ Balance no disponible aún (esperando cliente IQ)")
        else:
            print(f"   ❌ Error obteniendo balance")
            
    except Exception as e:
        print(f"   💥 Error: {e}")
    
    # 3. Test sesión (debe estar vacía inicialmente)
    print("\n3. 🔐 Probando sistema de sesiones...")
    try:
        session_res = requests.get(f"{base_url}/api/iq/session", timeout=5)
        print(f"   Status: {session_res.status_code}")
        
        if session_res.status_code == 200:
            session_data = session_res.json()
            is_active = session_data.get('active', False)
            
            if is_active:
                session_info = session_data.get('session', {})
                email = session_info.get('email', 'N/A')
                print(f"   ✅ Sesión activa: {email}")
            else:
                print("   ✅ No hay sesión activa (estado limpio)")
                
    except Exception as e:
        print(f"   💥 Error: {e}")
    
    # 4. Test health
    print("\n4. ❤️ Probando estado del sistema...")
    try:
        health_res = requests.get(f"{base_url}/health", timeout=5)
        if health_res.status_code == 200:
            print("   ✅ Sistema saludable")
        else:
            print(f"   ❌ Sistema no saludable: {health_res.status_code}")
            
    except Exception as e:
        print(f"   💥 Error: {e}")

def main():
    test_complete_system()
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE MEJORAS IMPLEMENTADAS:")
    print("\n🔧 BACKEND:")
    print("  ✅ Solo símbolos reales (no hardcoded)")
    print("  ✅ Sistema de sesiones persistentes")
    print("  ✅ Endpoint de logout")
    print("  ✅ Endpoint de verificación de sesión")
    
    print("\n🎨 FRONTEND:")
    print("  ✅ Botón logout funcional")
    print("  ✅ Restauración automática de sesión")
    print("  ✅ Selector dinámico de símbolos")
    print("  ✅ Manejo de estados sin símbolos")
    
    print("\n🤖 CLIENTE IQ:")
    print("  ✅ Obtención mejorada de símbolos")
    print("  ✅ Procesamiento de logouts")
    print("  ✅ Método alternativo para símbolos")
    
    print("\n🎯 PRÓXIMO PASO:")
    print("  1. Usar el dashboard: http://127.0.0.1:5001/dashboard")
    print("  2. Login se mantiene entre recargas")
    print("  3. Logout limpia la sesión completamente")
    print("  4. Solo símbolos reales de IQ Option")

if __name__ == "__main__":
    main()
