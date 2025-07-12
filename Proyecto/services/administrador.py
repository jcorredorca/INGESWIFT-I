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

def recuperar_id_ubicacion(nombre_ubicacion):
    '''Esta funcion trae el id de ubicacion dado un nombre'''
    query_ubi = '''SELECT id_ubicaciones FROM ubicaciones where ubicacion = ?'''
    respuesta = Conexion().ejecutar_consulta(query_ubi, (nombre_ubicacion,))

    id_ubicacion = [ubicacion[0] for ubicacion in respuesta]
    return id_ubicacion[0]

def crear_horario(parametros):
    '''Esta funcion crea una sesion en base de datos y posteriormente
    devuelve su id\n
    parametros = [publico, fecha, actividad_tipo, ubicaciones_id_ubicaciones]'''
    query_horario = '''INSERT INTO sesiones \
                    (publico, fecha, actividad_tipo, ubicaciones_id_ubicaciones) \
                    VALUES (?, ?, ?, ?)'''
    Conexion().ejecutar_consulta(query_horario, parametros)

    query_id_horario = '''SELECT id FROM sesiones \
                    where fecha = ? AND actividad_tipo = ?'''
    id_horario = Conexion().ejecutar_consulta(query_id_horario, (parametros[1], parametros[2]))

    return id_horario[0][0]

def asignar_funcionarios(funcionarios, sesion, profesor):
    '''Esta funcion asigna los funcionarios a una determinada sesion'''

    query_rel_funcionario = '''INSERT INTO funcionarios_en_sesion \
                    (personas_usuario, sesiones_id, profesor_encargado) \
                    VALUES (?, ?, ?)'''

    for funcionario in funcionarios:
        if profesor != funcionario:
            Conexion().ejecutar_consulta(query_rel_funcionario, (funcionario, sesion, 'NO'))

    Conexion().ejecutar_consulta(query_rel_funcionario, (profesor, sesion, 'SI'))

def eliminar_sesion(id_sesion):
    '''Elimina una sesión y todas sus relaciones'''
    # Borra relaciones en funcionarios_en_sesion
    query_funcionarios = "DELETE FROM funcionarios_en_sesion WHERE sesiones_id = ?"
    Conexion().ejecutar_consulta(query_funcionarios, (id_sesion,))

    # Borra relaciones en reservas
    query_reservas = "DELETE FROM reservas WHERE sesiones_id = ?"
    Conexion().ejecutar_consulta(query_reservas, (id_sesion,))

    # Finalmente, borra la sesión
    query_sesion = "DELETE FROM sesiones WHERE id = ?"
    Conexion().ejecutar_consulta(query_sesion, (id_sesion,))

def recuperar_ubicacion_publico(id_sesion):
    '''Trae de vuelta la ubicacion y publico de determinada sesion'''
    query_ubi_publico = '''SELECT ubicaciones_id_ubicaciones, publico FROM sesiones WHERE id = ?'''
    query_ubi = '''SELECT ubicacion FROM ubicaciones WHERE id_ubicaciones = ?'''
    nombre_ubicacion = [None]
    resultado = Conexion().ejecutar_consulta(query_ubi_publico, (id_sesion,))
    ubicacion_id = resultado[0][0]
    publico = resultado[0][1]
    if ubicacion_id:
        nombre_ubicacion = Conexion().ejecutar_consulta(query_ubi, (ubicacion_id,))

    return publico, nombre_ubicacion[0][0]

def recuperar_funcionarios_en_sesion(id_sesion):
    '''Devuelve una lista de usuarios asignados a la sesión'''
    query = "SELECT personas_usuario FROM funcionarios_en_sesion WHERE sesiones_id = ?"
    resultado = Conexion().ejecutar_consulta(query, (id_sesion,))
    return [funcionario[0] for funcionario in resultado]

def recuperar_profesor_en_sesion(id_sesion):
    '''Devuelve una lista de usuarios asignados a la sesión'''
    query = "SELECT personas_usuario\
     FROM funcionarios_en_sesion WHERE sesiones_id = ? AND profesor_encargado = 'SI'"
    resultado = Conexion().ejecutar_consulta(query, (id_sesion,))
    return [funcionario[0] for funcionario in resultado]

def eliminar_funcionarios_en_sesion(id_sesion):
    '''Esta funcion elimina todos los funcionarios asociados a una sesion'''
    query_funcionarios = "DELETE FROM funcionarios_en_sesion WHERE sesiones_id = ?"
    Conexion().ejecutar_consulta(query_funcionarios, (id_sesion,))

def actualizar_publico_ubicacion(id_sesion, publico, ubicacion):
    '''Esta funcon actualiza el publico y ubicacion de una sesion'''
    id_ubicacion = recuperar_id_ubicacion(ubicacion)
    query_actualizacion = '''UPDATE sesiones
                            SET publico =?,
                            ubicaciones_id_ubicaciones =?
                            WHERE id =?;'''
    Conexion().ejecutar_consulta(query_actualizacion, (publico,  id_ubicacion, id_sesion))

def recuperar_miembros_activos() -> dict:
    '''Recupera los miembros activos del sistema'''
    query_activos = '''SELECT p.nombre, p.apellido, p.usuario
                    FROM personas p
                    JOIN rol_persona rp ON p.usuario = rp.personas_usuario
                    WHERE rp.rol_nombre = 'MIEMBRO' AND p.estado = 'ACTIVO';'''
    respuesta = Conexion().ejecutar_consulta(query_activos)
    miembros_activos = {miembro[2] : miembro[0]+' '+miembro[1] for miembro in respuesta}

    return miembros_activos

def recuperar_miembros_inactivos() -> dict:
    '''Recupera los miembros inactivos del sistema'''
    query_inactivos = '''SELECT p.nombre, p.apellido, p.usuario
                    FROM personas p
                    JOIN rol_persona rp ON p.usuario = rp.personas_usuario
                    WHERE rp.rol_nombre = 'MIEMBRO' AND p.estado = 'INACTIVO';'''
    respuesta = Conexion().ejecutar_consulta(query_inactivos)
    miembros_inactivos = {miembro[2]: miembro[0]+' '+miembro[1] for miembro in respuesta}

    return miembros_inactivos

def activar_miembros(usuarios):
    '''Esta funcion cambia el estado de los usuarios a activo'''

    query_upd_estado = '''UPDATE personas SET estado = 'ACTIVO' WHERE usuario = ?'''

    for usuario in usuarios:
        Conexion().ejecutar_consulta(query_upd_estado,[usuario])

def desactivar_miembros(usuarios):
    '''Esta funcion cambia el estado de los usuarios a inactivo'''
    query_upd_estado = '''UPDATE personas SET estado = 'INACTIVO' WHERE usuario = ?'''

    for usuario in usuarios:
        Conexion().ejecutar_consulta(query_upd_estado,[usuario])
