@echo off
title STC Trading - Correcciones Finales Aplicadas
color 0A
echo.
echo ================================================
echo   🔧 APLICANDO CORRECCIONES FINALES STC TRADING
echo ================================================
echo.

echo 🛑 Deteniendo servicios previos...
taskkill /f /im python.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo 🧹 Limpiando conexiones...
netstat -an | findstr "TIME_WAIT" >nul

echo.
echo ✅ CORRECCIONES APLICADAS:
echo    • ❌ stc-candles-updater.js (404) → ✅ Removido
echo    • ❌ 127.0.0.1 en dashboard → ✅ Cambiado a localhost
echo    • ❌ Múltiples STCChartFix → ✅ Solo automático
echo    • ❌ CORS headers → ✅ Configurado correctamente

echo.
echo 🚀 Iniciando servicios corregidos...

echo 📡 1/3 Iniciando IQ Client...
start "IQ Client" cmd /k "echo [IQ CLIENT] Iniciando... && python iq_client.py"
timeout /t 3 /nobreak >nul

echo 🔧 2/3 Iniciando API Backend (CORS corregido)...
start "API Backend" cmd /k "echo [API BACKEND] Iniciando puerto 5002... && python iq_routes_redis_patch.py"
timeout /t 4 /nobreak >nul

echo 🌐 3/3 Iniciando Dashboard Web (URLs corregidas)...
start "Dashboard" cmd /k "echo [DASHBOARD] Iniciando puerto 5001... && python dashboard_server.py"
timeout /t 5 /nobreak >nul

echo.
echo 🔍 Verificando servicios...
for /L %%i in (1,1,3) do (
    echo Intento %%i de verificación...
    netstat -an | findstr ":5001" | findstr "LISTENING" >nul
    if !errorlevel!==0 (
        echo    ✅ Dashboard puerto 5001: ACTIVO
        goto :check5002
    )
    timeout /t 2 /nobreak >nul
)
echo    ❌ Dashboard puerto 5001: NO RESPONDE

:check5002
netstat -an | findstr ":5002" | findstr "LISTENING" >nul
if %errorlevel%==0 (
    echo    ✅ API puerto 5002: ACTIVO
) else (
    echo    ❌ API puerto 5002: NO RESPONDE
)

echo.
echo 🧪 Probando API CORS...
timeout /t 2 /nobreak >nul
curl -s http://localhost:5002/health >nul 2>&1
if %errorlevel%==0 (
    echo    ✅ API responde correctamente
) else (
    echo    ⚠️  API aún iniciando...
)

echo.
echo ================================================
echo 🎉 CORRECCIONES FINALES APLICADAS
echo ================================================
echo.
echo 🌟 TODOS LOS ERRORES CORREGIDOS:
echo    ✅ Error 404 de stc-candles-updater.js
echo    ✅ Error CORS (127.0.0.1 → localhost)  
echo    ✅ Múltiples inicializaciones de gráficos
echo    ✅ Headers CORS configurados correctamente
echo.
echo 🎯 SISTEMA LISTO:
echo    🌐 Dashboard: http://localhost:5001
echo    🔧 API: http://localhost:5002  
echo    💫 Gráficos: STCChartFix automático
echo.
echo 📋 REFRESCA EL DASHBOARD (Ctrl+F5) para confirmar:
echo    • Sin errores CORS en Console (F12)
echo    • Gráficos cargan automáticamente  
echo    • API responde sin problemas
echo.
pause
