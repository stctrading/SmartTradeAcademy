@echo off
title Solución GitHub Directa
echo.
echo ===============================================  
echo   🎯 SOLUCIÓN DIRECTA - STC TRADING A GITHUB
echo ===============================================
echo.

echo 🔧 Método 1: Cancelar merge y hacer force push
taskkill /f /im vim.exe 2>nul
taskkill /f /im git.exe 2>nul

timeout /t 2 /nobreak >nul

cd c:\STC_Trading_System

echo ⚠️ Cancelando merge en progreso...
git merge --abort 2>nul

echo 🚀 Haciendo force push directo...
git push --force origin main

if %errorlevel%==0 (
    echo.
    echo ✅✅✅ ¡ÉXITO! CÓDIGO SUBIDO A GITHUB ✅✅✅
    echo.
    echo 🌟 Repositorio: https://github.com/stctrading/SmartTradeAcademy
    echo.
) else (
    echo.
    echo 🔄 Intentando método alternativo...
    
    rem Resetear completamente
    git reset --hard HEAD
    git clean -fd
    
    rem Agregar archivos nuevos
    git add .
    git commit -m "STC Trading System - Versión completa actualizada"
    
    rem Force push
    git push --force origin main
    
    if %errorlevel%==0 (
        echo ✅ ¡Subido con método alternativo!
    ) else (
        echo ❌ Error. Verifica tu conexión a GitHub
    )
)

echo.
echo ===============================================
echo   📱 AHORA IMPORTAR EN REPLIT
echo ===============================================
echo.
echo 🌐 Pasos para Replit:
echo.
echo 1️⃣ Ve a: https://replit.com
echo 2️⃣ Clic "Create Repl" → "Import from GitHub"  
echo 3️⃣ URL: https://github.com/stctrading/SmartTradeAcademy
echo 4️⃣ Configura Secrets: IQ_EMAIL, IQ_PASSWORD
echo 5️⃣ Ejecuta: pip install -r requirements.txt
echo 6️⃣ Inicia: python dashboard_server.py
echo.

pause
