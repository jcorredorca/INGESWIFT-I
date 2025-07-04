''' Modulo para conexion con la base de datos '''

from os import getenv   #Para acceder a las variables de entorno
from dotenv import load_dotenv #Libreria para cargar las variables de entorno del .env
import mysql.connector


load_dotenv()
class Conexion:
    ''' Clase que representa unca conexion a la base de datos'''
    def __init__(self):
        self.host = getenv('DB_HOST')
        self.user = getenv('DB_USER')
        self.password = getenv('DB_PASSWORD')
        self.database = getenv('DB_NAME')
        self.conexion = None
        self.cursor = None

    def conectar(self):
        ''' Este metodo crea la conexion con la baase de datos y genera
            respectivo cursor'''
        self.conexion = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conexion.cursor()

    def desconectar(self):
        ''' Este metodo termina la conexion con la base de datos '''
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()

    def ejecutar_consulta(self, consulta, parametros=None):
        ''' Este metodo ejecuta las consultas sql '''
        resultados = []

        self.conectar()
        self.cursor.execute(consulta, parametros)
        resultados = self.cursor.fetchall()
        self.conexion.commit()
        self.desconectar()
        return resultados
