'''Tabla rol - persona'''
from models import Base
from sqlalchemy import Column, ForeignKey, Table

t_rol_persona = Table(
    'rol_persona', Base.metadata,
    Column('personas_usuario', ForeignKey('personas.usuario'), primary_key=True, nullable=False),
    Column('rol_nombre', ForeignKey('rol.nombre'), primary_key=True, nullable=False)
)
