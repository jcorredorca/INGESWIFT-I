'''Tabla asistencias_extemp'''
from models import Base
from sqlalchemy import Column, ForeignKey, Table

t_asistencias_extemp = Table(
    'asistencias_extemp', Base.metadata,
    Column('personas_usuario', ForeignKey('personas.usuario'), primary_key=True, nullable=False),
    Column('sesiones_id', ForeignKey('sesiones.id'), primary_key=True, nullable=False)
)
