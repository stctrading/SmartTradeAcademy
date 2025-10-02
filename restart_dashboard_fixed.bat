@echo off
echo ==========================================
echo     REINICIANDO DASHBOARD CON GRAFICOS CORREGIDOS
echo ==========================================
echo.

echo 1. Cerrando dashboard actual...
taskkill /f /im python.exe /fi "WINDOWTITLE eq STC-Dashboard" >nul 2>&1

echo 2. Esperando 3 segundos...
timeout /t 3 >nul

echo 3. Reiniciando Dashboard con gráficos mejorados...
start "STC-Dashboard" cmd /c "cd /d c:\STC_Trading_System && C:\STC_Trading_System\.venv311\Scripts\python.exe dashboard_server.py"

echo 4. Esperando 5 segundos...
timeout /t 5 >nul

echo 5. Probando dashboard...
curl -s http://localhost:5001/health

echo.
echo ==========================================
echo     DASHBOARD ACTUALIZADO
echo ==========================================
echo.
echo 🔧 CORRECCIONES APLICADAS:
echo   • Versión específica de LightweightCharts (4.1.0)
echo   • CDN backup en caso de fallo
echo   • Modo fallback sin gráficos
echo   • Verificación de funciones antes de uso
echo.
echo 📊 FUNCIONALIDADES:
echo   • Si los gráficos cargan: Velas completas
echo   • Si no cargan: Modo texto con precios
echo   • Trading sigue funcionando en ambos casos
echo.
echo 🌐 Acceso: http://localhost:5001
echo.
pause
