import os
from pprint import pprint

import sib_api_v3_sdk
from dotenv import load_dotenv
from sib_api_v3_sdk.rest import ApiException

# Carga las credenciales desde .env
load_dotenv()
API_KEY = os.getenv("BREVO_API_KEY")

def enviar_correo(destinatario, asunto, contenido_html):
    # Configurar la autenticación
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = API_KEY

    # Instanciar API
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Crear estructura del correo
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": destinatario, "name": "Usuario ATUN"}],
        sender={"name": "ATUN", "email": "jcorredorca@unal.edu.co"},
        subject=asunto,
        html_content=contenido_html
    )

    # Enviar correo
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("Correo enviado:")
        pprint(api_response)
    except ApiException as e:
        print("Error al enviar correo: %s\n" % e)

if __name__ == "__main__":
    #print("API KEY =", API_KEY)
    enviar_correo(
        destinatario="nbolanosf@unal.edu.co",
        asunto="Penalización",
        contenido_html="""
        <h2>¡Hola!</h2>
        <p>Tu estado en el sistema ATUN ha sido actualizado a <strong>penalizado</strong> por 48 horas.</p>
        <p>Recuerda asistir puntualmente a tus próximas sesiones.</p>
        """
    )
    enviar_correo(
        destinatario="sfetecua@unal.edu.co",
        asunto="¡Cupo disponible en tu clase de interés!",
        contenido_html="""
        <h3>¡Buenas noticias!</h3>
        <p>Se ha liberado un cupo en la clase que marcaste como favorita.</p>
        <p>Ingresa al sistema ATUN y reserva antes de que se agote.</p>
        """
    )
    enviar_correo(
        destinatario="lalvarezla@unal.edu.co",
        asunto="¡Cupo disponible en tu clase de interés!",
        contenido_html="""
        <h3>¡Buenas noticias!</h3>
        <p>Se ha liberado un cupo en la clase que marcaste como favorita.</p>
        <p>Ingresa al sistema ATUN y reserva antes de que se agote.</p>
        """
    )