'''Programa principal desde el cual se crea la ventana'''
from ctypes import windll
import Plantilla.ventana_principal as vp

if __name__ == '__main__':
    windll.shcore.SetProcessDpiAwareness(1)
    app = vp.App()
    app.mainloop()
