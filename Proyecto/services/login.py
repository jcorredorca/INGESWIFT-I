'''Funciones de backend para la ventana login'''

import bcrypt
from models.conexion import Conexion
from .general import enviar_correo


def hash_contrasena(contrasena: str) -> bytes:
    '''Funcion que toma un string con una contraseña y devuelve el hash correspondiente'''
    return bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt()).decode()

def autenticar_credenciales(usuario, contrasena):
    '''Esta función autentica la identidad de un usuario'''

    query_usuario_hash = "SELECT hash_contrasena FROM personas WHERE usuario = ?"
    conexion = Conexion()

    hash_db: list = conexion.ejecutar_consulta(query_usuario_hash, [usuario])

    #Excepcion 1: Usuario no existe

    if len(hash_db) == 0:
        raise ValueError('El usuario o contraseña ingresado no son correctos.')

    # Excepcion 2: Usuario y contraseña no coinciden
    credenciales_coinciden = bcrypt.checkpw(contrasena.encode(), hash_db[0][0].encode())
    if not credenciales_coinciden:
        raise ValueError('El usuario o contraseña ingresado no son correctos.')

    return True

def cambiar_contrasena(usuario, nueva_contr):
    '''Esta funcion permite actualizar en la db el hash de una contraseña'''
    query = 'UPDATE personas SET hash_contrasena = ? WHERE usuario = ?'
    query_correo = "SELECT correo FROM personas WHERE usuario = ?"

    conexion = Conexion()
    hash_nuevo = hash_contrasena(nueva_contr)

    #Actualiza la contraseña en la db
    conexion.ejecutar_consulta(query, [hash_nuevo, usuario])

    #Consulta el correo del usuario
    correo = conexion.ejecutar_consulta(query_correo, [usuario])

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
    query = 'SELECT rol_nombre FROM rol_persona WHERE personas_usuario = ?'

    conexion = Conexion()
    roles = [rol[0] for rol in conexion.ejecutar_consulta(query, [usuario])]

    return roles
