@echo off
echo ==========================================
echo     STC TRADING SYSTEM - INICIO COMPLETO
echo     Dashboard + API + IQ Client
echo ==========================================
echo.
echo 1. Cerrando procesos previos...
taskkill /f /im python.exe >nul 2>&1

echo 2. Esperando 3 segundos...
timeout /t 3 >nul

echo 3. Iniciando Dashboard MT5 (puerto 5001 HTTPS)...
start "STC-Dashboard" cmd /c "cd /d c:\STC_Trading_System && C:\STC_Trading_System\.venv311\Scripts\python.exe mt5_server.py"

echo 4. Esperando 5 segundos para que el dashboard inicie...
timeout /t 5 >nul

echo 5. Iniciando servidor Flask API (puerto 5002)...
start "STC-Flask-Server" cmd /c "cd /d c:\STC_Trading_System && C:\STC_Trading_System\.venv311\Scripts\python.exe iq_routes_redis_patch.py"

echo 6. Esperando 5 segundos para que el servidor Flask inicie...
timeout /t 5 >nul

echo 7. Iniciando cliente IQ Option...
start "STC-IQ-Client" cmd /c "cd /d c:\STC_Trading_System && C:\STC_Trading_System\.venv311\Scripts\python.exe iq_client.py"

echo 8. Esperando 5 segundos para que el cliente IQ inicie...
timeout /t 5 >nul

echo.
echo ==========================================
echo     SISTEMA INICIADO - PROBANDO...
echo ==========================================
echo.

echo 9. Verificando Dashboard (HTTPS puerto 5001)...
curl -k -s https://localhost:5001/api

echo.
echo 10. Verificando API Flask (HTTP puerto 5002)...
curl -s http://localhost:5002/health

echo.
echo 11. Probando balance IQ Option...
curl -s http://localhost:5002/api/iq/balance

echo.
echo.
echo ==========================================
echo     SISTEMA LISTO - ACCESO WEB
echo ==========================================
echo - Dashboard Principal: https://localhost:5001
echo - API Backend:         http://localhost:5002  
echo - Health Check:        http://localhost:5002/health
echo - Balance IQ:          http://localhost:5002/api/iq/balance
echo.
echo Las ventanas del sistema estan abiertas en segundo plano.
echo.
echo Presiona cualquier tecla para salir...
pause >nul
