from typing import List, Optional
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Table, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Actividad(Base):
    __tablename__ = 'actividad'

    tipo: Mapped[str] = mapped_column(Text, primary_key=True)
    aforo: Mapped[int] = mapped_column(Integer)

    sesiones: Mapped[List['Sesiones']] = relationship('Sesiones', back_populates='actividad')


class Personas(Base):
    __tablename__ = 'personas'

    usuario: Mapped[str] = mapped_column(Text, primary_key=True)
    nombre: Mapped[str] = mapped_column(Text)
    apellido: Mapped[str] = mapped_column(Text)
    hash_contrasena: Mapped[str] = mapped_column(Text)
    correo: Mapped[str] = mapped_column(Text, unique=True)
    estado: Mapped[Optional[str]] = mapped_column(Enum('ACTIVO', 'INACTIVO'), server_default=text("'INACTIVO'"))
    rol_en_universidad: Mapped[Optional[str]] = mapped_column(Enum('GENERAL', 'FUNCIONARIO', 'FODUN', 'CUIDADO'), server_default=text("'GENERAL'"))
    grupo_especial: Mapped[Optional[str]] = mapped_column(Enum('JOVENES', 'SELECCION'))

    rol: Mapped[List['Rol']] = relationship('Rol', secondary='rol_persona', back_populates='personas')
    logs: Mapped[List['Logs']] = relationship('Logs', back_populates='personas')
    funcionarios_en_sesion: Mapped[List['FuncionariosEnSesion']] = relationship('FuncionariosEnSesion', back_populates='personas')
    reservas: Mapped[List['Reservas']] = relationship('Reservas', back_populates='personas')


class Rol(Base):
    __tablename__ = 'rol'

    nombre: Mapped[str] = mapped_column(Enum('MIEMBRO', 'FUNCIONARIO', 'ADMINISTRADOR'), primary_key=True)

    personas: Mapped[List['Personas']] = relationship('Personas', secondary='rol_persona', back_populates='rol')


class Ubicaciones(Base):
    __tablename__ = 'ubicaciones'

    ubicacion: Mapped[str] = mapped_column(Text)
    id_ubicaciones: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    sesiones: Mapped[List['Sesiones']] = relationship('Sesiones', back_populates='ubicaciones')


class Logs(Base):
    __tablename__ = 'logs'

    operacion: Mapped[str] = mapped_column(Enum('del', 'upd', 'ins', 'sel'))
    tabla: Mapped[str] = mapped_column(Text)
    time_stamp: Mapped[datetime.datetime] = mapped_column(DateTime)
    personas_usuario: Mapped[str] = mapped_column(ForeignKey('personas.usuario'))
    id_log: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    personas: Mapped['Personas'] = relationship('Personas', back_populates='logs')


class Penalizaciones(Personas):
    __tablename__ = 'penalizaciones'

    personas_usuario: Mapped[str] = mapped_column(ForeignKey('personas.usuario'), primary_key=True)
    fin_penalizacion: Mapped[datetime.datetime] = mapped_column(DateTime)


t_rol_persona = Table(
    'rol_persona', Base.metadata,
    Column('personas_usuario', ForeignKey('personas.usuario'), primary_key=True, nullable=False),
    Column('rol_nombre', ForeignKey('rol.nombre'), primary_key=True, nullable=False)
)


class Sesiones(Base):
    __tablename__ = 'sesiones'

    publico: Mapped[str] = mapped_column(Enum('GENERAL', 'FUNCIONARIO', 'FODUN'))
    fecha: Mapped[datetime.datetime] = mapped_column(DateTime)
    actividad_tipo: Mapped[str] = mapped_column(ForeignKey('actividad.tipo'))
    ubicaciones_id_ubicaciones: Mapped[int] = mapped_column(ForeignKey('ubicaciones.id_ubicaciones'))
    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    actividad: Mapped['Actividad'] = relationship('Actividad', back_populates='sesiones')
    ubicaciones: Mapped['Ubicaciones'] = relationship('Ubicaciones', back_populates='sesiones')
    funcionarios_en_sesion: Mapped[List['FuncionariosEnSesion']] = relationship('FuncionariosEnSesion', back_populates='sesiones')
    reservas: Mapped[List['Reservas']] = relationship('Reservas', back_populates='sesiones')


class FuncionariosEnSesion(Base):
    __tablename__ = 'funcionarios_en_sesion'

    personas_usuario: Mapped[str] = mapped_column(ForeignKey('personas.usuario'), primary_key=True)
    sesiones_id: Mapped[int] = mapped_column(ForeignKey('sesiones.id'), primary_key=True)
    profesor_encargado: Mapped[str] = mapped_column(Enum('SI', 'NO'))

    personas: Mapped['Personas'] = relationship('Personas', back_populates='funcionarios_en_sesion')
    sesiones: Mapped['Sesiones'] = relationship('Sesiones', back_populates='funcionarios_en_sesion')


class Reservas(Base):
    __tablename__ = 'reservas'

    codigo: Mapped[str] = mapped_column(Text, primary_key=True)
    sesiones_id: Mapped[int] = mapped_column(ForeignKey('sesiones.id'))
    personas_usuario: Mapped[str] = mapped_column(ForeignKey('personas.usuario'))

    personas: Mapped['Personas'] = relationship('Personas', back_populates='reservas')
    sesiones: Mapped['Sesiones'] = relationship('Sesiones', back_populates='reservas')
