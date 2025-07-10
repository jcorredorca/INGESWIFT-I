'''Programa principal desde el cual se crea la ventana'''
try:
    from ctypes import windll
    #Para indicar que la app ya tiene en cuenta el reescalamiento 
    windll.shcore.SetProcessDpiAwareness(1)
except (ImportError, AttributeError):
    pass
import views.main_window as vp

def run_app():
    '''Esta funcion corre la aplicacion'''

    app = vp.App()
    app.mainloop()

if __name__ == '__main__':
    run_app()
