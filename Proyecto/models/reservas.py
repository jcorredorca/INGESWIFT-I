'''Tabla Reservas'''
from models import Base
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Reservas(Base):
    '''Tabla Reservas'''
    __tablename__ = 'reservas'

    codigo: Mapped[str] = mapped_column(Text, primary_key=True)
    sesiones_id: Mapped[int] = mapped_column(ForeignKey('sesiones.id'))
    personas_usuario: Mapped[str] = mapped_column(ForeignKey('personas.usuario'))

    personas: Mapped['Personas'] = relationship('Personas', back_populates='reservas')
    sesiones: Mapped['Sesiones'] = relationship('Sesiones', back_populates='reservas')
