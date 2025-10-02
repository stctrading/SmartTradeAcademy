@echo off
echo 🚀 INICIANDO SISTEMA STC - VERSION FINAL 100% REAL
echo.

echo 🛑 Deteniendo servicios anteriores...
taskkill /f /im python.exe >nul 2>&1
timeout /t 3 /nobreak >nul

echo 🔄 Actualizando IQ Option API...
pip install iqoptionapi --upgrade

echo 🎯 Iniciando IQ Client Final...
start "STC IQ Client FINAL" cmd /k "python iq_client_final.py"

echo ⏳ Esperando inicialización del API (10 segundos)...
timeout /t 10 /nobreak >nul

echo 🌐 Iniciando Dashboard Web...
start "STC Dashboard" cmd /k "python dashboard_server.py"

echo.
echo ✅ SISTEMA 100% REAL INICIADO
echo 🌐 Dashboard: http://localhost:5001
echo 📊 API Health: http://localhost:5002/health
echo.
echo 🎯 AHORA USA TUS CREDENCIALES REALES EN EL DASHBOARD:
echo 📧 diegofelipeserranobecerra@gmail.com
echo 🔒 123456789p
echo.
pause