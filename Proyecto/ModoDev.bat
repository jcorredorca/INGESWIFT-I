@echo off
python --version >nul 2>&1
if errorlevel 1 (
    echo Python no esta instalado o no esta en el PATH.
    pause
    exit /b
) else (
    echo Python esta instalado.
)

python -m venv venv
call venv\Scripts\activate

for %%i in (customtkinter dotenv pillow bcrypt sib_api_v3_sdk sqlalchemy) do (
    pip show %%i >nul 2>&1
    if errorlevel 1 (
        echo %%i no está instalado. Procediendo con su intalacion...
        pip install %%i
        echo La libreria ha sido instalada correctamente!
    ) else (
        echo %%i esta instalado.
    )

)

python script_modo_dev.py
pause
python app.py

call venv\Scripts\deactivate
