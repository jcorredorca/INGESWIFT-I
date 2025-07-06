'''Programa principal desde el cual se crea la ventana'''
from ctypes import windll
import scripts.datos_test
import views.main_window as vp
import scripts.crear_db

#from Pruebas import crear_datosDb_ficticios

if __name__ == '__main__':
    windll.shcore.SetProcessDpiAwareness(1)

    #crear_datosDb_ficticios.usar()
    #scripts.crear_db.create_afid_database()
    #scripts.datos_test.create_afid_test()

    app = vp.App()
    app.mainloop()
