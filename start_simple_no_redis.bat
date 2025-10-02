@echo off
title STC Trading System - Inicio Simplificado

echo.
echo ================================================================
echo                    🚀 STC TRADING SYSTEM 🚀
echo ================================================================
echo.
echo   📊 Iniciando sistema SIN Redis (cache en memoria)
echo   🔐 Datos de IQ Option reales + simulacion
echo   📈 Dashboard web funcional
echo.
echo ================================================================
echo.

REM Cambiar al directorio correcto
cd /d c:\STC_Trading_System

REM Verificar archivos
if not exist "backend_no_redis.py" (
    echo ❌ ERROR: backend_no_redis.py no encontrado
    pause
    exit /b 1
)

if not exist "iq_client_simple.py" (
    echo ❌ ERROR: iq_client_simple.py no encontrado
    pause
    exit /b 1
)

if not exist "mt5_server.py" (
    echo ❌ ERROR: mt5_server.py no encontrado
    pause
    exit /b 1
)

REM Detectar Python
set PYTHON_CMD=python
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    echo ✅ Python detectado: py
) else (
    python --version >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=python
        echo ✅ Python detectado: python
    ) else (
        echo ❌ Python no encontrado - Instala Python 3.8+ y reinicia
        pause
        exit /b 1
    )
)

REM Verificar/instalar dependencias mínimas
echo.
echo 📦 Verificando dependencias...
%PYTHON_CMD% -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando Flask...
    %PYTHON_CMD% -m pip install flask >nul 2>&1
)

%PYTHON_CMD% -c "import httpx" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando httpx...
    %PYTHON_CMD% -m pip install httpx >nul 2>&1
)

%PYTHON_CMD% -c "from dotenv import load_dotenv" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando python-dotenv...
    %PYTHON_CMD% -m pip install python-dotenv >nul 2>&1
)

echo ✅ Dependencias listas

REM Limpiar puertos si están ocupados
echo.
echo 🌐 Liberando puertos 5001 y 5002...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5001" 2^>nul') do (
    taskkill /PID %%a /F >nul 2>&1
)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5002" 2^>nul') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo.
echo ================================================================
echo                        🚀 INICIANDO SERVICIOS
echo ================================================================
echo.
echo 📋 COMPONENTES:
echo    1. 🔧 Backend API (sin Redis)  - Puerto 5002
echo    2. 🔌 Cliente IQ Simple        - Datos reales + mock
echo    3. 🌐 Dashboard Web            - Puerto 5001
echo.

REM 1. Iniciar Backend API (sin Redis)
echo 🔧 Iniciando Backend API (Puerto 5002)...
start "STC Backend API" cmd /k "title STC Backend API ^(Puerto 5002^) && echo 🔧 Backend iniciando... && %PYTHON_CMD% backend_no_redis.py"

REM Esperar que inicie
echo ⏳ Esperando backend (3 segundos)...
timeout /t 3 /nobreak >nul

REM 2. Iniciar Cliente IQ Simple
echo 🔌 Iniciando Cliente IQ Simple...
start "STC IQ Client" cmd /k "title STC IQ Client && echo 🔌 Cliente IQ iniciando... && %PYTHON_CMD% iq_client_simple.py"

REM Esperar que inicie
echo ⏳ Esperando cliente IQ (3 segundos)...
timeout /t 3 /nobreak >nul

REM 3. Iniciar Dashboard Web
echo 🌐 Iniciando Dashboard Web (Puerto 5001)...
start "STC Dashboard" cmd /k "title STC Dashboard ^(Puerto 5001^) && echo 🌐 Dashboard iniciando... && %PYTHON_CMD% mt5_server.py"

REM Esperar que todos inicien
echo ⏳ Esperando que todos los servicios inicien (5 segundos)...
timeout /t 5 /nobreak >nul

REM Verificar servicios
echo.
echo 🔍 VERIFICANDO SERVICIOS...

REM Comprobar si los puertos están activos
netstat -an | findstr ":5002" >nul 2>&1
if not errorlevel 1 (
    echo ✅ Backend API: Puerto 5002 activo
) else (
    echo ⚠️ Backend API: Verificando...
)

netstat -an | findstr ":5001" >nul 2>&1
if not errorlevel 1 (
    echo ✅ Dashboard Web: Puerto 5001 activo
) else (
    echo ⚠️ Dashboard Web: Verificando...
)

echo.
echo ================================================================
echo                    ✅ SISTEMA INICIADO
echo ================================================================
echo.
echo 🎉 COMPONENTES ACTIVOS:
echo.
echo    🔧 Backend API        ✅ http://localhost:5002/health
echo    🔌 Cliente IQ Simple  ✅ Enviando datos reales/mock
echo    🌐 Dashboard Web      ✅ http://localhost:5001
echo.
echo 💾 CACHE: Memoria (sin Redis)
echo 📊 DATOS: IQ Option reales + simulacion
echo 📈 VELAS: M5 en tiempo real
echo.
echo 🚀 ACCESO AL DASHBOARD:
echo    👉 http://localhost:5001
echo.
echo 🔧 API ENDPOINTS:
echo    👉 http://localhost:5002/health
echo    👉 http://localhost:5002/api/iq/symbols
echo    👉 http://localhost:5002/api/iq/candles?symbol=EURUSD
echo.
echo ================================================================

REM Abrir dashboard automáticamente
timeout /t 2 /nobreak >nul
echo 🌐 Abriendo dashboard en navegador...
start http://localhost:5001

echo.
echo ✅ Sistema STC Trading iniciado correctamente
echo 💡 Modo: Sin Redis - Cache en memoria
echo 📊 Datos: Reales de IQ Option + simulacion de respaldo
echo 💰 Balance: Modo PRACTICE (cuenta demo)
echo.
echo 📝 PARA DETENER:
echo    - Cierra las 3 ventanas de comandos que se abrieron
echo    - O presiona Ctrl+C en cada una
echo.
echo 🎯 ¡LISTO PARA TRADING!
echo.
pause
