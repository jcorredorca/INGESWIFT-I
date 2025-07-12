''' Este modulo se encarga de crear las constantes globales del sistema '''
import os
import sys

from dotenv import load_dotenv


def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, compatible con PyInstaller."""
    try:
        # PyInstaller crea una carpeta temporal y almacena el path en _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# Ruta absoluta al archivo de la base de datos SQLite
DB_PATH = resource_path(os.path.join("data", "AFID.db"))

# Ruta absoluta a la carpeta de imagenes del proyecto
IMG_PATH = resource_path(os.path.join("assets", "images"))

# Ruta absoluta al icono de la aplicación
APP_ICON = resource_path(os.path.join("assets", "images", "iconATUN.ico"))

# Configuración de la aplicación
APP_TITLE = "ATUN"
#TODO: crear el logo con el pescadito
#APP_ICON = resource_path(os.path.join("assets", "images", "logo.ico"))

# Colores y fuentes globales
COLOR_PRIMARIO = "#2e1045"
COLOR_SECUNDARIO = "#a783c2"
FUENTE_TITULO = ("Libre Baskerville", 28, "bold")
FUENTE_GENERAL = ("Arial", 14)

# Otros parámetros globales...
# Carga las credenciales desde .env
load_dotenv()
API_KEY = os.getenv("BREVO_API_KEY")
