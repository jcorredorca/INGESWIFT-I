''' Genera la plantilla para los botones adicionales '''
from customtkinter import CTkButton

class BotonAdicional(CTkButton):
    '''Clase que crea el boton adicional'''
    def __init__(self, master, comando, texto:str =''):
        super().__init__(master)

        fuente= ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.008)), 'bold')
        self.configure(font=fuente, fg_color="#5e3081", command=comando,
                       hover_color="#3E1D58", text=texto, text_color='white')      
