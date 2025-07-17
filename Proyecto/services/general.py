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

def hay_sesiones(plan, fecha_hora):
    '''Devuelve el id de la sesión si existe
    una sesión para ese plan y fecha, o False si no existe'''
    query = '''SELECT id FROM sesiones WHERE actividad_tipo = ? AND fecha = ?'''
    resultado = Conexion().ejecutar_consulta(query, (plan, fecha_hora))
    if resultado:
        return resultado[0][0]

    return False

def hay_cupos_disponibles(id_sesion):
    '''Esta funcion revisa la cantidad de cupos disponibles para determinada sesion
    Retorna:
        True  → hay cupo disponible o es aforo ilimitado.
        False → el aforo ya está completo.'''

    query_cupos = '''SELECT actividad.aforo
        FROM sesiones
        JOIN actividad ON sesiones.actividad_tipo = actividad.tipo
        WHERE sesiones.id = ?'''

    respuesta = Conexion().ejecutar_consulta(query_cupos, (id_sesion,))
    aforo = respuesta[0][0]
    if aforo == -1:
        return True
    query_reservas = '''SELECT COUNT(*)
        FROM reservas
        WHERE sesiones_id = ?'''
    respuesta = Conexion().ejecutar_consulta(query_reservas, (id_sesion,))
    reservas = respuesta[0][0]
    return reservas < aforo

def recuperar_cupos(sesion):
    '''Este metodo recupera el numero de cupos disponibles para una sesion'''
    query_cupos = '''SELECT actividad.aforo
        FROM sesiones
        JOIN actividad ON sesiones.actividad_tipo = actividad.tipo
        WHERE sesiones.id = ?'''

    respuesta = Conexion().ejecutar_consulta(query_cupos, (sesion,))
    aforo = respuesta[0][0]
    if aforo == -1:
        return 'SIN RESERVA'
    query_reservas = '''SELECT COUNT(*)
        FROM reservas
        WHERE sesiones_id = ?'''
    respuesta = Conexion().ejecutar_consulta(query_reservas, (sesion,))
    reservas = respuesta[0][0]
    return aforo - reservas