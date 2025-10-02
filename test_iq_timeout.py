#!/usr/bin/env python3
"""
Test de conexión IQ Option con timeout
"""
import os
import time
import signal
import threading
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Conexión timeout")

def test_iq_connection():
    try:
        from iqoptionapi.stable_api import IQ_Option
        
        email = os.getenv("IQ_EMAIL", "")
        password = os.getenv("IQ_PASSWORD", "")
        balance_type = os.getenv("IQ_BALANCE_TYPE", "PRACTICE")
        
        print("🔌 Test de Conexión IQ Option (con timeout)")
        print("=" * 50)
        print(f"📧 Email: {email}")
        print(f"🔒 Password: {'*' * len(password)}")
        print(f"💰 Balance Type: {balance_type}")
        print("=" * 50)
        
        # Crear instancia de IQ_Option
        print("🔧 Creando instancia de IQ_Option...")
        iq = IQ_Option(email, password)
        
        # Configurar timeout de 15 segundos
        print("🌐 Intentando conectar (timeout: 15s)...")
        
        # Usar threading para timeout
        result = {"success": False, "reason": None, "error": None}
        
        def connect_thread():
            try:
                result["success"], result["reason"] = iq.connect()
            except Exception as e:
                result["error"] = e
        
        thread = threading.Thread(target=connect_thread)
        thread.daemon = True
        thread.start()
        thread.join(timeout=15)  # 15 segundos timeout
        
        if thread.is_alive():
            print("⏰ TIMEOUT - La conexión tardó más de 15 segundos")
            print("💡 Posibles causas:")
            print("   - Problemas de red/internet")
            print("   - IQ Option bloqueado en tu país/ISP")
            print("   - Firewall/proxy bloqueando la conexión")
            print("   - Servidores de IQ Option sobrecargados")
            return False
        
        if result["error"]:
            print(f"💥 EXCEPCIÓN durante conexión: {result['error']}")
            print(f"💥 Tipo: {type(result['error']).__name__}")
            return False
            
        if result["success"]:
            print("✅ CONEXIÓN EXITOSA!")
            print(f"📊 Cambiando a balance {balance_type}...")
            iq.change_balance(balance_type)
            time.sleep(2)
            
            # Obtener balance
            try:
                balance = iq.get_balance()
                print(f"💰 Balance actual: ${balance:.2f}")
            except Exception as e:
                print(f"⚠️ No se pudo obtener balance: {e}")
            
            # Verificar conexión
            try:
                connected = iq.check_connect()
                print(f"🔗 Estado de conexión: {connected}")
            except Exception as e:
                print(f"⚠️ No se pudo verificar conexión: {e}")
            
            print("🚪 Desconectando...")
            try:
                iq.api.close()
            except:
                pass
            print("✅ Test completado exitosamente")
            return True
            
        else:
            print(f"❌ ERROR DE CONEXIÓN: {result['reason']}")
            print(f"❌ Tipo de error: {type(result['reason'])}")
            
            # Analizar el error
            error_str = str(result['reason'])
            if "2159" in error_str:
                print("💡 ERROR 2159 - Posibles causas:")
                print("   - Credenciales incorrectas")
                print("   - Cuenta ya conectada en otro lugar")
                print("   - Restricciones geográficas")
                print("   - Problemas de red/firewall")
            elif "timeout" in error_str.lower():
                print("💡 ERROR TIMEOUT - Posibles causas:")
                print("   - Conexión de internet lenta")
                print("   - Servidores IQ Option lentos")
                print("   - Firewall/proxy bloqueando")
            
            return False
        
    except Exception as e:
        print(f"💥 EXCEPCIÓN GENERAL: {e}")
        print(f"💥 Tipo: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = test_iq_connection()
    print(f"\n🏁 Test finalizado - {'Éxito' if success else 'Falló'}")
