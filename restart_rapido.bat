@echo off
title STC Trading - Reinicio Rapido
echo 🚀 Reiniciando STC Trading System...

taskkill /f /im python.exe >nul 2>&1
ping -n 3 127.0.0.1 >nul

start /MIN python iq_client.py
ping -n 2 127.0.0.1 >nul

start /MIN python iq_routes_redis_patch.py
ping -n 2 127.0.0.1 >nul

start /MIN python dashboard_server.py
ping -n 3 127.0.0.1 >nul

echo ✅ Servicios iniciados
netstat -an | findstr "5001\|5002"
echo.
echo 🌐 Dashboard: http://localhost:5001
echo 🔧 API: http://localhost:5002
pause
