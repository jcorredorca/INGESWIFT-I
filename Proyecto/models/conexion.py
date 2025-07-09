''' Modulo para conexion con la base de datos '''

import sqlite3
from config import DB_PATH

class Conexion:
    ''' Clase que representa unca conexion a la base de datos'''
    def __init__(self):
        self.conexion = None
        self.cursor = None

    def conectar(self):
        ''' Este metodo crea la conexion con la baase de datos y genera
            respectivo cursor'''

        self.conexion = sqlite3.connect(DB_PATH)
        self.cursor = self.conexion.cursor()

    def desconectar(self):
        ''' Este metodo termina la conexion con la base de datos '''
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()

    def ejecutar_consulta(self, consulta, parametros=None):
        ''' Este metodo ejecuta las consultas sql '''
        parametros = [] if parametros is None else parametros
        resultados = []

        self.conectar()
        self.cursor.execute(consulta, parametros)
        resultados = self.cursor.fetchall()
        self.conexion.commit()
        self.desconectar()
        return resultados

    def ejecutar_multiples_consulta(self, consulta, parametros=None):
        ''' Este metodo ejecuta las consultas sql '''
        resultados = []

        self.conectar()
        self.cursor.executemany(consulta, parametros)
        resultados = self.cursor.fetchall()
        self.conexion.commit()
        self.desconectar()
        return resultados
