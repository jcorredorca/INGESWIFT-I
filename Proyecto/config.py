''' Este modulo se encarga de crear las constantes globales del sistema '''
import os
import sys
import shutil
from dotenv import load_dotenv

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, compatible con PyInstaller."""
    try:
        # PyInstaller crea una carpeta temporal y almacena el path en _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# Ruta a la carpeta de datos persistente
USER_DATA_DIR = os.path.join(os.path.expanduser("~"), ".atun")
os.makedirs(USER_DATA_DIR, exist_ok=True)

# Ruta definitiva de la base de datos fuera del .exe
DB_PATH = os.path.join(USER_DATA_DIR, "AFID.db")

# Si la BD no existe aún, copiarla desde los recursos
if not os.path.exists(DB_PATH):
    original_db_path = resource_path(os.path.join("data", "AFID.db"))
    shutil.copy2(original_db_path, DB_PATH)

# Ruta absoluta a la carpeta de imagenes del proyecto
IMG_PATH = resource_path(os.path.join("assets", "images"))

# Ruta absoluta al icono de la aplicación
APP_ICON = resource_path(os.path.join("assets", "images", "iconATUN.ico"))
APP_ICON_LINUX = resource_path(os.path.join("assets", "images", "iconATUN.png"))

# Configuración de la aplicación
APP_TITLE = "ATUN"
# Colores y fuentes globales
COLOR_PRIMARIO = "#2e1045"
COLOR_SECUNDARIO = "#a783c2"
FUENTE_TITULO = ("Libre Baskerville", 28, "bold")
FUENTE_GENERAL = ("Arial", 14)

# Otros parámetros globales...
# Carga las credenciales desde .env
dotenv_path = resource_path(".env")
load_dotenv(dotenv_path)
API_KEY = os.getenv("BREVO_API_KEY")
