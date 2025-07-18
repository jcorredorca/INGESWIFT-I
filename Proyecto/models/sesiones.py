'''Tabla sesiones'''
import datetime
from typing import List, Optional
from models import Base
from sqlalchemy import DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Sesiones(Base):
    '''Tabla sesiones'''
    __tablename__ = 'sesiones'

    publico: Mapped[str] = mapped_column(Enum('GENERAL', 'FUNCIONARIO', 'FODUN'))
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime)
    actividad_tipo: Mapped[str] = mapped_column(ForeignKey('actividad.tipo'))
    ubicaciones_id_ubicaciones: Mapped[int] = mapped_column(
                                                            ForeignKey('ubicaciones.id_ubicaciones')
                                                            )
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    actividad: Mapped['Actividad'] = relationship('Actividad', back_populates='sesiones')
    ubicaciones: Mapped['Ubicaciones'] = relationship('Ubicaciones', back_populates='sesiones')
    funcionarios_en_sesion: Mapped[List['FuncionariosEnSesion']] = relationship(
                                                                            'FuncionariosEnSesion',
                                                                            back_populates='sesiones'
                                                                                )
    reservas: Mapped[List['Reservas']] = relationship('Reservas', back_populates='sesiones')
