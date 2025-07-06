import sqlite3

from config import DB_PATH
from services import login

def create_afid_test():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    con1 = login.hash_contrasena('1')

    # Insert personas
    cursor.executemany("INSERT INTO personas (usuario, nombre, apellido, hash_contrasena, estado, correo) VALUES (?, ?, ?, ?, ?, ?)", [
        ('user1', 'Ana', 'García', con1, 'ACTIVO', 'ana@example.com'),
        ('user2', 'Luis', 'Martínez', con1, None, 'luis@example.com'),
        ('user3', 'María', 'López', con1, None, 'maria@example.com'),
        ('Admin0', 'Juan', 'Pérez', con1, 'INACTIVO', 'juan@example.com')
    ])


    # Insert activities
    cursor.executemany("INSERT INTO rol_persona (personas_usuario, rol_nombre) VALUES  (?, ?)", [
        ('user1', 'MIEMBRO'),
        ('user3', 'ADMINISTRADOR'),
        ('user2', 'FUNCIONARIO'),
        ('Admin0', 'MIEMBRO'),
        ('Admin0', 'FUNCIONARIO'),
        ('Admin0', 'ADMINISTRADOR')
    ])

    conn.commit()
    cursor.close()
    conn.close()
    print("Datos ficticios creados con éxito.")

