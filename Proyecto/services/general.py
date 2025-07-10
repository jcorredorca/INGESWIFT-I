'''Servicios generales de la app'''
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from models.conexion import Conexion
from config import API_KEY

def recuperar_actividades():
    '''Esta funcion recupera los tipos de actividad ofertados'''

    query_actividades = "SELECT tipo FROM actividad"
    respuesta = Conexion().ejecutar_consulta(query_actividades)
    actividades = [actividad[0] for actividad in respuesta]

    return actividades

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

