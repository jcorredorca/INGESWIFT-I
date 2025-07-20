# funcionarios.py

'''Funciones de backend para el rol Funcionario''' 

from datetime import datetime, timedelta
from models import (SessionLocal,
                    t_rol_persona,
                    Personas,
                    Reservas,
                    Actividad,
                    Sesiones,
                    t_asistencias_extemp
                    )
from sqlalchemy import select, func
from .general import enviar_correo


def registrar_miembro(info:dict):
    '''Esta funcion permite registrar un nuevo miembro en el sistema'''
    with SessionLocal.begin() as session: #pylint: disable = no-member
        persona = session.get(Personas, info['usuario'])
        if persona:
            raise ValueError('Este usuario ya existe en la base de datos')

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

def eliminar_miembro(usuario):
    '''Esta funcion permite eliminar un nuevo del el sistema'''
    with SessionLocal.begin() as session: #pylint: disable = no-member
        persona = session.get(Personas, usuario)
        if not persona:
            raise ValueError('Este usuario no existe en la base de datos')
        persona = session.get(Personas, usuario)
        session.delete(persona)

def usuario_ya_registrado(usuario):
    '''Esta funcion valida si un usuario ya esta en la base de datos basado en su usuario'''
    with SessionLocal() as session:
        stmt = select(Personas.nombre).filter(Personas.usuario == usuario)
        result = session.execute(stmt)
        nombre = result.scalar()

    return nombre is not None

def registrar_asistencia(miembro, sesion, codigo):
    '''Registra asistencia del usuario para la sesion activa (si hay).'''
    with SessionLocal() as session:
        reserva = session.get(Reservas, codigo)
        if reserva:
            usuario = reserva.personas_usuario
            sesion_reserva = reserva.sesiones_id
            asistencia_registrada = reserva.asistio
        else:
            return False, 'El código de reserva es inválido'

    if usuario != miembro:
        return False, 'El usuario no corresponde con el de la reserva.'

    if sesion_reserva != sesion:
        return False, 'La reserva no es válida para esta sesión.'

    if asistencia_registrada == 1:
        return False, 'Ya se registró la asistencia de esta reserva.'

    with SessionLocal.begin() as session: #pylint: disable = no-member
        if reserva:
            reserva.asistio = 1

    return True, 'Asistencia registrada exitosamente'

def registro_extemporaneo(usuario, sesion):
    '''Funcion para registrar un miembro que accede de forma extemporanea'''
    with SessionLocal() as session:
        stmt = select(
                    Personas.nombre
                    ).filter(Personas.usuario == usuario,
                            Personas.estado == 'ACTIVO')
        result = session.execute(stmt)
        nombre = result.scalar()

        if not nombre:
            return False, 'El usuario no está registrado en el sistema o no está activo'

        stmt = select(
                    Reservas.codigo
                    ).filter(Reservas.personas_usuario == usuario,
                            Reservas.sesiones_id == sesion,
                            Reservas.asistio == 1)
        result = session.execute(stmt)
        asistencia_reserva = result.scalar()


        stmt = select(t_asistencias_extemp.c.personas_usuario).select_from( #pylint: disable=not-callable
                                t_asistencias_extemp).where(
                                    t_asistencias_extemp.c.sesiones_id == sesion,
                                    t_asistencias_extemp.c.personas_usuario == usuario)
        result = session.execute(stmt)
        asistencia_extemp = result.scalar()

        if asistencia_reserva or asistencia_extemp:
            return False, "El usuario ya está registrado en esta sesión"

    with SessionLocal.begin() as session: #pylint: disable = no-member
        stmt = t_asistencias_extemp.insert().values(personas_usuario=usuario, sesiones_id=sesion)
        return True, 'La asistencia se registró correctamente'

def verificar_sesion_activa(actividad):
    '''Verifica si hay una sesion activa para el tipo de actividad dado'''
    hora_acutal = datetime.now()
    with SessionLocal() as session:
        stmt = select(Sesiones.id).filter(
                                        Sesiones.fecha < hora_acutal + timedelta(minutes=55),
                                        hora_acutal - timedelta(minutes=55) <= Sesiones.fecha,
                                        Sesiones.actividad_tipo == actividad
                                        )
        result = session.execute(stmt)
        sesion = result.scalar()

    return sesion

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
