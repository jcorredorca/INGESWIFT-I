'''Funcionalidades especificas para administradores'''
from models.conexion import Conexion

def recuperar_funcionarios():
    '''Esta funcion recupera todos los funcionarios del sistema'''

    query_funcionarios = '''SELECT p.nombre, p.apellido, p.usuario
                        FROM personas p
                        JOIN rol_persona rp ON p.usuario = rp.personas_usuario
                        WHERE rp.rol_nombre = 'FUNCIONARIO';'''
    respuesta = Conexion().ejecutar_consulta(query_funcionarios)
    funcionarios = [[funcionario[0]+' '+funcionario[1],funcionario[2]] for funcionario in respuesta]

    return funcionarios

def recuperar_ubicaciones():
    '''Esta funcion recupera todas las ubicaciones del sistema'''
    query_ubicaciones= '''SELECT ubicacion FROM ubicaciones;'''
    respuesta = Conexion().ejecutar_consulta(query_ubicaciones)
    ubicaciones = [ubicacion[0] for ubicacion in respuesta]

    return ubicaciones
