'''Este modulo crea el engine'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_PATH
from .base import Base
from .actividad import Actividad
from .sesiones import Sesiones
from .reservas import Reservas
from .funcionarios_sesion import FuncionariosEnSesion
from .personas import Personas
from .ubicaciones import Ubicaciones
from .rol import Rol
from .rol_persona import t_rol_persona
from .asistencias_extemp import t_asistencias_extemp
from .penalizacion import Penalizaciones
from .logs import Logs

__all__ = [
    "Personas", "Actividad", "Sesiones", "Rol", "Reservas", "t_asistencias_extemp",
    "Penalizaciones", "Logs", "FuncionariosEnSesion", "t_rol_persona", "Ubicaciones"
]

# Crea el engine (conecta base de datos SQLite)
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)

# Crea el SessionLocal (fábrica de sesiones)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def crear_tablas():
    '''Crea las tablas basado en los modelos'''
    Base.metadata.create_all(bind=engine)
