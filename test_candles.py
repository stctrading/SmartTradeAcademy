import requests
import time
import json

def test_candles_continuous():
    print("🧪 Probando actualización continua de velas...")
    
    for i in range(10):  # 10 pruebas
        try:
            response = requests.get("http://localhost:5002/api/iq/candles?symbol=EURUSD-OTC&limit=5")
            data = response.json()
            
            print(f"Prueba {i+1}: {len(data)} velas")
            if data:
                last_candle = data[-1]
                time_str = time.strftime('%H:%M:%S', time.localtime(last_candle['time']/1000))
                print(f"   Última vela: {time_str} - Close: {last_candle['close']}")
            
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(2)  # Esperar 2 segundos entre pruebas

if __name__ == "__main__":
    test_candles_continuous()