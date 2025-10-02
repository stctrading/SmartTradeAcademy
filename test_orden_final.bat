@echo off
echo ======================================
echo   PRUEBA FINAL ORDEN OTC
echo ======================================
echo.
echo Enviando orden OTC CALL EURUSD-OTC $1 por 1 minuto...
echo.

curl -X POST http://localhost:5002/api/iq/order ^
  -H "Content-Type: application/json" ^
  -d "{\"action\": \"call\", \"symbol\": \"EURUSD-OTC\", \"amount\": 1, \"duration\": 1}"

echo.
echo.
echo ======================================
echo   RESULTADO ARRIBA ↑
echo ======================================
echo.
echo Presiona cualquier tecla para continuar...
pause >nul
