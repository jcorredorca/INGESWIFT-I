'''Funcionalidades especificas para miembros'''
from hashlib import sha256
from datetime import datetime, timedelta
from models.conexion import Conexion

def recuperar_estado(usuario):
    '''Esta funcion recupera el estado de un miembro'''

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

def generar_codigo_reserva(usuario: str, id_sesion: int) -> str:
    '''
    Genera un código único de reserva combinando el hash del usuario y el ID de sesión.
    '''
    # Hash del usuario (obtenemos los primeros 8 caracteres del hash hexadecimal)
    hash_usuario = sha256(usuario.encode()).hexdigest()[:5]

    # Concatenamos el hash corto con el ID
    codigo = f"{hash_usuario}{id_sesion}"

    return codigo

def crear_reserva(codigo, sesion, usuario):
    '''Esta funcion crea una nueva reserva para el codigo dado'''
    query_reserva = '''    INSERT INTO reservas (codigo, sesiones_id, personas_usuario)
    VALUES (?, ?, ?) '''
    Conexion().ejecutar_consulta(query_reserva, (codigo, sesion, usuario))

def eliminar_reserva(codigo):
    '''Esta funcion crea una nueva reserva para el codigo dado'''
    query_reserva = '''  DELETE FROM reservas WHERE codigo = ? '''
    Conexion().ejecutar_consulta(query_reserva, (codigo, ))

def sesion_disponible(sesion):
    '''Esta funcion confirma si una sesion esta dentro del
    rango de dos horas a partir ahora'''
    query = "SELECT fecha FROM sesiones WHERE id = ?"
    resultado = Conexion().ejecutar_consulta(query, (sesion,))
    if len(resultado) < 1:
        return False
    fecha_sesion = datetime.fromisoformat(resultado[0][0])

    ahora = datetime.now()
    dos_horas_despues = ahora + timedelta(hours=2)

    return ahora <= fecha_sesion <= dos_horas_despues

def recuperar_cupos(sesion):
    '''Este metodo recupera el numero de cupos disponibles para una sesion'''
    query_cupos = '''SELECT actividad.aforo
        FROM sesiones
        JOIN actividad ON sesiones.actividad_tipo = actividad.tipo
        WHERE sesiones.id = ?'''

    respuesta = Conexion().ejecutar_consulta(query_cupos, (sesion,))
    aforo = respuesta[0][0]
    if aforo == -1:
        return True
    query_reservas = '''SELECT COUNT(*)
        FROM reservas
        WHERE sesiones_id = ?'''
    respuesta = Conexion().ejecutar_consulta(query_reservas, (sesion,))
    reservas = respuesta[0][0]
    return aforo - reservas
