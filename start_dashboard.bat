@echo off
echo ==========================================
echo     STC DASHBOARD - INICIO SIMPLE
echo ==========================================
echo.
echo 1. Cerrando procesos previos de dashboard...
taskkill /f /im python.exe /fi "WINDOWTITLE eq STC-Dashboard" >nul 2>&1

echo 2. Iniciando Dashboard HTTP (puerto 5001)...
start "STC-Dashboard" cmd /c "cd /d c:\STC_Trading_System && C:\STC_Trading_System\.venv311\Scripts\python.exe dashboard_server.py"

echo 3. Esperando 3 segundos...
timeout /t 3 >nul

echo 4. Probando acceso al dashboard...
curl -s http://localhost:5001/health

echo.
echo ==========================================
echo     DASHBOARD LISTO
echo ==========================================
echo - Acceso: http://localhost:5001
echo - Health: http://localhost:5001/health
echo - API:    http://localhost:5001/api
echo.
pause
