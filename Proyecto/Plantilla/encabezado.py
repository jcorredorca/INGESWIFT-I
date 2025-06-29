''' Encabezado de atun '''
from os import path
from PIL import Image
from customtkinter import CTkFrame,CTkLabel,CTkImage

class Encabezado(CTkFrame):
    '''Clase que representa el encabezado'''
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="white", corner_radius=1, )
        self.repartir_espacio()

        logo_un,logo_atun = self.crear_imagenes_ctk()
        self.logo_atun = CTkLabel(self, image=logo_atun, text='')
        self.logo_atun.grid(row=0, column=0, sticky="nw", pady=10, padx=10)

        self.links = None

        self.logo_un = CTkLabel(self, image=logo_un, text='')
        self.logo_un.grid(row=0, column=2, sticky="ne",  padx=10)

    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)

    def crear_imagenes_ctk(self):
        '''Este metodo crea los objetos imagen para mostrarlo en un label'''

        base_dir = path.dirname(__file__)
        # Rutas a imagenes
        ruta_logo_un = path.join(base_dir,"..","Imagenes", "LogoUNAL.png")
        ruta_logo_atun = path.join(base_dir,"..","Imagenes", "LogoATUN.png")

        logo_un = CTkImage(light_image=Image.open(ruta_logo_un),
        size=(370//1.5, 200//1.5))
        logo_atun = CTkImage(light_image=Image.open(ruta_logo_atun),
        size=(631//2, 215//2))
        return logo_un,logo_atun
