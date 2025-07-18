# funcionarios.py

'''Funciones de backend para el rol Funcionario''' 

from datetime import datetime
from models import (SessionLocal,
                    t_rol_persona,
                    Personas
                    )
from sqlalchemy import select
from models.conexion import Conexion
from .general import enviar_correo


def registrar_miembro(info:dict):
    '''Esta funcion permite registrar un nuevo miembro en el sistema'''
    with SessionLocal.begin() as session: #pylint: disable = no-member
        nueva_persona = Personas(usuario = info["usuario"],
                                 nombre = info["nombre"],
                                 apellido = info["apellido"],
                                 hash_contrasena = info["contrasena"],
                                 correo = info["correo"],
                                 rol_en_universidad = info["rol"],
                                 grupo_especial = info["programa"]
                                )
        session.add(nueva_persona)
        stmt = t_rol_persona.insert().values(personas_usuario=info["usuario"], rol_nombre='MIEMBRO')
        session.execute(stmt)

    enviar_correo( 
        destinatario=info['correo'], 
        asunto='ATUN - Registro exitoso', 
        contenido_html=f""" 
        <h2>¡Hola {info['nombre']}!</h2> 
        <p>Tu registro en el sistema ATUN ha sido <strong>exitoso</strong>.</p> 
        <p>Recuerda que tus credenciales son: usuario: <strong>{info['usuario']}</strong> / 
contraseña: Tu <strong>número de documento de identidad</strong></p> 
        <p>Para poder hacer reservas, recuerda que debes ir a las pruebas físicas para ser un 
miembro activo y poder reservar</p> 
        <p>Te recomendamos cambiar tu contraseña al iniciar sesión por primera vez.</p> 
        """)

def usuario_ya_registrado(usuario): 
    '''Esta funcion valida si un usuario ya esta en la base de datos basado en su usuario''' 
    query = "SELECT nombre FROM personas WHERE usuario = ?" 
    conexion = Conexion() 
    respuesta = conexion.ejecutar_consulta(query, [usuario]) 
    return True if respuesta else False 

def registrar_asistencia(usuario):
    '''Registra asistencia del usuario para la sesion activa (si hay).'''
    conexion = Conexion()

    query_sesiones = """
        SELECT s.id FROM sesiones s
        JOIN reservas r ON s.id = r.sesiones_id
        WHERE r.personas_usuario = ? AND date(s.fecha) = date('now')
    """
    sesiones = conexion.ejecutar_consulta(query_sesiones, [usuario])

    if not sesiones:
        return "No hay sesiones activas hoy para este usuario."

    asistencia_registrada = False

    for sesion in sesiones:
        id_sesion = sesion[0]

        query_estado = """
            SELECT asistio FROM reservas
            WHERE sesiones_id = ? AND personas_usuario = ?
        """
        resultado = conexion.ejecutar_consulta(query_estado, [id_sesion, usuario])

        if resultado and resultado[0][0] == 0:
            query_update = """
                UPDATE reservas SET asistio = 1
                WHERE sesiones_id = ? AND personas_usuario = ?
            """
            conexion.ejecutar_consulta(query_update, [id_sesion, usuario])
            asistencia_registrada = True

    if asistencia_registrada:
        return "Asistencia registrada exitosamente."
    else:
        return "Ya se habia registrado asistencia o no habia sesiones pendientes."

def verificar_sesion_activa(actividad):
    '''Verifica si hay una sesion activa para el tipo de actividad dado'''
    query = """
        SELECT id FROM sesiones
        WHERE actividad_tipo = ? 
        AND ? >= fecha
        AND ? < datetime(fecha, '+1 hour')
    """
    conexion = Conexion()
    hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    resultado = conexion.ejecutar_consulta(query, [actividad, hora_actual, hora_actual])

    return resultado[0][0] if resultado else None
