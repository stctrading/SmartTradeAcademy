@echo off
echo ==========================================
echo     STC TRADING SYSTEM - INICIO COMPLETO
echo ==========================================
echo.
echo 1. Cerrando procesos previos...
taskkill /f /im python.exe >nul 2>&1

echo 2. Esperando 3 segundos...
timeout /t 3 >nul

echo 3. Iniciando servidor Flask (puerto 5002)...
start "STC-Flask-Server" cmd /c "cd /d c:\STC_Trading_System && C:\STC_Trading_System\.venv311\Scripts\python.exe iq_routes_redis_patch.py"

echo 4. Esperando 5 segundos para que el servidor Flask inicie...
timeout /t 5 >nul

echo 5. Iniciando cliente IQ Option...
start "STC-IQ-Client" cmd /c "cd /d c:\STC_Trading_System && C:\STC_Trading_System\.venv311\Scripts\python.exe iq_client.py"

echo 6. Esperando 5 segundos para que el cliente IQ inicie...
timeout /t 5 >nul

echo.
echo ==========================================
echo     SISTEMA INICIADO - PROBANDO...
echo ==========================================
echo.

echo 7. Verificando servidor Flask...
curl -s http://localhost:5002/health

echo.
echo 8. Probando orden OTC automatica...
curl -X POST http://localhost:5002/api/iq/order ^
  -H "Content-Type: application/json" ^
  -d "{\"action\": \"call\", \"amount\": 1, \"asset\": \"EURUSD-OTC\", \"duration\": 1}"

echo.
echo.
echo ==========================================
echo     SISTEMA LISTO PARA TRADING OTC
echo ==========================================
echo - Servidor Flask: http://localhost:5002
echo - Dashboard: http://localhost:5001 (si esta corriendo)
echo - Logs en las ventanas separadas
echo.
echo Presiona cualquier tecla para salir...
pause >nul
