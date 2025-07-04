'''Funciones de backend para la ventana login'''

import bcrypt
from .conexion import Conexion
from Miembros import miembros
from Funcionarios import modulo_asistencia
#from Administrador import ...


def hash_contrasena(contrasena: str) -> bytes:
    '''Funcion que toma un string con una contraseña y devuelve el hash correspondiente'''
    return bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt()).decode()

def autenticar_credenciales(usuario, contrasena, rol):
    '''Esta función autentica la identidad de un usuario'''

    query_usuario_hash = "SELECT hash_contrasena FROM personas WHERE usuario = %s"
    query_rol = "SELECT rol_nombre FROM rol_persona WHERE personas_usuario = %s"

    conexion = Conexion()

    hash_db: list = conexion.ejecutar_consulta(query_usuario_hash, [usuario])

    #Excepcion 1: Usuario no existe

    if len(hash_db) == 0:
        raise ValueError('El usuario o contraseña ingresado no son correctos.')

    # Excepcion 2: Usuario y contraseña no coinciden
    credenciales_coinciden = bcrypt.checkpw(contrasena.encode(), hash_db[0][0].encode())
    if not credenciales_coinciden:
        raise ValueError('El usuario o contraseña ingresado no son correctos.')


    #Excepcion 3: Usuario y rol no coinciden
    rol_db = conexion.ejecutar_consulta(query_rol, [usuario])
    if (rol,) not in rol_db:
        raise ValueError('El usuario no cuenta con este rol.')

    return True

def cambiar_contrasena(usuario, nueva_contr):
    '''Esta funcion permite actualizar en la db el hash de una contraseña'''
    query = 'UPDATE personas SET hash_contrasena = %s WHERE usuario = %s'

    conexion = Conexion()
    hash_nuevo = hash_contrasena(nueva_contr)

    conexion.ejecutar_consulta(query, [hash_nuevo, usuario])

def recuperar_roles():
    '''Esta función recupera los posibles roles de un usuario'''
    query = 'SELECT nombre FROM rol'

    conexion = Conexion()
    roles = [rol[0] for rol in conexion.ejecutar_consulta(query)]

    return roles

def construir_ventana(rol, origen):
    '''Esta ventana construye la ventana de cada rol para ser redirigido luego del login'''
    ventanas = {
        'MIEMBRO': miembros.Miembros,
        'FUNCIONARIO': modulo_asistencia.ModuloAsistencia,
        'ADMINISTRADOR': None #TODO poner pagina principal de ADMIN (JUAN PABLO)
    }
    return ventanas[rol](origen)
