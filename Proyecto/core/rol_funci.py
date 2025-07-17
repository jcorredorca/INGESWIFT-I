'''Funciones de backend para el rol Funcionario'''
import sqlite3
from datetime import datetime

from config import DB_PATH
from views.funcionarios import (modulo_asistencia, registro_extemporaneo,
                                registro_miembro, sesion_cerrada)


def redirigir_pantalla_miembros(origen):
    '''Esta función construye la ventana para registrar miembros'''
    ventana = registro_miembro.RegistroMiembro(origen)
    origen.contenido.destroy()
    origen.contenido = ventana
    origen.contenido.grid(row=1, column=0, sticky="nsew")

def redirigir_pantalla_asistencia(origen):
    '''Esta función construye la ventana para gestionar a los funcionarios'''
    ventana = modulo_asistencia.ModuloAsistencia(origen)
    origen.contenido.destroy()
    origen.contenido = ventana
    origen.contenido.grid(row=1, column=0, sticky="nsew")

def redirigir_pantalla_registro_extemporaneo(origen):
    '''Esta función construye la ventana para registro extemporáneo'''
    cupos_disponibles = obtener_cupos_disponibles_sesion_actual()
    ventana = registro_extemporaneo.RegistroExtemporaneo(origen, cupos=cupos_disponibles)
    origen.contenido.destroy()
    origen.contenido = ventana
    origen.contenido.grid(row=1, column=0, sticky="nsew")

def redirigir_pantalla_sesion_cerrada(origen):
    '''Esta función construye la ventana para sesión cerrada'''
    ventana = sesion_cerrada.SesionCerrada(origen)
    origen.contenido.destroy()
    origen.contenido = ventana
    origen.contenido.grid(row=1, column=0, sticky="nsew")

def obtener_sesion_actual():
    '''Obtiene la sesión actual basada en la hora y fecha'''
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Obtener la hora actual
        hora_actual = datetime.now().hour
        fecha_actual = datetime.now().date()

        # Buscar sesión que corresponda a la hora actual
        cursor.execute("""
            SELECT s.id, a.aforo, s.publico, s.fecha, a.tipo
            FROM sesiones s
            JOIN actividad a ON s.actividad_tipo = a.tipo
            WHERE strftime('%H', s.fecha) = ? 
            AND date(s.fecha) = ?
            LIMIT 1
        """, (str(hora_actual).zfill(2), fecha_actual))

        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            return {
                'id': resultado[0],
                'aforo': resultado[1],
                'publico': resultado[2],
                'fecha': resultado[3],
                'tipo_actividad': resultado[4]
            }
        return None

    except Exception as e:
        print(f"Error obteniendo sesión actual: {e}")
        return None

def obtener_cupos_disponibles_sesion_actual():
    '''Obtiene el número de cupos disponibles para la sesión actual'''
    sesion = obtener_sesion_actual()
    if not sesion:
        return 0

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Contar reservas para la sesión actual
        cursor.execute("""
            SELECT COUNT(*) 
            FROM reservas 
            WHERE sesiones_id = ?
        """, (sesion['id'],))

        reservas_actuales = cursor.fetchone()[0]
        conn.close()

        # Si el aforo es -1, significa cupos ilimitados
        if sesion['aforo'] == -1:
            return 999  # Número alto para representar "ilimitado"

        cupos_disponibles = max(0, sesion['aforo'] - reservas_actuales)
        return cupos_disponibles

    except Exception as e:
        print(f"Error obteniendo cupos disponibles: {e}")
        return 0

def verificar_cupos_disponibles():
    '''Verifica si hay cupos disponibles en la sesión actual'''
    cupos = obtener_cupos_disponibles_sesion_actual()
    return cupos > 0

def verificar_cupos_llenos():
    '''Verifica si todos los cupos están llenos'''
    return not verificar_cupos_disponibles()

def registrar_asistencia(usuario, codigo_reserva):
    '''Registra la asistencia de un usuario con su código de reserva'''
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Verificar que existe la reserva y coincide con el usuario
        cursor.execute("""
            SELECT r.codigo, r.sesiones_id, p.usuario
            FROM reservas r
            JOIN personas p ON r.personas_usuario = p.usuario
            WHERE r.codigo = ? AND p.usuario = ?
        """, (codigo_reserva, usuario))

        reserva = cursor.fetchone()

        if not reserva:
            conn.close()
            return False, "Reserva no encontrada o usuario incorrecto"

        # Registrar en funcionarios_en_sesion (asistencia confirmada)
        cursor.execute("""
            INSERT OR REPLACE INTO funcionarios_en_sesion 
            (personas_usuario, sesiones_id, profesor_encargado)
            VALUES (?, ?, 'NO')
        """, (usuario, reserva[1]))

        # Registrar en logs
        cursor.execute("""
            INSERT INTO logs (operacion, tabla, time_stamp, personas_usuario)
            VALUES ('ins', 'funcionarios_en_sesion', ?, ?)
        """, (datetime.now(), usuario))

        conn.commit()
        conn.close()

        return True, "Asistencia registrada exitosamente"

    except Exception as e:
        print(f"Error registrando asistencia: {e}")
        return False, f"Error en el sistema: {e}"

def registrar_extemporaneo(usuario):
    '''Registra un usuario de forma extemporánea'''
    try:
        # Verificar que hay cupos disponibles
        if not verificar_cupos_disponibles():
            return False, "No hay cupos disponibles"

        sesion = obtener_sesion_actual()
        if not sesion:
            return False, "No hay sesión activa"

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Verificar que el usuario existe
        cursor.execute("SELECT usuario FROM personas WHERE usuario = ?", (usuario,))
        if not cursor.fetchone():
            conn.close()
            return False, "Usuario no encontrado"

        # Generar código de reserva único
        import random
        import string
        codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

        # Crear reserva
        cursor.execute("""
            INSERT INTO reservas (codigo, sesiones_id, personas_usuario)
            VALUES (?, ?, ?)
        """, (codigo, sesion['id'], usuario))

        # Registrar asistencia directamente
        cursor.execute("""
            INSERT INTO funcionarios_en_sesion 
            (personas_usuario, sesiones_id, profesor_encargado)
            VALUES (?, ?, 'NO')
        """, (usuario, sesion['id']))

        # Registrar en logs
        cursor.execute("""
            INSERT INTO logs (operacion, tabla, time_stamp, personas_usuario)
            VALUES ('ins', 'reservas', ?, ?)
        """, (datetime.now(), usuario))

        conn.commit()
        conn.close()

        return True, f"Registro extemporáneo exitoso. Código: {codigo}"

    except Exception as e:
        print(f"Error en registro extemporáneo: {e}")
        return False, f"Error en el sistema: {e}"
