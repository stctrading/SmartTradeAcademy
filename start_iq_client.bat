@echo off
echo 🚀 Iniciando Cliente IQ Option para Trading...
echo =============================================

cd /d "c:\STC_Trading_System"

echo 📧 Verificando credenciales...
echo    Email: %IQ_EMAIL%
echo    Balance: %IQ_BALANCE_TYPE%

echo.
echo 🔌 Iniciando cliente IQ Option...
echo ⏳ Esto puede tomar hasta 30 segundos...

start "IQ Client" .venv311\Scripts\python.exe iq_client.py

timeout /t 3 /nobreak >nul

echo.
echo ✅ Cliente IQ iniciado en ventana separada
echo 💡 Verifica la ventana "IQ Client" para ver la conexión
echo.
pause
