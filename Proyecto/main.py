'''Programa principal desde el cual se crea la ventana'''
from ctypes import windll
import Plantilla.ventana_principal as vp

from Pruebas import crear_datosDb_ficticios

if __name__ == '__main__':
    windll.shcore.SetProcessDpiAwareness(1)

    #crear_datosDb_ficticios.usar()

    app = vp.App()
    app.mainloop()
