@echo off
title STC Trading System - Inicio Simple

echo.
echo ================================================================
echo                    🚀 STC TRADING SYSTEM 🚀
echo ================================================================
echo.
echo   📊 Iniciando sistema simplificado (sin Redis)
echo   🔐 Modo simulacion con datos realistas
echo   📈 Dashboard web integrado
echo.
echo ================================================================
echo.

REM Verificar directorio
if not exist "iq_client_simple.py" (
    echo ❌ ERROR: Archivos no encontrados
    pause
    exit /b 1
)

REM Buscar Python
set PYTHON_CMD=python
py --version >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=py
    echo ✅ Usando: py
) else (
    python --version >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=python
        echo ✅ Usando: python
    ) else (
        echo ❌ Python no encontrado
        echo    Instala Python 3.8+ y reinicia
        pause
        exit /b 1
    )
)

echo.
echo 📦 Instalando dependencias...
%PYTHON_CMD% -m pip install flask httpx python-dotenv >nul 2>&1

echo.
echo 🔧 Iniciando Backend API (Puerto 5002)...
start "STC Backend" /min cmd /k "title STC Backend API && %PYTHON_CMD% iq_routes_redis_patch.py"

timeout /t 3 /nobreak >nul

echo 🔌 Iniciando Cliente IQ Simple...
start "STC Client" /min cmd /k "title STC IQ Client && %PYTHON_CMD% iq_client_simple.py"

timeout /t 3 /nobreak >nul

echo 🌐 Iniciando Dashboard (Puerto 5001)...
start "STC Dashboard" /min cmd /k "title STC Dashboard && %PYTHON_CMD% mt5_server.py"

timeout /t 5 /nobreak >nul

echo.
echo ================================================================
echo                    ✅ SISTEMA INICIADO
echo ================================================================
echo.
echo 🎉 COMPONENTES ACTIVOS:
echo.
echo    🔧 Backend API        ✅ http://localhost:5002
echo    🔌 Cliente IQ Simple  ✅ Datos simulados realistas
echo    🌐 Dashboard Web      ✅ http://localhost:5001
echo.
echo 🚀 ACCEDER:
echo    👉 http://localhost:5001
echo.
echo ================================================================

timeout /t 3 /nobreak >nul
start http://localhost:5001

echo.
echo ✅ Sistema STC Trading iniciado en modo simple
echo 💡 Usando datos de simulacion realistas
echo 🌐 Dashboard abierto en navegador
echo.
pause
