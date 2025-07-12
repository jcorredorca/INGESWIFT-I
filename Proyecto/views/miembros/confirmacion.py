'''Este modulo se encarga del frame de confirmaciones'''

from customtkinter import CTkLabel,CTkFrame

class Confirmacion(CTkFrame):
    '''Clase que representa una ventana emergente para confirmaciones'''

    def __init__(self, master, codigo):
        super().__init__(master)
        self.fuente = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.011)), 'bold')
        self.configure(fg_color="#3d1c57")

        self.repartir_espacio()


        

    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
