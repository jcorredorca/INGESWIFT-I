# funcionarios.py

'''Funciones de backend para el rol Funcionario''' 

from models.conexion import Conexion 
from .general import enviar_correo 

def registrar_miembro(info:dict): 
    '''Esta funcion permite registrar un nuevo miembro en el sistema''' 
    query_personas = "INSERT INTO personas \
        (usuario, nombre, apellido, hash_contrasena, correo, rol_en_universidad, grupo_especial) \
        VALUES (?, ?, ?, ?, ?, ?, ?)" 
    query_rol_persona = "INSERT INTO rol_persona \
        (personas_usuario, rol_nombre) VALUES (?, 'MIEMBRO')" 
    datos = [info[i] for i in info.keys()] 

    conexion = Conexion() 
    conexion.ejecutar_consulta(query_personas, datos) 
    conexion.ejecutar_consulta(query_rol_persona, [info['usuario']]) 

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

