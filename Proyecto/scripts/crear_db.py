# crear_db.py

import sqlite3
from config import DB_PATH

def create_afid_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # personas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS personas (
        usuario TEXT NOT NULL PRIMARY KEY,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        hash_contrasena TEXT NOT NULL,
        estado TEXT DEFAULT 'INACTIVO' CHECK(estado IN ('ACTIVO', 'INACTIVO')),
        correo TEXT NOT NULL UNIQUE,
        rol_en_universidad TEXT DEFAULT 'GENERAL' CHECK(rol_en_universidad IN ('GENERAL', 'FUNCIONARIO', 'FODUN', 'CUIDADO')),
        grupo_especial TEXT CHECK(grupo_especial IN ('JOVENES', 'SELECCION'))
    )
    """)

    # actividad
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS actividad (
        tipo TEXT NOT NULL PRIMARY KEY,
        aforo INTEGER NOT NULL
    )
    """)

    # ubicaciones
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ubicaciones (
        id_ubicaciones INTEGER PRIMARY KEY AUTOINCREMENT,
        ubicacion TEXT NOT NULL
    )
    """)

    # sesiones
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sesiones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        publico TEXT NOT NULL CHECK(publico IN ('GENERAL', 'FUNCIONARIO', 'FODUN', 'CUIDADO')),
        fecha DATETIME NOT NULL,
        actividad_tipo TEXT NOT NULL,
        ubicaciones_id_ubicaciones INTEGER NOT NULL,
        FOREIGN KEY (actividad_tipo) REFERENCES actividad(tipo),
        FOREIGN KEY (ubicaciones_id_ubicaciones) REFERENCES ubicaciones(id_ubicaciones)
    )
    """)

    # rol
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rol (
        nombre TEXT NOT NULL PRIMARY KEY CHECK(nombre IN ('MIEMBRO', 'FUNCIONARIO', 'ADMINISTRADOR'))
    )
    """)

    # rol_persona
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rol_persona (
        personas_usuario TEXT NOT NULL,
        rol_nombre TEXT NOT NULL CHECK(rol_nombre IN ('MIEMBRO', 'FUNCIONARIO', 'ADMINISTRADOR')),
        PRIMARY KEY (personas_usuario, rol_nombre),
        FOREIGN KEY (personas_usuario) REFERENCES personas(usuario),
        FOREIGN KEY (rol_nombre) REFERENCES rol(nombre)
    )
    """)

    # asistencia_extemporanea
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS asistencias_extemp (
        personas_usuario TEXT NOT NULL,
        sesiones_id INTEGER NOT NULL,
        PRIMARY KEY (personas_usuario, sesiones_id),
        FOREIGN KEY (personas_usuario) REFERENCES personas(usuario),
        FOREIGN KEY (sesiones_id) REFERENCES sesiones(id)
    )
    """)

    # funcionarios_en_sesion
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS funcionarios_en_sesion (
        personas_usuario TEXT NOT NULL,
        sesiones_id INTEGER NOT NULL,
        profesor_encargado TEXT NOT NULL CHECK(profesor_encargado IN ('SI', 'NO')),
        PRIMARY KEY (personas_usuario, sesiones_id),
        FOREIGN KEY (personas_usuario) REFERENCES personas(usuario),
        FOREIGN KEY (sesiones_id) REFERENCES sesiones(id)
    )
    """)

    # reservas con campo asistio
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservas (
        codigo TEXT NOT NULL PRIMARY KEY,
        sesiones_id INTEGER NOT NULL,
        personas_usuario TEXT NOT NULL,
        asistio INTEGER DEFAULT 0 CHECK(asistio IN (0,1)),
        FOREIGN KEY (sesiones_id) REFERENCES sesiones(id),
        FOREIGN KEY (personas_usuario) REFERENCES personas(usuario)
    )
    """)

    # logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id_log INTEGER PRIMARY KEY AUTOINCREMENT,
        operacion TEXT NOT NULL CHECK(operacion IN ('del', 'upd', 'ins', 'sel')),
        tabla TEXT NOT NULL,
        time_stamp DATETIME NOT NULL,
        personas_usuario TEXT NOT NULL,
        FOREIGN KEY (personas_usuario) REFERENCES personas(usuario)
    )
    """)

    # penalizaciones
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS penalizaciones (
        personas_usuario TEXT NOT NULL PRIMARY KEY,
        fin_penalizacion DATETIME NOT NULL,
        FOREIGN KEY (personas_usuario) REFERENCES personas(usuario)
    )
    """)

    # Insert roles
    cursor.executemany("INSERT INTO rol (nombre) VALUES (?)", [
        ('MIEMBRO',),
        ('ADMINISTRADOR',),
        ('FUNCIONARIO',)
    ])

    # Insert activities
    cursor.executemany("INSERT INTO actividad (tipo, aforo) VALUES (?, ?)", [
        ("PLUS", 30),
        ("CARDIO", 20),
        ("FUERZA", 30),
        ("FULLBODY", 20),
        ("SPINNING", 5),
        ("YOGA", 20),
        ("MIND BODY", 20),
        ("PRUEBAS FÍSICAS", -1),
        ("NUTRICIÓN", -1)
    ])

    # Insert locations
    cursor.executemany("INSERT INTO ubicaciones (ubicacion) VALUES (?)", [
        ('PEROLA',),
        ('ESTADIO',),
        ('EDIFICIO 701-116',),
        ('EDIFICIO 701-203',),
        ('POLIDEPORTIVO',)
    ])

    conn.commit()
    cursor.close()
    conn.close()
    print("La base de datos AFID.db ha sido creada con todas sus tablas")

if __name__ == "__main__":
    create_afid_database()
