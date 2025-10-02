@echo off
echo ==========================================
echo     NUEVO DASHBOARD STC - DISEÑO PRO
echo ==========================================
echo.

echo 1. Deteniendo procesos anteriores...
taskkill /f /im python.exe >nul 2>&1

echo 2. Esperando limpieza...
timeout /t 3 >nul

echo 3. Iniciando API Backend (puerto 5002)...
start "STC-API-Backend" cmd /c "cd /d c:\STC_Trading_System && C:\STC_Trading_System\.venv311\Scripts\python.exe iq_routes_redis_patch.py"

echo 4. Esperando API Backend...
timeout /t 5 >nul

echo 5. Iniciando Nuevo Dashboard Pro (puerto 5001)...
start "STC-Dashboard-Pro" cmd /c "cd /d c:\STC_Trading_System && C:\STC_Trading_System\.venv311\Scripts\python.exe dashboard_server.py"

echo 6. Esperando Dashboard...
timeout /t 4 >nul

echo 7. Iniciando Cliente IQ Option...
start "STC-IQ-Client" cmd /c "cd /d c:\STC_Trading_System && C:\STC_Trading_System\.venv311\Scripts\python.exe iq_client.py"

echo 8. Esperando conexión IQ...
timeout /t 5 >nul

echo.
echo ==========================================
echo     VERIFICANDO NUEVO SISTEMA...
echo ==========================================

echo 9. Probando API Backend:
curl -s -m 5 http://localhost:5002/health >nul 2>&1
if %ERRORLEVEL% == 0 (echo ✓ API Backend OK) else (echo ✗ API Backend Error)

echo.
echo 10. Probando Dashboard Pro:
curl -s -m 5 http://localhost:5001/health >nul 2>&1
if %ERRORLEVEL% == 0 (echo ✓ Dashboard Pro OK) else (echo ✗ Dashboard Error)

echo.
echo 11. Probando ruta de trading:
curl -X POST -s -m 5 http://localhost:5002/api/iq/trade -H "Content-Type: application/json" -d "{\"symbol\":\"EURUSD-OTC\",\"direction\":\"call\",\"amount\":1,\"expiration\":1}" >nul 2>&1
if %ERRORLEVEL% == 0 (echo ✓ Trading API OK) else (echo ✗ Trading Error)

echo.
echo ==========================================
echo       NUEVO DASHBOARD LISTO
echo ==========================================
echo.
echo 🌟 NUEVA INTERFAZ PROFESIONAL:
echo   • Dashboard Pro: http://localhost:5001
echo   • Diseño moderno y elegante
echo   • Gráficos optimizados
echo   • Trading integrado
echo.
echo 🔧 COMPATIBILIDAD:
echo   • Dashboard anterior: http://localhost:5001/dashboard_old
echo   • API Backend: http://localhost:5002
echo.
echo 📊 CARACTERÍSTICAS:
echo   • Gráficos TradingView Lightweight
echo   • Interface de trading rápida
echo   • Balance en tiempo real
echo   • Estadísticas integradas
echo   • Diseño responsive
echo.
echo ⚡ ACCIONES RÁPIDAS:
echo   1. Abrir http://localhost:5001 en navegador
echo   2. Usar botones CALL/PUT para operar
echo   3. Monitorear balance y estadísticas
echo.
pause
