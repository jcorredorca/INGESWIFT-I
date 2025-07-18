'''Funcionalidades especificas para miembros'''
from hashlib import sha256
from datetime import datetime, timedelta
from models import (SessionLocal,
                    Reservas, Sesiones,
                    Personas,Reservas
                    )
from sqlalchemy import select
from .general import enviar_correo

def recuperar_estado(usuario):
    '''Esta funcion recupera el estado de un miembro'''
    with SessionLocal() as session:
        stmt = select(
                    Personas.estado
                    ).filter(Personas.usuario == usuario)
        resultado = session.execute(stmt)
        estado = resultado.scalar()
    return estado

def buscar_reserva(usuario, sesion):
    '''Esta funcion recupera la reserva de un miembro a una sesion  '''
    with SessionLocal() as session:
        stmt = select(Reservas.codigo).filter(
                                        Reservas.personas_usuario == usuario,
                                        Reservas.sesiones_id == sesion)
        resultado = session.execute(stmt)
        codigo = resultado.scalar()
    if codigo:
        return codigo
    return False

def generar_codigo_reserva(usuario: str, id_sesion: int) -> str:
    '''
    Genera un código único de reserva combinando el hash del usuario y el ID de sesión.
    '''
    # Hash del usuario (obtenemos los primeros 8 caracteres del hash hexadecimal)
    hash_usuario = sha256(usuario.encode()).hexdigest()[:5]

    # Concatenamos el hash corto con el ID
    codigo = f"{hash_usuario}{id_sesion}"

    return codigo

def crear_reserva(codigo, sesion, usuario):
    '''Esta funcion crea una nueva reserva para el codigo dado'''
    with SessionLocal.begin() as session: #pylint: disable = no-member
        nueva_reserva = Reservas(
            codigo = codigo,
            sesiones_id = sesion,
            personas_usuario = usuario
            )
        session.add(nueva_reserva)
        stmt = select(Personas.correo).filter(Personas.usuario == usuario)
        resultado = session.execute(stmt)
        correo = resultado.scalar()

    enviar_correo(correo[0][0], 'ATUN - Confirmación de reserva',
        contenido_html=f"""
        <h2>¡Hola!</h2>
        <p>Tu reserva en el sistema ATUN ha sido <strong>registrada correctamente</strong>.</p>
        <p>Tu código de acceso es: <strong>{codigo}</strong>.</p>
        <p>Recuerda presentarlo antes de entrar a la sesión para la que reservaste</p>
        """ )

def eliminar_reserva(codigo):
    '''Esta funcion crea una nueva reserva para el codigo dado'''
    with SessionLocal.begin() as session: #pylint: disable = no-member
        reserva = session.get(Reservas, codigo)
        if reserva:
            session.delete(reserva)

def sesion_disponible(sesion):
    '''Esta funcion confirma si una sesion esta dentro del
    rango de dos horas a partir ahora'''
    with SessionLocal() as session:
        stmt = select(Sesiones.fecha).filter(Sesiones.id == sesion)
        resultado = session.execute(stmt)
        fecha = resultado.scalar()

    if not fecha:
        return False

    fecha_sesion = fecha

    ahora = datetime.now()
    dos_horas_despues = ahora + timedelta(hours=2)

    return ahora <= fecha_sesion <= dos_horas_despues


def rol_sesion(usuario, id_sesion):
    '''Revisa que el rol de la persona sea el apropiado para la sesion
    roles: 'GENERAL', 'FUNCIONARIO', 'FODUN', 'CUIDADO')'''
    with SessionLocal() as session:
        stmt = select(Sesiones.publico).filter(Sesiones.id == id_sesion)
        resultado = session.execute(stmt)
        publico = resultado.scalar()

    if publico == 'GENERAL':
        return True

    with SessionLocal() as session:
        stmt = select(Personas.rol_en_universidad).filter(Personas.usuario == usuario)
        resultado = session.execute(stmt)
        rol = resultado.scalar()

    return rol == publico
