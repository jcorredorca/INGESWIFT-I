'''Funciones de backend para el rol Funcionario'''

from datetime import datetime

from views.funcionarios import (modulo_asistencia, registro_extemporaneo,
                                registro_miembro, sesion_cerrada)
from services.funcionario import hay_cupos_disponibles

def redirigir_pantalla_miembros(origen):
    '''Esta función construye la ventana para registrar miembros'''
    ventana = registro_miembro.RegistroMiembro(origen)
    origen.contenido.destroy()
    origen.contenido = ventana
    origen.contenido.grid(row=1, column=0, sticky="nsew")

def redirigir_pantalla_asistencia(origen, sesion):
    '''Esta función construye la ventana para gestionar a los funcionarios'''
    minutos = datetime.now().minute

    ventana = modulo_asistencia.ModuloAsistencia(origen, sesion)
    if 10 < minutos < 55:
        if hay_cupos_disponibles(sesion):
            ventana = registro_extemporaneo.RegistroExtemporaneo(origen, sesion)
        else:
            ventana = sesion_cerrada.SesionCerrada(origen)

    origen.contenido.destroy()
    origen.contenido = ventana
    origen.contenido.grid(row=1, column=0, sticky="nsew")
