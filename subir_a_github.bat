@echo off
title STC Trading - Subir a GitHub y Replit
color 0A
echo.
echo ===============================================
echo   📚 GUÍA PARA SUBIR STC TRADING A GITHUB
echo ===============================================
echo.

echo 🎯 PASOS PARA GITHUB:
echo.
echo 1️⃣ INICIALIZAR REPOSITORIO LOCAL:
echo    cd c:\STC_Trading_System
echo    git init
echo    git add .
echo    git commit -m "Initial commit: STC Trading System"
echo.

echo 2️⃣ CREAR REPOSITORIO EN GITHUB:
echo    • Ve a: https://github.com/new
echo    • Nombre: stc-trading-system
echo    • Descripción: Sistema de trading automatizado para IQ Option
echo    • Público o Privado (tu elección)
echo    • NO marques README, .gitignore, license (ya los tenemos)
echo    • Clic en "Create repository"
echo.

echo 3️⃣ CONECTAR Y SUBIR:
echo    git remote add origin https://github.com/TU_USUARIO/stc-trading-system.git
echo    git branch -M main
echo    git push -u origin main
echo.

echo 🚀 COMANDOS AUTOMÁTICOS:
echo ===============================================

echo ¿Quieres ejecutar los comandos automáticamente? (S/N)
set /p respuesta=

if /i "%respuesta%"=="S" (
    echo.
    echo 📦 Inicializando repositorio Git...
    git --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Git no está instalado. Instálalo desde: https://git-scm.com/
        pause
        exit /b 1
    )
    
    echo ✅ Git detectado
    git init
    git add .
    git commit -m "Initial commit: STC Trading System completo con dashboard, API y gráficos"
    
    echo.
    echo ✅ Repositorio local creado
    echo.
    echo 🌐 AHORA EN GITHUB:
    echo    1. Ve a https://github.com/new
    echo    2. Crea repositorio: stc-trading-system
    echo    3. Copia la URL del repositorio
    echo.
    echo 📝 Introduce la URL de tu repositorio GitHub:
    echo    Ejemplo: https://github.com/tuusuario/stc-trading-system.git
    set /p repo_url=URL del repositorio: 
    
    if not "%repo_url%"=="" (
        echo.
        echo 🔗 Conectando con GitHub...
        git remote add origin %repo_url%
        git branch -M main
        
        echo 🚀 Subiendo archivos...
        git push -u origin main
        
        if %errorlevel%==0 (
            echo.
            echo ✅✅✅ PROYECTO SUBIDO EXITOSAMENTE A GITHUB! ✅✅✅
            echo.
            echo 🌟 Tu repositorio está en: %repo_url%
        ) else (
            echo.
            echo ❌ Error subiendo. Verifica:
            echo    • URL del repositorio correcta
            echo    • Credenciales de GitHub
            echo    • Conexión a internet
        )
    )
)

echo.
echo ===============================================
echo   🔄 PASOS PARA REPLIT
echo ===============================================
echo.
echo 1️⃣ IMPORTAR DESDE GITHUB:
echo    • Ve a: https://replit.com/
echo    • Clic en "Create Repl"
echo    • Selecciona "Import from GitHub"
echo    • Pega la URL: %repo_url%
echo    • Clic en "Import from GitHub"
echo.

echo 2️⃣ CONFIGURAR EN REPLIT:
echo    • Replit detectará automáticamente Python
echo    • Agrega tus credenciales en Secrets:
echo      - IQ_EMAIL: tu_email@gmail.com
echo      - IQ_PASSWORD: tu_password
echo    • Ejecuta: pip install -r requirements.txt
echo.

echo 3️⃣ EJECUTAR EN REPLIT:
echo    • Archivo principal: dashboard_server.py
echo    • O ejecuta: inicio_manual.bat (si está disponible)
echo    • URLs: https://tu-repl.replit.app
echo.

echo 📋 ARCHIVOS IMPORTANTES INCLUIDOS:
echo    ✅ README_GITHUB.md - Documentación completa
echo    ✅ .gitignore - Archivos excluidos de Git
echo    ✅ requirements.txt - Dependencias Python
echo    ✅ Todo el código fuente del sistema
echo.

echo 🎉 ¡LISTO PARA SUBIR A GITHUB Y REPLIT!
echo.
pause
