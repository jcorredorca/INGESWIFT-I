''' Encabezado de atun '''
from os import path
from PIL import Image
from customtkinter import CTkFrame,CTkLabel,CTkImage

class Encabezado(CTkFrame):
    '''Clase que representa el encabezado'''
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="white", corner_radius=1 )
        self.repartir_espacio()

        self.abrir_imagenes()

        self.logo_atun = CTkLabel(self, text='', sticky="w")
        self.logo_atun.grid(row=0, column=0)

        self.logo_un = CTkLabel(self, text='', sticky="e")
        self.logo_un.grid(row=0, column=2)

        self.actualizar_dimensiones_imagen()
        self.links = None

    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)

    def abrir_imagenes(self):
        '''Este método abre las imágenes necesarias para el encabezado'''
        base_dir = path.dirname(__file__)
        # Rutas a imagenes
        ruta_logo_un = path.join(base_dir,"..","Imagenes", "LogoUNAL.png")
        ruta_logo_atun = path.join(base_dir,"..","Imagenes", "LogoATUN.png")

        self.imagen_un =Image.open(ruta_logo_un)
        self.imagen_atun =Image.open(ruta_logo_atun)

    def actualizar_dimensiones_imagen(self):
        '''Ajusta automáticamente las dimensiones de la imagen al frame'''

        frame_heigth = self.master.winfo_height()/2
        new_width_un = frame_heigth * 370 / 200
        new_width_atun = frame_heigth * 631 / 215

        logo_un = CTkImage(light_image=self.imagen_un, size=(new_width_un, frame_heigth))
        logo_atun = CTkImage(light_image=self.imagen_atun, size=(new_width_atun, frame_heigth))

        self.logo_atun.configure(image=logo_atun)

        self.logo_un.configure(image=logo_un)

        self.master.update()
