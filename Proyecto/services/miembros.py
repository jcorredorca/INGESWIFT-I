'''Funcionalidades especificas para miembros'''
from models.conexion import Conexion

def recuperar_estado(usuario):
    '''Esta funcion recupera el estado de un miebro'''

    query_estado = '''SELECT estado
                        FROM personas
                        WHERE usuario = ?;'''
    respuesta = Conexion().ejecutar_consulta(query_estado, (usuario,))

    return respuesta[0][0]

def buscar_reserva(usuario, sesion):
    '''Esta funcion recupera la reserva de un miembro a una sesion  '''

    query_reserva = '''SELECT codigo
                        FROM reservas
                        WHERE personas_usuario = ? AND
                        sesiones_id = ?;'''
    respuesta = Conexion().ejecutar_consulta(query_reserva, (usuario, sesion))
    if len(respuesta) > 0:
        return respuesta[0][0]
    return False

def hay_cupos_disponibles(id_sesion):
    '''Esta funcion revisa la cantidad de cupos disponibles para determinada sesion
    Retorna:
        True  → hay cupo disponible o es aforo ilimitado.
        False → el aforo ya está completo.'''

    query_cupos = '''SELECT actividad.aforo
        FROM sesiones
        JOIN actividad ON sesiones.actividad_tipo = actividad.tipo
        WHERE sesiones.id = ?'''

    respuesta = Conexion().ejecutar_consulta(query_cupos, (id_sesion,))
    aforo = respuesta[0][0]
    if aforo == -1:
        return True
    query_reservas = '''SELECT COUNT(*)
        FROM reservas
        WHERE sesiones_id = ?'''
    respuesta = Conexion().ejecutar_consulta(query_reservas, (id_sesion,))
    reservas = respuesta[0][0]
    return reservas < aforo
