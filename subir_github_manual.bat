@echo off
title GitHub Manual - STC Trading System
color 0A
echo.
echo ===============================================
echo   🚀 SUBIDA MANUAL A GITHUB - STC TRADING
echo ===============================================
echo.

echo 📍 Tu repositorio: https://github.com/stctrading/SmartTradeAcademy
echo.

echo 🔧 PASO 1: Verificar conexión Git
git --version
if %errorlevel% neq 0 (
    echo ❌ Git no está instalado
    pause
    exit /b 1
)

echo ✅ Git detectado
echo.

echo 🔧 PASO 2: Verificar repositorio local
git status
echo.

echo 🔧 PASO 3: Verificar conexión remota
git remote -v
echo.

echo 🔧 PASO 4: Intentar subida
echo 📤 Subiendo archivos a GitHub...
git push -u origin main

if %errorlevel%==0 (
    echo.
    echo ✅✅✅ ¡ÉXITO! PROYECTO SUBIDO A GITHUB ✅✅✅
    echo.
    echo 🌟 Tu repositorio: https://github.com/stctrading/SmartTradeAcademy
    echo.
) else (
    echo.
    echo ⚠️ Problema con la autenticación GitHub
    echo.
    echo 💡 SOLUCIONES:
    echo    1. Configura credenciales Git:
    echo       git config --global user.name "Tu Nombre"
    echo       git config --global user.email "tu@email.com"
    echo.
    echo    2. Autenticación con token (recomendado):
    echo       - Ve a: https://github.com/settings/tokens
    echo       - Genera un Personal Access Token
    echo       - Úsalo como password cuando Git lo pida
    echo.
    echo    3. GitHub CLI (alternativo):
    echo       - Instala: https://cli.github.com/
    echo       - Ejecuta: gh auth login
    echo.
)

echo.
echo ===============================================
echo   🔄 SIGUIENTE PASO: IMPORTAR EN REPLIT
echo ===============================================
echo.
echo 1️⃣ Ve a: https://replit.com/
echo 2️⃣ Clic en "Create Repl" 
echo 3️⃣ Selecciona "Import from GitHub"
echo 4️⃣ Pega: https://github.com/stctrading/SmartTradeAcademy
echo 5️⃣ Clic en "Import from GitHub"
echo.
echo 6️⃣ CONFIGURAR SECRETS EN REPLIT:
echo    - Variables → Secrets
echo    - IQ_EMAIL = tu_email@gmail.com  
echo    - IQ_PASSWORD = tu_password
echo.
echo 7️⃣ INSTALAR DEPENDENCIAS:
echo    pip install -r requirements.txt
echo.
echo 8️⃣ EJECUTAR SISTEMA:
echo    python dashboard_server.py
echo    O usar: python iq_routes_redis_patch.py
echo.

pause
