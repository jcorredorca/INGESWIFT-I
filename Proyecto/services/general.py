'''Servicios generales de la app'''
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from models.conexion import Conexion
from config import API_KEY
from models.db import SessionLocal
from models.modelos import Actividad, Sesiones
from sqlalchemy import select

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
        stmt = select(Sesiones.id).filter(Sesiones.actividad_tipo == plan, Sesiones.fecha == fecha_hora)
        result = session.execute(stmt)
        ids = result.scalars().all()
    if ids:
        return ids[0]
    return False
