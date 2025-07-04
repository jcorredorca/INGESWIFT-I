import bcrypt

from Funcionalidades.conexion import Conexion


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def usar():
    hashed = hash_password("Admin1234")

    store = hashed.decode()

    contrasena = "Admin234"
    print(bcrypt.checkpw(contrasena.encode(), store.encode()))

    con = Conexion()

    query = f'''
    INSERT INTO personas (
    usuario,
    nombre,
    apellido,
    hash_contrasena,
    estado,
    correo,
    rol_en_universidad,
    grupo_especial
    )
    VALUES 
    ('Admin0', 'Santiago', 'Fetecua', %s, null, 'sfetecua@unal.edu.co', null, null);'''
    
    rol = '''INSERT INTO rol_persona VALUES ('Admin0', 'ADMINISTRADOR')'''

    con.ejecutar_consulta(query, [store])
    con.ejecutar_consulta(rol)

    print(con.ejecutar_consulta('SELECT * FROM rol_persona'))

