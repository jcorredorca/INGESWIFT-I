'''Servicios generales de la app'''
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from config import API_KEY
from models import SessionLocal, Actividad, Sesiones, Reservas
from sqlalchemy import select, func

def recuperar_actividades():
    '''Esta funcion recupera los tipos de actividad ofertados'''
    with SessionLocal() as session:
        stmt = select(Actividad.tipo)
        result = session.execute(stmt)
        tipos = result.scalars().all()
    return tipos

def enviar_correo(destinatario, asunto, contenido_html):
    '''
    Esta función se encarga de mandar un correo.
    '''
    # Configurar la autenticación
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = API_KEY

    # Instanciar API
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Crear estructura del correo
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": destinatario, "name": "Usuario ATUN"}],
        sender={"name": "ATUN", "email": "atun.bog@gmail.com"},
        subject=asunto,
        html_content=contenido_html
    )

    # Enviar correo
    try:
        api_instance.send_transac_email(send_smtp_email)
    except ApiException as e:
        print(f"Error al enviar correo: {str(e)}\n")

def hay_sesiones(plan, fecha_hora):
    '''Devuelve el id de la sesión si existe
    una sesión para ese plan y fecha, o False si no existe'''
    with SessionLocal() as session:
        stmt = select(Sesiones.id).filter(
                                        Sesiones.actividad_tipo == plan).filter(
                                        Sesiones.fecha == fecha_hora
                                        )
        result = session.execute(stmt)
        ids = result.scalars().all()
    if ids:
        return ids[0]
    return False

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
        stmt = select(func.count(Reservas.codigo)).filter(Reservas.sesiones_id == id_sesion) #pylint: disable = not-callable
        result = session.execute(stmt)
        total_reservas = result.scalar_one()
    return total_reservas < aforo

def recuperar_cupos(sesion):
    '''Este metodo recupera el numero de cupos disponibles para una sesion'''

    with SessionLocal() as session:
        stmt = select(Actividad.aforo).join(Sesiones).filter(Sesiones.id == sesion)
        result = session.execute(stmt)
        aforo = result.scalar_one()

    if aforo == -1:
        return 'SIN RESERVA'

    with SessionLocal() as session:
        stmt = select(func.count(Reservas.codigo)).filter(Reservas.sesiones_id == sesion) #pylint: disable = not-callable
        result = session.execute(stmt)
        total_reservas = result.scalar_one()

    return aforo - total_reservas
