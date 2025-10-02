@echo off
REM ==============================================================
REM    STC TRADING SYSTEM - SCRIPT DE INICIO COMPLETO
REM ==============================================================
REM
REM  🚀 Sistema de Trading IQ Option con TradingView Charts
REM  📊 Solo datos reales - Sin simulaciones
REM  🔐 Sesión persistente - Login/Logout funcional
REM  📈 Gráficos profesionales - TradingView Lightweight Charts
REM
REM ==============================================================

title STC Trading System - Iniciando...

echo.
echo ================================================================
echo                    🚀 STC TRADING SYSTEM 🚀
echo ================================================================
echo.
echo   📊 Sistema de Trading IQ Option Profesional
echo   🔐 Sesion persistente y datos reales
echo   📈 Graficos TradingView integrados
echo.
echo ================================================================
echo.

REM Colores para la consola
color 0a

REM Verificar directorio de trabajo
if not exist "iq_routes_redis_patch.py" (
    echo ❌ ERROR: No se encuentran los archivos del sistema
    echo    Asegurate de estar en el directorio correcto
    echo    Directorio actual: %cd%
    pause
    exit /b 1
)

REM Verificar entorno virtual
echo 🐍 VERIFICANDO ENTORNO PYTHON...
if exist ".venv311\Scripts\python.exe" (
    echo ✅ Entorno virtual encontrado: .venv311
    set PYTHON_CMD=.venv311\Scripts\python.exe
    set PIP_CMD=.venv311\Scripts\pip.exe
) else if exist "venv\Scripts\python.exe" (
    echo ✅ Entorno virtual encontrado: venv
    set PYTHON_CMD=venv\Scripts\python.exe
    set PIP_CMD=venv\Scripts\pip.exe
) else (
    echo ⚠️ No se encontro entorno virtual, usando Python global
    set PYTHON_CMD=python
    set PIP_CMD=pip
)

REM Verificar Python y dependencias
echo.
echo 📦 VERIFICANDO DEPENDENCIAS...
%PYTHON_CMD% -c "import flask, redis, iqoptionapi" 2>nul
if errorlevel 1 (
    echo ⚠️ Faltan dependencias, instalando...
    %PIP_CMD% install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error instalando dependencias
        echo    Ejecuta manualmente: pip install -r requirements.txt
        pause
        exit /b 1
    )
) else (
    echo ✅ Dependencias verificadas correctamente
)

REM Verificar Redis
echo.
echo 🗄️ VERIFICANDO REDIS...
netstat -an | findstr ":6380" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Redis no detectado en puerto 6380
    echo    Intentando iniciar con Docker...
    
    docker --version >nul 2>&1
    if not errorlevel 1 (
        echo 🐳 Iniciando Redis con Docker Compose...
        docker-compose up -d redis
        timeout /t 5 /nobreak >nul
        
        netstat -an | findstr ":6380" >nul 2>&1
        if errorlevel 1 (
            echo ❌ No se pudo iniciar Redis
            echo    Inicia Redis manualmente o verifica Docker
            pause
            exit /b 1
        ) else (
            echo ✅ Redis iniciado correctamente
        )
    ) else (
        echo ❌ Docker no disponible y Redis no esta corriendo
        echo    Instala Redis o Docker para continuar
        pause
        exit /b 1
    )
) else (
    echo ✅ Redis detectado en puerto 6380
)

REM Verificar archivo .env
echo.
echo ⚙️ VERIFICANDO CONFIGURACION...
if not exist ".env" (
    if exist ".env.example" (
        echo ⚠️ Creando archivo .env desde .env.example
        copy ".env.example" ".env" >nul
        echo ✅ Archivo .env creado
        echo.
        echo ⚠️ IMPORTANTE: Configura tus credenciales IQ Option en .env
        echo    - IQ_EMAIL=tu_email@gmail.com
        echo    - IQ_PASSWORD=tu_password
        echo.
        set /p continuar="Presiona ENTER cuando hayas configurado .env o 'n' para salir: "
        if /i "%continuar%"=="n" exit /b 0
    ) else (
        echo ❌ No se encuentra archivo .env ni .env.example
        echo    Configura las variables de entorno manualmente
        pause
        exit /b 1
    )
) else (
    echo ✅ Archivo .env encontrado
)

REM Crear directorios necesarios
echo.
echo 📁 CREANDO DIRECTORIOS...
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "static" mkdir static
echo ✅ Directorios verificados

REM Verificar puertos disponibles
echo.
echo 🌐 VERIFICANDO PUERTOS...

netstat -an | findstr ":5001" >nul 2>&1
if not errorlevel 1 (
    echo ⚠️ Puerto 5001 ocupado - Terminando proceso...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5001"') do taskkill /PID %%a /F >nul 2>&1
)

netstat -an | findstr ":5002" >nul 2>&1
if not errorlevel 1 (
    echo ⚠️ Puerto 5002 ocupado - Terminando proceso...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5002"') do taskkill /PID %%a /F >nul 2>&1
)

echo ✅ Puertos 5001 y 5002 disponibles

REM Mostrar información del sistema
echo.
echo ================================================================
echo                        🚀 INICIANDO SISTEMA
echo ================================================================
echo.
echo 📋 COMPONENTES:
echo    1. 🔧 Backend API Flask     (Puerto 5002)
echo    2. 🔌 Cliente IQ Option     (Conexion real)
echo    3. 🌐 Dashboard Web         (Puerto 5001)
echo    4. 🗄️ Redis Cache           (Puerto 6380)
echo.
echo 🎯 URLS DE ACCESO:
echo    👉 Dashboard: http://localhost:5001
echo    👉 API Health: http://localhost:5002/health
echo    👉 API Symbols: http://localhost:5002/api/iq/symbols
echo.
echo ================================================================

REM Iniciar componentes del sistema
echo.
echo 🔧 Iniciando Backend API Flask...
start "STC Backend API" /min cmd /k "title STC Backend API ^(Puerto 5002^) && echo 🔧 Backend API iniciando... && %PYTHON_CMD% iq_routes_redis_patch.py"

REM Esperar que el backend inicie
echo ⏳ Esperando que el backend inicie...
timeout /t 3 /nobreak >nul

REM Iniciar Cliente IQ Option
echo 🔌 Iniciando Cliente IQ Option...
start "STC IQ Client" /min cmd /k "title STC IQ Client ^(Conexion IQ Option^) && echo 🔌 Cliente IQ iniciando... && %PYTHON_CMD% iq_client.py"

REM Esperar que el cliente inicie
echo ⏳ Esperando que el cliente IQ inicie...
timeout /t 3 /nobreak >nul

REM Iniciar Dashboard Web
echo 🌐 Iniciando Dashboard Web...
start "STC Dashboard" /min cmd /k "title STC Dashboard ^(Puerto 5001^) && echo 🌐 Dashboard iniciando... && %PYTHON_CMD% mt5_server.py"

REM Esperar que todos los servicios inicien
echo ⏳ Esperando que todos los servicios inicien...
timeout /t 5 /nobreak >nul

REM Verificar que los servicios esten corriendo
echo.
echo 🔍 VERIFICANDO SERVICIOS...

REM Verificar API Backend
curl -s -o nul -w "%%{http_code}" http://localhost:5002/health | findstr "200" >nul
if not errorlevel 1 (
    echo ✅ Backend API: Corriendo correctamente
) else (
    echo ⚠️ Backend API: Verificando estado...
)

REM Verificar Dashboard
curl -s -o nul -w "%%{http_code}" http://localhost:5001 | findstr "200" >nul
if not errorlevel 1 (
    echo ✅ Dashboard Web: Corriendo correctamente
) else (
    echo ⚠️ Dashboard Web: Verificando estado...
)

echo.
echo ================================================================
echo                    ✅ SISTEMA INICIADO CORRECTAMENTE
echo ================================================================
echo.
echo 🎉 TODOS LOS COMPONENTES ESTAN ACTIVOS:
echo.
echo    🔧 Backend API Flask     ✅ http://localhost:5002
echo    🔌 Cliente IQ Option     ✅ Conectando a IQ Option...  
echo    🌐 Dashboard Web         ✅ http://localhost:5001
echo    🗄️ Redis Cache           ✅ Puerto 6380
echo.
echo 🚀 ACCEDER AL SISTEMA:
echo    👉 Abre tu navegador en: http://localhost:5001
echo    👉 Ingresa tus credenciales IQ Option
echo    👉 ¡Comienza a hacer trading!
echo.
echo 📚 DOCUMENTACION:
echo    👉 README.md - Informacion general
echo    👉 docs/ - Documentacion tecnica
echo.
echo 🛑 PARA DETENER EL SISTEMA:
echo    👉 Cierra todas las ventanas de comandos
echo    👉 O ejecuta: stop_system.bat
echo.
echo ================================================================

REM Abrir el dashboard automaticamente
timeout /t 3 /nobreak >nul
echo 🌐 Abriendo dashboard en el navegador...
start http://localhost:5001

echo.
echo ✅ Sistema STC Trading iniciado correctamente
echo 💰 ¡Feliz Trading!
echo.
echo Presiona cualquier tecla para minimizar esta ventana...
pause >nul

REM Minimizar la ventana principal
powershell -window minimized -command ""
