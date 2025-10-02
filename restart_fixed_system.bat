@echo off
echo 🔄 REINICIANDO SISTEMA STC TRADING - VERSION CORREGIDA
echo.

echo 🛑 Deteniendo servicios anteriores...
taskkill /f /im python.exe >nul 2>&1
timeout /t 3 /nobreak >nul

echo 🚀 Iniciando API Backend Mejorado...
start "STC API Backend" cmd /k "python iq_client_fixed.py"

echo ⏳ Esperando inicialización del API...
timeout /t 5 /nobreak >nul

echo 🌐 Iniciando Dashboard Web...
start "STC Dashboard" cmd /k "python dashboard_server.py"

echo ⏳ Esperando inicialización del Dashboard...
timeout /t 4 /nobreak >nul

echo 🧪 Ejecutando diagnóstico del sistema...
python diagnostic.py

echo.
echo ✅ Sistema reiniciado correctamente
echo 🌐 Dashboard: http://localhost:5001
echo 📊 API Health: http://localhost:5002/health
echo.
pause