@echo off
title GitHub Force Push - STC Trading System  
color 0A
echo.
echo ===============================================
echo   🚀 SOLUCIÓN RÁPIDA - SUBIR A GITHUB
echo ===============================================
echo.

echo 📍 Repositorio: https://github.com/stctrading/SmartTradeAcademy
echo.

echo 🔧 OPCIÓN 1: Force Push (sobrescribir GitHub)
echo ⚠️  ADVERTENCIA: Esto sobrescribirá el contenido actual en GitHub
echo.
set /p opcion=¿Quieres sobrescribir GitHub con tu versión local? (S/N): 

if /i "%opcion%"=="S" (
    echo.
    echo 🚀 Realizando force push...
    git push --force-with-lease origin main
    
    if %errorlevel%==0 (
        echo.
        echo ✅✅✅ ¡ÉXITO! PROYECTO SUBIDO A GITHUB ✅✅✅
        echo.
        echo 🌟 Tu repositorio: https://github.com/stctrading/SmartTradeAcademy
        echo.
        goto replit_steps
    ) else (
        echo.
        echo ❌ Error en force push. Probando método alternativo...
        goto alternative_method
    )
) else (
    goto alternative_method
)

:alternative_method
echo.
echo 🔧 MÉTODO ALTERNATIVO: Crear nuevo repositorio
echo.
echo 💡 RECOMENDACIÓN:
echo 1. Ve a GitHub y elimina el repositorio actual (si es tuyo)
echo 2. Crea un nuevo repositorio vacío con el mismo nombre
echo 3. Ejecuta este comando:
echo    git push -u origin main
echo.
echo O usa este comando para crear una nueva rama:
set /p nueva_rama=¿Quieres crear una nueva rama? (Escribe el nombre o N): 

if /i not "%nueva_rama%"=="N" (
    git checkout -b %nueva_rama%
    git push -u origin %nueva_rama%
    echo ✅ Nueva rama '%nueva_rama%' creada y subida
)

:replit_steps
echo.
echo ===============================================
echo   🔄 PASOS PARA REPLIT
echo ===============================================
echo.
echo 1️⃣ Ve a: https://replit.com/
echo 2️⃣ Clic en "Create Repl"
echo 3️⃣ Selecciona "Import from GitHub" 
echo 4️⃣ Pega: https://github.com/stctrading/SmartTradeAcademy
echo 5️⃣ Clic en "Import from GitHub"
echo.
echo 6️⃣ CONFIGURAR SECRETS EN REPLIT:
echo    Variables → Secrets
echo    • IQ_EMAIL = tu_email@gmail.com
echo    • IQ_PASSWORD = tu_password  
echo.
echo 7️⃣ INSTALAR DEPENDENCIAS:
echo    Abre el Shell de Replit y ejecuta:
echo    pip install -r requirements.txt
echo.
echo 8️⃣ EJECUTAR EL SISTEMA:
echo    Opción A: python dashboard_server.py
echo    Opción B: python iq_routes_redis_patch.py
echo    Opción C: Ejecutar ambos en terminales separados
echo.
echo 🌐 Tu aplicación estará en: https://tu-nombre-repl.replit.app
echo.

echo 📋 ARCHIVOS IMPORTANTES EN TU PROYECTO:
echo ✅ requirements.txt - Dependencias Python
echo ✅ dashboard_server.py - Servidor del dashboard  
echo ✅ iq_routes_redis_patch.py - API backend
echo ✅ iq_client.py - Cliente IQ Option
echo ✅ templates/dashboard_pro.html - Interface web
echo ✅ static/ - Archivos CSS y JS
echo.

pause
