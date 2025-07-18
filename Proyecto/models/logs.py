'''Tabla logs'''
import datetime
from typing import Optional
from models import Base
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Logs(Base):
    '''Tabla logs'''
    __tablename__ = 'logs'

    operacion: Mapped[str] = mapped_column(Enum('del', 'upd', 'ins', 'sel'))
    tabla: Mapped[str] = mapped_column(Text)
    time_stamp: Mapped[datetime.datetime] = mapped_column(DateTime)
    personas_usuario: Mapped[str] = mapped_column(ForeignKey('personas.usuario'))
    id_log: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)

    personas: Mapped['Personas'] = relationship('Personas', back_populates='logs')
