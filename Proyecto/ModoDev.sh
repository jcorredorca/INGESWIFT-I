#!/bin/bash

# Verificar si la máquina tiene Python
if command -v python3 >/dev/null 2>&1
then
    echo "Python 3 está instalado."
else
    echo "Python 3 no está instalado. Por favor instalelo"
    exit
fi

#Verificar si la maquina tiene python-venv
if python3 -c "import ensurepip" >/dev/null 2>&1
then
    echo "Python-venv esta instalado."
else
    echo "ensurepip no esta disponible. Por favor ejecute los siguientes comandos e intente nuevamente:"
    echo "	sudo apt install python3-venv"
    exit
fi


# Verificar si la máquina tiene pip
if command -v pip3 >/dev/null 2>&1
then
    echo "Pip3 está instalado."
else
    echo "Pip3 no está instalado. Por favor ejecute los siguientes comandos e intente nuevamente:"
    echo "      sudo apt update"
    echo "      sudo apt install python3-pip"
    exit
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
source "venv/bin/activate"

#Verificar si tkinter esta disponible
if python -c "import tkinter" >/dev/null 2>&1
then
    echo "tkinter esta disponible."
else
    echo "Por favor, permita la instalacion de tkinter"
    sudo apt install python3-tk
fi

# Asegurarse de tener pip actualizado dentro del venv
pip install --upgrade pip

# Lista de librerías
LIBRARIES=("customtkinter" "dotenv" "bcrypt" "sib_api_v3_sdk")
which python3

for lib in "${LIBRARIES[@]}"; do
    if python -c "import $lib" >/dev/null 2>&1
    then
        echo "$lib está instalado."
    else
        echo "$lib no está instalado. Procediendo con su instalación..."
        if pip install "$lib"
        then
            echo "La librería $lib ha sido instalada correctamente."
        else
            echo "Error al instalar la librería $lib. Revisa tu conexión o permisos."
        fi
    fi
done

if python -c "import PIL" >/dev/null 2>&1
then
    echo "pillow esta instalado."
else
    echo "pillow no esta instalado. Procediendo con su instalacion..."
    if pip install pillow
    then
	echo "La libreria pillow ha sido instalada correctamente."
    else
	echo "Error al instalar la libreria pillow. Revisa tu conexion o permisos."
    fi
fi

python script_modo_dev.py
python app.py