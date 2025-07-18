'''Tabla personas'''
from typing import List, Optional
from models import Base
from sqlalchemy import Enum, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Personas(Base):
    '''Tabla personas'''
    __tablename__ = 'personas'

    usuario: Mapped[str] = mapped_column(Text, primary_key=True)
    nombre: Mapped[str] = mapped_column(Text)
    apellido: Mapped[str] = mapped_column(Text)
    hash_contrasena: Mapped[str] = mapped_column(Text)
    correo: Mapped[str] = mapped_column(Text, unique=True)
    estado: Mapped[Optional[str]] = mapped_column(
                                                Enum('ACTIVO', 'INACTIVO'),
                                                server_default=text("'INACTIVO'")
                                                )
    rol_en_universidad: Mapped[Optional[str]] = mapped_column(
                                                Enum('GENERAL', 'FUNCIONARIO', 'FODUN', 'CUIDADO'),
                                                server_default=text("'GENERAL'")
                                                )
    grupo_especial: Mapped[Optional[str]] = mapped_column(Enum('JOVENES', 'SELECCION'))

    rol: Mapped[List['Rol']] = relationship(
                                            'Rol',
                                            secondary='rol_persona',
                                            back_populates='personas'
                                            )
    logs: Mapped[List['Logs']] = relationship('Logs', back_populates='personas')
    funcionarios_en_sesion: Mapped[List['FuncionariosEnSesion']] = relationship(
                                                                'FuncionariosEnSesion',
                                                                back_populates='personas'
                                                                                )
    reservas: Mapped[List['Reservas']] = relationship('Reservas', back_populates='personas')
