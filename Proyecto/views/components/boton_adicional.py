''' Genera la plantilla para los botones adicionales '''
from customtkinter import CTkButton

class BotonAdicional(CTkButton):
    '''Clase que crea el boton adicional'''
    def __init__(self, master, comando, texto:str =''):
        super().__init__(master)

        tamanio = 0.008 if self.winfo_screenwidth() > 2000 else 0.015
        fuente= ("Segoe UI", self.winfo_screenwidth() * tamanio, 'bold')
        self.configure(font=fuente, fg_color="#5e3081", command=comando,
                       hover_color="#3E1D58", text=texto, text_color='white', anchor = 'center',
                       border_spacing=5)
