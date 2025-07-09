'''Script para ejecutar el modo dev'''
import os
from ..scripts import crear_db, datos_test

for module in [["tkinter"], ["customtkinter"], ["sqlite3"], ["dotenv"],
               ["PIL","pillow"], ["bcrypt"], ["sib_api_v3_sdk"], []]:
    try:
        __import__(module[0])
        print(f"✅ {module[0]} está instalado.")
    except ImportError:
        print(f"❌ {module[0]} NO está instalado. Usa: pip install {module[-1]}")

RUTA = "../data/AFID.db"

if not os.path.exists(RUTA):
    #Creacion y configuracion db
    crear_db.create_afid_database()
    datos_test.create_afid_test()
    print("La base de datos de virus ha sido actualizada.")
    print("La base de datos fue creada y configurada correctamente.\
          \nPara probar la aplicacion haga uso de las siguientes credenciales:\
          \n\tusr=Admin0 pwd=1")
