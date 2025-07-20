'''Funcionalidades especificas para administradores'''
from models import (SessionLocal,
                    Ubicaciones, Sesiones,
                    FuncionariosEnSesion,Personas,
                    Rol, Reservas
                    )
from sqlalchemy import select

def recuperar_funcionarios():
    '''Esta funcion recupera todos los funcionarios del sistema'''
    with SessionLocal() as session:
        stmt = select(
                    Personas.nombre,
                    Personas.apellido,
                    Personas.usuario
                    ).join(Personas.rol).filter(Rol.nombre == 'FUNCIONARIO')
        result = session.execute(stmt)
        funcionarios = result.all()

    return [[funcionario[0]+' '+funcionario[1],funcionario[2]] for funcionario in funcionarios]

def recuperar_ubicaciones():
    '''Esta funcion recupera todas las ubicaciones del sistema'''
    with SessionLocal() as session:
        stmt = select(Ubicaciones.ubicacion)
        result = session.execute(stmt)
        ubicaciones = result.scalars().all()
        return ubicaciones

def recuperar_id_ubicacion(nombre_ubicacion):
    '''Esta funcion trae el id de ubicacion dado un nombre'''
    with SessionLocal() as session:
        stmt = select(Ubicaciones.id_ubicaciones).filter(Ubicaciones.ubicacion == nombre_ubicacion)
        result = session.execute(stmt)
        id_ubicacion = result.scalar()
        return id_ubicacion

def crear_horario(parametros):
    '''Esta funcion crea una sesion en base de datos y posteriormente
    devuelve su id\n
    parametros = [publico, fecha, actividad_tipo, ubicaciones_id_ubicaciones]'''
    with SessionLocal.begin() as session: #pylint: disable = no-member
        nueva_sesion = Sesiones(
            publico = parametros[0],
            fecha = parametros[1],
            actividad_tipo = parametros[2],
            ubicaciones_id_ubicaciones = parametros[3]
                                )
        session.add(nueva_sesion)
        session.flush()
        id_sesion = nueva_sesion.id
    return id_sesion

def asignar_funcionarios(funcionarios, sesion, profesor):
    '''Esta funcion asigna los funcionarios a una determinada sesion'''

    with SessionLocal.begin() as session: #pylint: disable = no-member
        for funcionario in funcionarios:
            if profesor != funcionario:
                nuevo_funcionario = FuncionariosEnSesion(
                    personas_usuario = funcionario,
                    sesiones_id = sesion,
                    profesor_encargado = 'NO'
                    )
                session.add(nuevo_funcionario)
        nuevo_profesor = FuncionariosEnSesion(
                    personas_usuario = profesor,
                    sesiones_id = sesion,
                    profesor_encargado = 'SI'
                    )
        session.add(nuevo_profesor)

def eliminar_sesion(id_sesion):
    '''Elimina una sesión y todas sus relaciones'''

    with SessionLocal.begin() as session: #pylint: disable = no-member
        sesion = session.get(Sesiones, id_sesion)
        if sesion:
            session.query(FuncionariosEnSesion).filter(
                                                FuncionariosEnSesion.sesiones_id == id_sesion
                                                ).delete()
            session.query(Reservas).filter(
                                            Reservas.sesiones_id == id_sesion
                                            ).delete()
            session.query(Sesiones).filter(
                                            Sesiones.id == id_sesion
                                            ).delete()

def recuperar_ubicacion_publico(id_sesion):
    '''Trae de vuelta la ubicacion y publico de determinada sesion'''
    with SessionLocal() as session:
        stmt = select(Sesiones.publico,
                    Ubicaciones.ubicacion
                    ).join(Ubicaciones).filter(Sesiones.id == id_sesion)
        result = session.execute(stmt)
        publico_ubicacion = result.all()

    return publico_ubicacion[0]

def recuperar_funcionarios_en_sesion(id_sesion):
    '''Devuelve una lista de usuarios asignados a la sesión'''
    with SessionLocal() as session:
        stmt = select(FuncionariosEnSesion.personas_usuario
                    ).filter(
                        FuncionariosEnSesion.sesiones_id == id_sesion,
                        FuncionariosEnSesion.profesor_encargado == 'NO'
                        )
        result = session.execute(stmt)
        funcionarios_en_sesion = result.scalars().all()

    return funcionarios_en_sesion

def recuperar_profesor_en_sesion(id_sesion):
    '''Devuelve una lista de usuarios asignados a la sesión'''
    with SessionLocal() as session:
        stmt = select(FuncionariosEnSesion.personas_usuario
                    ).filter(
                        FuncionariosEnSesion.sesiones_id == id_sesion,
                        FuncionariosEnSesion.profesor_encargado == 'SI'
                        )
        result = session.execute(stmt)
        profesor_en_sesion = result.first()

    return profesor_en_sesion

def eliminar_funcionarios_en_sesion(id_sesion):
    '''Esta funcion elimina todos los funcionarios asociados a una sesion'''
    with SessionLocal.begin() as session: #pylint: disable = no-member
        sesion = session.get(Sesiones, id_sesion)
        if sesion:
            session.query(FuncionariosEnSesion).filter(
                                                FuncionariosEnSesion.sesiones_id == id_sesion
                                                ).delete()

def actualizar_publico_ubicacion(id_sesion, publico, ubicacion):
    '''Esta funcon actualiza el publico y ubicacion de una sesion'''
    id_ubicacion = recuperar_id_ubicacion(ubicacion)
    with SessionLocal.begin() as session: #pylint: disable = no-member
        sesion = session.get(Sesiones, id_sesion)
        if sesion:
            sesion.publico = publico
            sesion.ubicaciones_id_ubicaciones = id_ubicacion

def recuperar_miembros_activos() -> dict:
    '''Recupera los miembros activos del sistema'''
    with SessionLocal() as session:
        stmt = select(
                    Personas.nombre,
                    Personas.apellido,
                    Personas.usuario
                    ).join(Personas.rol).filter(Rol.nombre == 'MIEMBRO',
                                                Personas.estado == 'ACTIVO')
        result = session.execute(stmt)
        miembros = result.all()

    miembros_activos = {miembro[2] : miembro[0]+' '+miembro[1] for miembro in miembros}

    return miembros_activos

def recuperar_miembros_inactivos() -> dict:
    '''Recupera los miembros inactivos del sistema'''
    with SessionLocal() as session:
        stmt = select(
                    Personas.nombre,
                    Personas.apellido,
                    Personas.usuario
                    ).join(Personas.rol).filter(Rol.nombre == 'MIEMBRO',
                                                Personas.estado == 'INACTIVO')
        result = session.execute(stmt)
        miembros = result.all()

    miembros_inactivos = {miembro[2] : miembro[0]+' '+miembro[1] for miembro in miembros}

    return miembros_inactivos

def activar_miembros(usuarios):
    '''Esta funcion cambia el estado de los usuarios a activo'''
    with SessionLocal.begin() as session: #pylint: disable = no-member
        for usuario in usuarios:
            miembro = session.get(Personas, usuario)
            if miembro:
                miembro.estado = 'ACTIVO'

def desactivar_miembros(usuarios):
    '''Esta funcion cambia el estado de los usuarios a inactivo'''
    with SessionLocal.begin() as session: #pylint: disable = no-member
        for usuario in usuarios:
            miembro = session.get(Personas, usuario)
            if miembro:
                miembro.estado = 'INACTIVO'
