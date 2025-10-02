@echo off
cd c:\STC_Trading_System
echo Ejecutando test rapido de orden OTC...
echo.
C:\STC_Trading_System\.venv311\Scripts\python.exe test_quick_otc.py
echo.
echo Presiona cualquier tecla para cerrar...
pause > nul
