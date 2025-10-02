@echo off
title Inicio Manual STC Trading
echo 🚀 Iniciando servicios manualmente...

echo.
echo 🔧 Iniciando API Backend...
start "API Backend - Puerto 5002" python iq_routes_redis_patch.py
timeout /t 5 /nobreak >nul

echo 🌐 Iniciando Dashboard...
start "Dashboard - Puerto 5001" python dashboard_server.py
timeout /t 3 /nobreak >nul

echo 📡 Iniciando IQ Client...
start "IQ Client" python iq_client.py
timeout /t 2 /nobreak >nul

echo.
echo ✅ Servicios iniciados
echo.
echo 🔍 Verificando puertos...
netstat -an | findstr ":5001\|:5002" | findstr "LISTEN"

echo.
echo 🧪 Probando API...
timeout /t 2 /nobreak >nul
curl http://localhost:5002/health

echo.
echo 📊 URLs del sistema:
echo Dashboard: http://localhost:5001  
echo API: http://localhost:5002
echo Health: http://localhost:5002/health
echo.
pause
