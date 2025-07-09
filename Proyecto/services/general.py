'''Servicios generales de la app'''
from models.conexion import Conexion

def recuperar_actividades():
    '''Esta funcion recupera los tipos de actividad ofertados'''

    query_actividades = "SELECT tipo FROM actividad"
    respuesta = Conexion().ejecutar_consulta(query_actividades)
    actividades = [actividad[0] for actividad in respuesta]

    return actividades
