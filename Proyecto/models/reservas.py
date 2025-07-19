'''Tabla Reservas'''
from typing import Optional
from models import Base
from sqlalchemy import ForeignKey, Text, Integer, text
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Reservas(Base):
    '''Tabla Reservas'''
    __tablename__ = 'reservas'

    codigo: Mapped[str] = mapped_column(Text, primary_key=True)
    sesiones_id: Mapped[int] = mapped_column(ForeignKey('sesiones.id'))
    personas_usuario: Mapped[str] = mapped_column(ForeignKey('personas.usuario'))
    asistio: Mapped[Optional[int]] = mapped_column(Integer, server_default=text('0'))

    personas: Mapped['Personas'] = relationship('Personas', back_populates='reservas')
    sesiones: Mapped['Sesiones'] = relationship('Sesiones', back_populates='reservas')
