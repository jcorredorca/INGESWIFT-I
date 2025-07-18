'''Tabla Rol'''
from models import Base
from typing import List
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Rol(Base):
    '''Tabla Rol'''
    __tablename__ = 'rol'

    nombre: Mapped[str] = mapped_column(
                        Enum('MIEMBRO', 'FUNCIONARIO', 'ADMINISTRADOR'),
                        primary_key=True
                        )

    personas: Mapped[List['Personas']] = relationship(
                                        'Personas',
                                        secondary='rol_persona',
                                        back_populates='rol'
                                        )
