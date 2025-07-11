import sqlite3
from datetime import datetime, timedelta
import random
import string

from config import DB_PATH
from services import login

def create_afid_test():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    con1 = login.hash_contrasena('1')

    # Insert personas
    cursor.executemany("INSERT INTO personas (usuario, nombre, apellido, \
                       hash_contrasena, estado, correo, rol_en_universidad, grupo_especial) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [
        ('user1', 'Ana', 'García', con1, 'ACTIVO', 'ana@example.com', 'GENERAL', None),
        ('user2', 'Luis', 'Martínez', con1, 'ACTIVO', 'luis@example.com', 'FUNCIONARIO', None),
        ('user3', 'María', 'López', con1, 'ACTIVO', 'maria@example.com', 'GENERAL', 'JOVENES'),
        ('Admin0', 'Juan', 'Pérez', con1, 'INACTIVO', 'juan@example.com', 'FUNCIONARIO', None),
        ('user4', 'Carlos', 'Rodríguez', con1, 'ACTIVO', 'carlos@example.com', 'FODUN', None),
        ('user5', 'Sofía', 'Hernández', con1, 'ACTIVO', 'sofia@example.com', 'GENERAL', 'SELECCION'),
        ('user6', 'Pedro', 'Gómez', con1, 'ACTIVO', 'pedro@example.com', 'CUIDADO', None),
        ('user7', 'Laura', 'Díaz', con1, 'ACTIVO', 'laura@example.com', 'GENERAL', 'JOVENES'),
        ('user8', 'Miguel', 'Torres', con1, 'ACTIVO', 'miguel@example.com', 'FUNCIONARIO', None),
        ('user9', 'Elena', 'Ruiz', con1, 'ACTIVO', 'elena@example.com', 'GENERAL', None),
        ('user10', 'David', 'Morales', con1, 'INACTIVO', 'david@example.com', 'GENERAL', None)
    ])

    # Insert rol_persona
    cursor.executemany("INSERT INTO rol_persona (personas_usuario, rol_nombre) VALUES (?, ?)", [
        ('user1', 'MIEMBRO'),
        ('user3', 'ADMINISTRADOR'),
        ('user2', 'FUNCIONARIO'),
        ('Admin0', 'MIEMBRO'),
        ('Admin0', 'FUNCIONARIO'),
        ('Admin0', 'ADMINISTRADOR'),
        ('user4', 'MIEMBRO'),
        ('user5', 'MIEMBRO'),
        ('user6', 'FUNCIONARIO'),
        ('user7', 'MIEMBRO'),
        ('user8', 'FUNCIONARIO'),
        ('user9', 'MIEMBRO'),
        ('user10', 'MIEMBRO')
    ])

    # Insert sesiones (proximas 2 semanas)
    base_date = datetime.now()
    actividades = ["PLUS", "CARDIO", "FUERZA", "FULLBODY", "SPINNING", "YOGA", "MIND BODY", "PRUEBAS FÍSICAS", "NUTRICIÓN"]
    publicos = ["GENERAL", "FUNCIONARIOS", "FODUN"]
    ubicaciones_ids = [1, 2, 3, 4, 5]  # IDs de ubicaciones insertadas en create_afid_database
    
    sesiones_data = []
    for i in range(50):  # 50 sesiones de ejemplo
        fecha = base_date + timedelta(days=random.randint(0, 14), hours=random.randint(6, 20))
        actividad = random.choice(actividades)
        publico = random.choice(publicos)
        ubicacion_id = random.choice(ubicaciones_ids)
        
        sesiones_data.append((publico, fecha, actividad, ubicacion_id))
    
    cursor.executemany("INSERT INTO sesiones (publico, fecha, actividad_tipo, ubicaciones_id_ubicaciones) VALUES (?, ?, ?, ?)", 
                      sesiones_data)

    # Insert funcionarios_en_sesion
    funcionarios = ['user2', 'Admin0', 'user6', 'user8']
    funcionarios_sesion_data = []
    for i in range(1, 21):  # Para las primeras 20 sesiones
        funcionario = random.choice(funcionarios)
        profesor_encargado = random.choice(['SI', 'NO'])
        funcionarios_sesion_data.append((funcionario, i, profesor_encargado))
    
    cursor.executemany("INSERT INTO funcionarios_en_sesion (personas_usuario, sesiones_id, profesor_encargado) VALUES (?, ?, ?)", 
                      funcionarios_sesion_data)

    # Insert reservas
    def generate_codigo():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    usuarios_miembros = ['user1', 'user3', 'user4', 'user5', 'user7', 'user9', 'user10']
    reservas_data = []
    for i in range(1, 31):  # Para las primeras 30 sesiones
        num_reservas = random.randint(1, 5)  # Entre 1 y 5 reservas por sesion
        usuarios_seleccionados = random.sample(usuarios_miembros, min(num_reservas, len(usuarios_miembros)))
        
        for usuario in usuarios_seleccionados:
            codigo = generate_codigo()
            reservas_data.append((codigo, i, usuario))
    
    cursor.executemany("INSERT INTO reservas (codigo, sesiones_id, personas_usuario) VALUES (?, ?, ?)", 
                      reservas_data)

    # Insert logs
    operaciones = ['del', 'upd', 'ins', 'sel']
    tablas = ['personas', 'sesiones', 'reservas', 'funcionarios_en_sesion', 'rol_persona']
    usuarios_todos = ['user1', 'user2', 'user3', 'Admin0', 'user4', 'user5', 'user6', 'user7', 'user8', 'user9', 'user10']
    
    logs_data = []
    for i in range(100):  # 100 logs de ejemplo
        operacion = random.choice(operaciones)
        tabla = random.choice(tablas)
        timestamp = base_date - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        usuario = random.choice(usuarios_todos)
        
        logs_data.append((operacion, tabla, timestamp, usuario))
    
    cursor.executemany("INSERT INTO logs (operacion, tabla, time_stamp, personas_usuario) VALUES (?, ?, ?, ?)", 
                      logs_data)

    # Insert penalizaciones
    cursor.executemany("INSERT INTO penalizaciones (personas_usuario, fin_penalizacion) VALUES (?, ?)", [
        ('user10', base_date + timedelta(days=7)),  # Penalizado por 7 días más
        ('user1', base_date + timedelta(days=3)),   # Penalizado por 3 días más
    ])

    conn.commit()
    cursor.close()
    conn.close()
    print("Datos ficticios creados con éxito.")

if __name__ == "__main__":
    create_afid_test()