'''Tabla penalizaciones'''
import datetime
from models.personas import Personas
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class Penalizaciones(Personas):
    '''Tabla penalizaciones'''
    __tablename__ = 'penalizaciones'

    personas_usuario: Mapped[str] = mapped_column(ForeignKey('personas.usuario'), primary_key=True)
    fin_penalizacion: Mapped[datetime.datetime] = mapped_column(DateTime)
