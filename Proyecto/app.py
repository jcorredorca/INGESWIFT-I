'''Programa principal desde el cual se crea la ventana'''
from ctypes import windll
import views.main_window as vp

def run_app():
    '''Esta funcion corre la aplicacion'''

    #Para indicar que la app ya tiene en cuenta el reescalamiento
    windll.shcore.SetProcessDpiAwareness(1)

    app = vp.App()
    app.mainloop()

if __name__ == '__main__':
    run_app()
