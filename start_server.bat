@echo off
echo.
echo 🚀 STC Trading Platform Server
echo ===============================
echo.
echo 🔧 Activating Python virtual environment...
echo.
echo 📊 Starting DUAL Protocol Servers:
echo    🔒 HTTPS: https://127.0.0.1:5001 (for MT5 Expert Advisor)
echo    🌐 HTTP:  http://127.0.0.1:5002 (for Web Dashboard)
echo.
echo ⏳ Starting server...
echo.

C:\IABOTBINARIAS\venv\Scripts\python.exe mt5_server.py

echo.
echo 🛑 Server stopped. Press any key to exit...
pause