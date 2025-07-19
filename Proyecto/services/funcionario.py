# funcionarios.py

'''Funciones de backend para el rol Funcionario''' 

from datetime import datetime, timedelta
from models import (SessionLocal,
                    t_rol_persona,
                    Personas,
                    Sesiones
                    )
from sqlalchemy import select, Time
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

def eliminar_miembro(usuario):
    '''Esta funcion permite eliminar un nuevo del el sistema'''
    with SessionLocal.begin() as session: #pylint: disable = no-member
        persona = session.get(Personas, usuario)
        session.delete(persona)

def usuario_ya_registrado(usuario):
    '''Esta funcion valida si un usuario ya esta en la base de datos basado en su usuario''' 
    with SessionLocal() as session:
        persona = session.get(Personas, usuario)

    return persona is not None

def verificar_sesion_activa(actividad):
    '''Verifica si hay una sesion activa para el tipo de actividad dado'''
    hora_acutal = datetime.now()
    with SessionLocal() as session:
        stmt = select(Sesiones.id).filter(
                                        Sesiones.fecha < hora_acutal,
                                        hora_acutal - timedelta(minutes=30) <= Sesiones.fecha,
                                        Sesiones.actividad_tipo == actividad
                                        )
        result = session.execute(stmt)
        sesion = result.scalar()

    return sesion
