@echo off
echo Probando puertos del sistema STC...
echo.

echo === PUERTO 5001 (Dashboard HTTPS) ===
curl -k -m 5 https://localhost:5001/api 2>nul
if %ERRORLEVEL% == 0 (
    echo ✓ Puerto 5001 ACTIVO - Dashboard accesible
) else (
    echo ✗ Puerto 5001 NO RESPONDE
)

echo.
echo === PUERTO 5002 (API HTTP) ===
curl -m 5 http://localhost:5002/health 2>nul  
if %ERRORLEVEL% == 0 (
    echo ✓ Puerto 5002 ACTIVO - API accesible
) else (
    echo ✗ Puerto 5002 NO RESPONDE
)

echo.
echo === BALANCE IQ OPTION ===
curl -m 5 -s http://localhost:5002/api/iq/balance 2>nul
if %ERRORLEVEL% == 0 (
    echo ✓ IQ Option conectado
) else (
    echo ✗ IQ Option no responde
)

echo.
echo ==========================================
echo ACCESO A PAGINAS WEB:
echo - Dashboard: https://localhost:5001
echo - API:       http://localhost:5002
echo ==========================================
pause
