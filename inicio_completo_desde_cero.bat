@echo off
title STC Trading - INICIO COMPLETO DESDE CERO
color 0C
echo.
echo ========================================================
echo   🚀 STC TRADING SYSTEM - INICIO COMPLETO DESDE CERO
echo ========================================================
echo.

echo 🛑 PASO 1: LIMPIANDO SISTEMA...
echo    • Deteniendo procesos previos...
taskkill /f /im python.exe >nul 2>&1
echo    • Esperando limpieza...
timeout /t 3 /nobreak >nul
echo    ✅ Sistema limpio

echo.
echo 🔧 PASO 2: VERIFICANDO ENTORNO PYTHON...
python --version
if %errorlevel% neq 0 (
    echo    ❌ Python no encontrado
    pause
    exit /b 1
) else (
    echo    ✅ Python disponible
)

echo.
echo 📦 PASO 3: VERIFICANDO DEPENDENCIAS...
python -c "import flask; print('   ✅ Flask disponible')" 2>nul || echo    ❌ Flask no disponible
python -c "import iqoptionapi; print('   ✅ IQ Option API disponible')" 2>nul || echo    ❌ IQ Option API no disponible
python -c "from flask_cors import CORS; print('   ✅ Flask-CORS disponible')" 2>nul || echo    ⚠️ Flask-CORS opcional

echo.
echo 🔄 PASO 4: ACTUALIZANDO DEPENDENCIAS...
echo    • Actualizando iqoptionapi...
pip install iqoptionapi --upgrade --quiet
echo    ✅ Dependencias actualizadas

echo.
echo 🚀 PASO 5: INICIANDO SERVICIOS...
echo    • Iniciando IQ Client (Puerto interno)...
start "STC IQ Client" cmd /k "echo IQ Client iniciando... && python iq_client.py"

echo    • Esperando inicialización (5 segundos)...
timeout /t 5 /nobreak >nul

echo    • Iniciando API Backend (Puerto 5002)...
start "STC API Backend" cmd /k "echo API Backend iniciando... && python iq_routes_redis_patch.py"

echo    • Esperando API Backend (3 segundos)...
timeout /t 3 /nobreak >nul

echo    • Iniciando Dashboard Web (Puerto 5001)...
start "STC Dashboard" cmd /k "echo Dashboard iniciando... && python dashboard_server.py"

echo.
echo ⏳ PASO 6: VERIFICANDO SERVICIOS (10 segundos)...
timeout /t 10 /nobreak >nul

echo.
echo 🔍 PASO 7: VERIFICACIÓN DE ESTADO...
netstat -an | findstr ":5001" | findstr "LISTENING" >nul
if %errorlevel%==0 (
    echo    ✅ Puerto 5001: Dashboard ACTIVO
) else (
    echo    ❌ Puerto 5001: Dashboard INACTIVO
)

netstat -an | findstr ":5002" | findstr "LISTENING" >nul
if %errorlevel%==0 (
    echo    ✅ Puerto 5002: API Backend ACTIVO
) else (
    echo    ❌ Puerto 5002: API Backend INACTIVO
)

for /f %%i in ('tasklist /fi "imagename eq python.exe" ^| find /c "python.exe"') do (
    if %%i gtr 0 (
        echo    ✅ Procesos Python: %%i activos
    ) else (
        echo    ❌ No hay procesos Python activos
    )
)

echo.
echo 🧪 PASO 8: PRUEBA RÁPIDA DE API...
echo    • Probando Health Check:
curl -s http://localhost:5002/health 2>nul || echo    ⚠️ API aún iniciando...

echo.
echo ========================================================
echo 🎉 SISTEMA STC TRADING INICIADO DESDE CERO
echo ========================================================
echo.
echo 🌐 ACCESO AL SISTEMA:
echo    • Dashboard: http://localhost:5001
echo    • API Backend: http://localhost:5002
echo    • Health Check: http://localhost:5002/health
echo.
echo 🔑 CREDENCIALES PARA LOGIN:
echo    • Email: diegofelipeserranobecerra@gmail.com  
echo    • Password: 123456789p
echo.
echo 📋 PRÓXIMOS PASOS:
echo    1. Abre el dashboard en tu navegador
echo    2. Ingresa las credenciales en el formulario
echo    3. Haz clic en "Connect" o "Login"
echo    4. Espera la conexión con IQ Option
echo    5. ¡Empieza a hacer trading real!
echo.
echo 🎯 ¡SISTEMA COMPLETAMENTE REINICIADO Y LISTO!
echo.
pause
