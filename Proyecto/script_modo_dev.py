'''Script para ejecutar el modo dev'''
import os
from scripts import crear_db, datos_test

RUTA = "../data/AFID.db"

if not os.path.exists(RUTA):
    #Creacion y configuracion db
    crear_db.create_afid_database()
    datos_test.create_afid_test()
    print("La base de datos de virus ha sido actualizada.")
    print("La base de datos fue creada y configurada correctamente.\
          \nPara probar la aplicacion haga uso de las siguientes credenciales:\
          \n\tusr=Admin0 pwd=1")
else:
    print("La base de datos fue encontrada.\
          \nPara probar la aplicacion haga uso de las siguientes credenciales:\
          \n\tusr=Admin0 pwd=1")
