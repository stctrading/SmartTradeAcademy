from iqoptionapi.stable_api import IQ_Option
import time
import json

def test_iq_detailed():
    print("🧪 TEST DETALLADO IQ OPTION")
    print("=" * 60)
    
    email = "diegofelipeserranobecerra@gmail.com"
    password = "123456789p"
    
    print(f"📧 Email: {email}")
    print(f"🔒 Password: {'*' * len(password)}")
    
    try:
        print("\n1. 🔌 Creando instancia API...")
        api = IQ_Option(email, password)
        
        print("2. ⏳ Intentando conexión (puede tomar 30 segundos)...")
        
        # Conexión con timeout extendido
        check, reason = api.connect()
        
        print(f"3. 📊 Resultado: {check}")
        print(f"4. 🎯 Razón: {reason}")
        
        if check:
            print("✅ ✅ ✅ CONEXIÓN EXITOSA!")
            
            # Obtener balance
            balance = api.get_balance()
            print(f"💰 Balance: ${balance}")
            
            # Cambiar a práctica
            print("🔄 Cambiando a cuenta PRACTICE...")
            practice_result = api.change_balance("PRACTICE")
            print(f"✅ Resultado cambio balance: {practice_result}")
            
            # Probar datos reales
            print("\n📊 Probando datos de mercado...")
            try:
                candles = api.get_candles("EURUSD-OTC", 300, 5, time.time())
                if candles:
                    print(f"✅ Velas obtenidas: {len(candles)}")
                    for i, candle in enumerate(candles[-3:]):
                        time_str = time.strftime('%H:%M:%S', time.localtime(candle['from']))
                        print(f"   Vela {i+1}: {time_str} - C: {candle['close']}")
                else:
                    print("❌ No se pudieron obtener velas")
            except Exception as e:
                print(f"❌ Error obteniendo velas: {e}")
                
        else:
            print("\n❌ ❌ ❌ FALLO EN CONEXIÓN")
            print("\n🔍 SOLUCIONES AVANZADAS:")
            print("1. 🔄 Reintentar con timeout mayor")
            print("2. 🌐 Usar VPN (Europa/USA)")
            print("3. 📱 Verificar cuenta en app móvil")
            print("4. 🚀 Actualizar iqoptionapi")
            print("5. 🔑 Verificar si la cuenta requiere 2FA")
            
    except Exception as e:
        print(f"💥 Error inesperado: {e}")
        print(f"📋 Tipo de error: {type(e).__name__}")

if __name__ == "__main__":
    test_iq_detailed()
    