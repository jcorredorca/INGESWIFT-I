@echo off
python --version >nul 2>&1
if errorlevel 1 (
    echo Python no esta instalado o no esta en el PATH.
    pause
    exit /b
) else (
    echo Python esta instalado.
)
python script_modo_dev.py

pause
