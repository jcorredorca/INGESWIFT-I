'''Funciones de backend para la ventana login'''
import bcrypt
from models.conexion import Conexion
from .general import enviar_correo
from models import SessionLocal, Actividad, Personas, Rol
from sqlalchemy import select, func

def hash_contrasena(contrasena: str) -> bytes:
    '''Funcion que toma un string con una contraseña y devuelve el hash correspondiente'''
    return bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt()).decode()

def autenticar_credenciales(usuario, contrasena):
    '''Esta función autentica la identidad de un usuario'''
    with SessionLocal() as session:
        stmt = select(Personas.hash_contrasena).filter(Personas.usuario == usuario)
        result = session.execute(stmt)
        hash_db = result.scalar()

    #Excepcion 1: Usuario no existe

    if len(hash_db) == 0:
        raise ValueError('El usuario o contraseña ingresado no son correctos.')

    # Excepcion 2: Usuario y contraseña no coinciden
    credenciales_coinciden = bcrypt.checkpw(contrasena.encode(), hash_db.encode())
    if not credenciales_coinciden:
        raise ValueError('El usuario o contraseña ingresado no son correctos.')

    return True

def cambiar_contrasena(usuario, nueva_contrasenia):
    '''Esta funcion permite actualizar en la db el hash de una contraseña'''
    with SessionLocal.begin() as session: #pylint: disable = no-member
        persona = session.get(Personas, usuario)
        if persona:
            persona.hash_contrasena = nueva_contrasenia

    correo = persona.correo

    enviar_correo(
        destinatario=correo[0][0],
        asunto= 'ATUN - Cambio de contraseña',
        contenido_html="""
        <h2>¡Hola!</h2>
        <p>Tu contraseña en el sistema ATUN ha sido <strong>actualizada correctamente</strong>.</p>
        <p>Si no fuiste tú o consideras que hubo un error, por favor comunicate al correo de soporte de ATUN.</p>
        """)

def recuperar_roles(usuario):
    '''Esta función recupera los posibles roles de un usuario'''
    with SessionLocal() as session:
        stmt = select(Rol.nombre).join(Personas.rol).filter(Personas.usuario == usuario)
        result = session.execute(stmt)
        roles = result.scalars().all()
    return roles
