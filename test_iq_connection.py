#!/usr/bin/env python3
"""
Test simple de conexión a IQ Option
"""
import os
import time
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

try:
    from iqoptionapi.stable_api import IQ_Option
    
    email = os.getenv("IQ_EMAIL", "")
    password = os.getenv("IQ_PASSWORD", "")
    balance_type = os.getenv("IQ_BALANCE_TYPE", "PRACTICE")
    
    print("🔌 Test de Conexión IQ Option")
    print("=" * 50)
    print(f"📧 Email: {email}")
    print(f"🔒 Password: {'*' * len(password)}")
    print(f"💰 Balance Type: {balance_type}")
    print("=" * 50)
    
    # Crear instancia de IQ_Option
    print("🔧 Creando instancia de IQ_Option...")
    iq = IQ_Option(email, password)
    
    # Intentar conectar con timeout
    print("🌐 Intentando conectar...")
    print("⏳ Esto puede tomar hasta 30 segundos...")
    
    try:
        success, reason = iq.connect()
    except Exception as conn_error:
        print(f"💥 Error durante conexión: {conn_error}")
        print(f"💥 Tipo: {type(conn_error).__name__}")
        success = False
        reason = str(conn_error)
    
    if success:
        print("✅ CONEXIÓN EXITOSA!")
        print(f"📊 Cambiando a balance {balance_type}...")
        iq.change_balance(balance_type)
        time.sleep(2)
        
        # Obtener balance
        balance = iq.get_balance()
        print(f"💰 Balance actual: ${balance:.2f}")
        
        # Verificar conexión
        connected = iq.check_connect()
        print(f"🔗 Estado de conexión: {connected}")
        
        print("🚪 Desconectando...")
        iq.api.close()
        print("✅ Test completado exitosamente")
        
    else:
        print(f"❌ ERROR DE CONEXIÓN: {reason}")
        print(f"❌ Tipo de error: {type(reason)}")
        
        # Analizar el error
        if "2159" in str(reason):
            print("💡 ERROR 2159 - Posibles causas:")
            print("   - Credenciales incorrectas")
            print("   - Cuenta ya conectada en otro lugar")
            print("   - Restricciones geográficas")
            print("   - Problemas de red/firewall")
        
except Exception as e:
    print(f"💥 EXCEPCIÓN: {e}")
    print(f"💥 Tipo: {type(e).__name__}")

print("\n🏁 Test finalizado")
