'''Tabla FuncionariosEnSesion'''
from models import Base
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class FuncionariosEnSesion(Base):
    '''Tabla FuncionariosEnSesion'''
    __tablename__ = 'funcionarios_en_sesion'

    personas_usuario: Mapped[str] = mapped_column(ForeignKey('personas.usuario'), primary_key=True)
    sesiones_id: Mapped[int] = mapped_column(ForeignKey('sesiones.id'), primary_key=True)
    profesor_encargado: Mapped[str] = mapped_column(Enum('SI', 'NO'))

    personas: Mapped['Personas'] = relationship('Personas', back_populates='funcionarios_en_sesion')
    sesiones: Mapped['Sesiones'] = relationship('Sesiones', back_populates='funcionarios_en_sesion')
