import sqlite3
from datetime import datetime, timedelta
from config import DB_PATH
from services import login

def create_afid_test():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    con1 = login.hash_contrasena('123')

    # Insert personas
    cursor.executemany("INSERT INTO personas (usuario, nombre, apellido, hash_contrasena, estado, correo, rol_en_universidad, grupo_especial) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [
        ('user1', 'Ana', 'García', con1, 'ACTIVO', 'ana@example.com', 'GENERAL', 'JOVENES'),
        ('user2', 'Luis', 'Martínez', con1, 'ACTIVO', 'luis@example.com', 'FUNCIONARIO', None),
        ('user3', 'María', 'López', con1, 'ACTIVO', 'maria@example.com', 'FODUN', 'SELECCION'),
        ('user4', 'Carlos', 'Ramírez', con1, 'INACTIVO', 'carlos@example.com', 'GENERAL', None),
        ('Admin0', 'Juan', 'Pérez', con1, 'ACTIVO', 'juan@example.com', 'FUNCIONARIO', None)
    ])

    # Insert roles por persona
    cursor.executemany("INSERT INTO rol_persona (personas_usuario, rol_nombre) VALUES (?, ?)", [
        ('user1', 'MIEMBRO'),
        ('user2', 'FUNCIONARIO'),
        ('user3', 'ADMINISTRADOR'),
        ('user4', 'MIEMBRO'),
        ('Admin0', 'FUNCIONARIO'),
        ('Admin0', 'ADMINISTRADOR'),
        ('Admin0', 'MIEMBRO')
    ])

    # Insert sesiones (hoy, mañana y pasado mañana)
    hoy = datetime.now().strftime('%Y-%m-%d 08:00:00')
    manana = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d 10:00:00')
    pasado = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d 18:00:00')

    cursor.executemany("INSERT INTO sesiones (publico, fecha, actividad_tipo, ubicaciones_id_ubicaciones) VALUES (?, ?, ?, ?)", [
        ('GENERAL', hoy, 'CARDIO', 1),
        ('FUNCIONARIOS', manana, 'YOGA', 2),
        ('FODUN', pasado, 'FUERZA', 3)
    ])

    # Insert funcionarios en sesion
    cursor.executemany("INSERT INTO funcionarios_en_sesion (personas_usuario, sesiones_id, profesor_encargado) VALUES (?, ?, ?)", [
        ('user2', 1, 'SI'),
        ('Admin0', 2, 'NO')
    ])

    # Insert reservas
    cursor.executemany("INSERT INTO reservas (codigo, sesiones_id, personas_usuario) VALUES (?, ?, ?)", [
        ('RES001', 1, 'user1'),
        ('RES002', 1, 'user3'),
        ('RES003', 2, 'user4'),
        ('RES004', 3, 'user1')
    ])

    # Insert penalizaciones
    cursor.executemany("INSERT INTO penalizaciones (personas_usuario, fin_penalizacion) VALUES (?, ?)", [
        ('user4', (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S'))
    ])

    # Insert logs (ultimos dias)
    cursor.executemany("INSERT INTO logs (operacion, tabla, time_stamp, personas_usuario) VALUES (?, ?, ?, ?)", [
        ('ins', 'reservas', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'user1'),
        ('upd', 'personas', (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'), 'user2'),
        ('del', 'rol_persona', (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'), 'Admin0'),
        ('sel', 'actividad', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'user3')
    ])

    conn.commit()
    cursor.close()
    conn.close()
    print("Datos ficticios creados con éxito.")

if __name__ == "__main__":
    create_afid_test()
