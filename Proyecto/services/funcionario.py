# funcionarios.py

'''Funciones de backend para el rol Funcionario''' 

from datetime import datetime
from models import (SessionLocal,
                    t_rol_persona,
                    Personas,
                    Reservas,
                    Actividad,
                    Sesiones,
                    t_asistencias_extemp
                    )
from sqlalchemy import select, func
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

def registrar_asistencia(miembro, sesion, codigo):
    '''Registra asistencia del usuario para la sesion activa (si hay).'''
    conexion = Conexion()

    query_verificacion_reserva = "SELECT personas_usuario, sesiones_id, asistio FROM reservas WHERE codigo = ?" #pylint: disable=line-too-long
    query_asistencia = "UPDATE reservas SET asistio=1 WHERE codigo = ?"

    respuesta = conexion.ejecutar_consulta(query_verificacion_reserva, [codigo])

    #Verficia que el codigo de reserva sea real
    if respuesta:
        usuario = respuesta[0][0]
        sesion_reserva = respuesta[0][1]
        asistencia_registrada = respuesta[0][2]
    else:
        return False, 'El código de reserva es inválido'

    if usuario != miembro:
        return False, 'El usuario no corresponde con el de la reserva.'

    if sesion_reserva != sesion:
        return False, 'La reserva no es válida para esta sesión.'

    if asistencia_registrada == 1:
        return False, 'Ya se registró la asistencia de esta reserva.'

    conexion.ejecutar_consulta(query_asistencia, [codigo])
    return True, 'Asistencia registrada exitosamente'

def registro_extemporaneo(usuario, sesion):
    '''Funcion para registrar un miembro que accede de forma extemporanea'''
    query_verificacion1 = "SELECT nombre FROM personas WHERE usuario = ? AND estado = ACTIVO"
    query_verificacion2 = '''
    SELECT * FROM reservas 
    WHERE personas_usuario = ? 
    AND sesiones_id = ? 
    AND asistio = 1'''
    query_verificacion3 = '''
    SELECT * FROM asistencias_extemp 
    WHERE personas_usuario = ? AND sesiones_id = ?'''
    query_asistencia= "INSERT INTO asistencias_extemp (personas_usuario, sesiones_id) VALUES (?, ?)"

    conexion = Conexion()

    respuesta = conexion.ejecutar_consulta(query_verificacion1, [usuario])
    if not respuesta:
        return False, 'El usuario no está registrado en el sistema o no está activo'

    respuesta_reserva = conexion.ejecutar_consulta(query_verificacion2, [usuario, sesion])
    respuesta_extemp = conexion.ejecutar_consulta(query_verificacion3, [usuario, sesion])
    if respuesta_reserva or respuesta_extemp:
        return False, "El usuario ya está registrado en esta sesión"

    conexion.ejecutar_consulta(query_asistencia, [usuario, sesion])
    return True, 'La asistencia se registró correctamente'

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

def hay_cupos_disponibles(id_sesion):
    '''Esta funcion revisa la cantidad de cupos disponibles para determinada sesion
    Retorna:
        True  → hay cupo disponible o es aforo ilimitado.
        False → el aforo ya está completo.'''

    with SessionLocal() as session:
        stmt = select(Actividad.aforo).join(Sesiones).filter(Sesiones.id == id_sesion)
        result = session.execute(stmt)
        aforo = result.scalars().all()

    aforo = aforo[0]
    if aforo == -1:
        return True

    with SessionLocal() as session:
        stmt = select(func.count(Reservas.codigo)).filter( #pylint: disable = not-callable
                                                        Reservas.sesiones_id == id_sesion,
                                                        )
        result = session.execute(stmt)
        total_reservas = result.scalar_one()

    with SessionLocal() as session:
        stmt = select(func.count()).select_from( #pylint: disable=not-callable
            t_asistencias_extemp).where( t_asistencias_extemp.c.sesiones_id == id_sesion)
        result = session.execute(stmt)
        asistencias_adicionales = result.scalar_one()

    return (total_reservas + asistencias_adicionales) < aforo

def recuperar_cupos(sesion):
    '''Este metodo recupera el numero de cupos disponibles para una sesion'''

    with SessionLocal() as session:
        stmt = select(Actividad.aforo).join(Sesiones).filter(Sesiones.id == sesion)
        result = session.execute(stmt)
        aforo = result.scalar_one()

    if aforo == -1:
        return 'SIN RESERVA'

    with SessionLocal() as session:
        stmt = select(func.count(Reservas.codigo)).filter(#pylint: disable = not-callable
                                                        Reservas.sesiones_id == sesion,
                                                        Reservas.asistio == 1
                                                        )
        result = session.execute(stmt)
        asistencias_reserva = result.scalar_one()

    with SessionLocal() as session:
        stmt = select(func.count()).select_from( #pylint: disable=not-callable
            t_asistencias_extemp).where( t_asistencias_extemp.c.sesiones_id == sesion)
        result = session.execute(stmt)
        asistencias_adicionales = result.scalar_one()

    return aforo - (asistencias_reserva + asistencias_adicionales)
