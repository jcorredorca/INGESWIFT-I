'''Tabla ubicaciones'''
from typing import List, Optional
from models import Base
from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Ubicaciones(Base):
    '''Tabla ubicaciones'''
    __tablename__ = 'ubicaciones'

    ubicacion: Mapped[str] = mapped_column(Text)
    id_ubicaciones: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    sesiones: Mapped[List['Sesiones']] = relationship('Sesiones', back_populates='ubicaciones')
