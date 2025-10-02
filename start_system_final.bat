@echo off
echo ==========================================
echo     STC TRADING SYSTEM - RESET Y INICIO
echo ==========================================
echo.
echo 1. Deteniendo TODOS los procesos Python...
taskkill /f /im python.exe >nul 2>&1

echo 2. Esperando 3 segundos para limpieza completa...
timeout /t 3 >nul

echo 3. Iniciando API Backend (puerto 5002)...
start "STC-API-Backend" cmd /c "cd /d c:\STC_Trading_System && C:\STC_Trading_System\.venv311\Scripts\python.exe iq_routes_redis_patch.py"

echo 4. Esperando 4 segundos...
timeout /t 4 >nul

echo 5. Iniciando Dashboard Frontend (puerto 5001)...
start "STC-Dashboard" cmd /c "cd /d c:\STC_Trading_System && C:\STC_Trading_System\.venv311\Scripts\python.exe dashboard_server.py"

echo 6. Esperando 4 segundos...
timeout /t 4 >nul

echo 7. Iniciando cliente IQ Option...
start "STC-IQ-Client" cmd /c "cd /d c:\STC_Trading_System && C:\STC_Trading_System\.venv311\Scripts\python.exe iq_client.py"

echo 8. Esperando 3 segundos para conexión IQ...
timeout /t 3 >nul

echo.
echo ==========================================
echo     VERIFICANDO SISTEMA...
echo ==========================================

echo 9. Dashboard (puerto 5001):
curl -s -m 5 http://localhost:5001/health || echo "FALLO"

echo.
echo 10. API Backend (puerto 5002):  
curl -s -m 5 http://localhost:5002/health || echo "FALLO"

echo.
echo 11. Balance IQ Option:
curl -s -m 5 http://localhost:5002/api/iq/balance || echo "FALLO"

echo.
echo ==========================================
echo        SISTEMA STC COMPLETAMENTE LISTO
echo ==========================================
echo.
echo 🌐 ACCESO WEB:
echo   • Dashboard Principal: http://localhost:5001
echo   • API Backend:         http://localhost:5002
echo   • Health Checks:       /health en ambos puertos
echo.
echo 📊 FUNCIONES DISPONIBLES:
echo   • Trading OTC 24/7 (EURUSD-OTC, GBPUSD-OTC, etc.)
echo   • Balance en tiempo real
echo   • Gráficos de velas M5 
echo   • Envío de órdenes CALL/PUT
echo.
echo ⚠️  Las ventanas del sistema están ejecutándose en segundo plano.
echo    Puedes cerrar esta ventana sin afectar el sistema.
echo.
echo Presiona cualquier tecla para continuar...
pause >nul
