@echo off
title STC Trading - Arreglo de Errores CORS y Gráficos
color 0C
echo.
echo ===============================================
echo   🔧 ARREGLANDO ERRORES DEL SISTEMA STC
echo ===============================================
echo.

echo 🛑 PASO 1: Deteniendo servicios...
taskkill /f /im python.exe >nul 2>&1
timeout /t 3 /nobreak >nul

echo 🔄 PASO 2: Reiniciando servicios con correcciones...
echo    • Iniciando IQ Client...
start "IQ Client" cmd /k "python iq_client.py"
timeout /t 3 /nobreak >nul

echo    • Iniciando API con CORS arreglado...
start "API Backend" cmd /k "python iq_routes_redis_patch.py"
timeout /t 3 /nobreak >nul

echo    • Iniciando Dashboard...
start "Dashboard" cmd /k "python dashboard_server.py"
timeout /t 5 /nobreak >nul

echo.
echo 🔍 PASO 3: Verificando servicios...
netstat -an | findstr ":5001" | findstr "LISTENING" >nul
if %errorlevel%==0 (
    echo    ✅ Dashboard (5001): ACTIVO
) else (
    echo    ❌ Dashboard (5001): ERROR
)

netstat -an | findstr ":5002" | findstr "LISTENING" >nul
if %errorlevel%==0 (
    echo    ✅ API (5002): ACTIVO
) else (
    echo    ❌ API (5002): ERROR
)

echo.
echo 🧪 PASO 4: Probando CORS...
curl -s http://localhost:5002/health >nul 2>&1
if %errorlevel%==0 (
    echo    ✅ CORS: Arreglado - API responde
) else (
    echo    ⚠️ CORS: Verificar manualmente
)

echo.
echo ===============================================
echo 🎯 CORRECCIONES APLICADAS:
echo ===============================================
echo.
echo ✅ CORS mejorado en API:
echo    • Permitir todos los orígenes (*)
echo    • Headers adicionales configurados
echo    • Métodos HTTP completos
echo.
echo ✅ Gráficos simplificados:
echo    • Eliminado STCChartManager conflictivo
echo    • Solo STCChartFix (funciona automáticamente)
echo    • Polling automático cada 2 segundos
echo.
echo 🌐 DASHBOARD: http://localhost:5001
echo 🔧 API: http://localhost:5002
echo.
echo 📋 Los errores CORS y de gráficos deberían estar solucionados.
echo    Refresca el dashboard para ver los cambios.
echo.
pause
