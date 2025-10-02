@echo off
echo Probando nueva ruta /trade...
echo.

curl -X POST http://localhost:5002/api/iq/trade -H "Content-Type: application/json" -d "{\"symbol\":\"EURUSD-OTC\",\"direction\":\"call\",\"amount\":1,\"expiration\":1}"

echo.
echo.
echo Probando ruta original /order...
curl -X POST http://localhost:5002/api/iq/order -H "Content-Type: application/json" -d "{\"action\":\"call\",\"asset\":\"EURUSD-OTC\",\"amount\":1,\"duration\":1}"

echo.
pause
