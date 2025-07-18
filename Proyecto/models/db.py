'''Este modulo crea el engine'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.modelos import Base
from config import DB_PATH

# Crea el engine (conecta base de datos SQLite)
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)

# Crea el SessionLocal (fábrica de sesiones)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def crear_tablas():
    '''Crea las tablas basado en los modelos'''
    Base.metadata.create_all(bind=engine)
