'''Tabla Actividad'''
from typing import List
from models import Base
from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Actividad(Base):
    '''Tabla Actividad'''
    __tablename__ = 'actividad'

    tipo: Mapped[str] = mapped_column(Text, primary_key=True)
    aforo: Mapped[int] = mapped_column(Integer)

    sesiones: Mapped[List['Sesiones']] = relationship('Sesiones', back_populates='actividad')
