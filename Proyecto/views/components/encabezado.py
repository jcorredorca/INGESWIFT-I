''' Encabezado de atun '''
from os import path
import sys
from PIL import Image
from customtkinter import CTkFrame,CTkLabel,CTkImage
from config import IMG_PATH

class Encabezado(CTkFrame):
    '''Clase que representa el encabezado'''
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="white", corner_radius=1 )
        self.repartir_espacio()

        self.abrir_imagenes()

        self.logo_atun = CTkLabel(self, text='')
        self.logo_atun.grid(row=0, column=0, sticky='w')

        self.logo_un = CTkLabel(self, text='')
        self.logo_un.grid(row=0, column=3, sticky='e')

        self.actualizar_dimensiones_imagen()
        self.logout = CTkFrame(self,fg_color="white", height=0)
        self.logout.grid(row=0, column=2, sticky='e')

        self.links = CTkFrame(self,fg_color="white", height=0)
        self.links.grid(row=0, column=1, sticky='w')


    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)

    def abrir_imagenes(self):
        '''Este método abre las imágenes necesarias para el encabezado'''

        # Rutas a imagenes
        ruta_logo_un = path.join(IMG_PATH, "LogoUNAL.png")
        ruta_logo_atun = path.join(IMG_PATH, "LogoATUN.png")

        self.imagen_un =Image.open(ruta_logo_un)
        self.imagen_atun =Image.open(ruta_logo_atun)

    def actualizar_dimensiones_imagen(self):
        '''Ajusta automáticamente las dimensiones de la imagen al frame'''
        self.master.update_idletasks()
        factor = 2/3 if self.winfo_screenwidth() > 2000 else 1/3
        if sys.platform.startswith('win'):
            pass
        else:
            factor = 1/10
        frame_heigth = int(self.master.winfo_height()*factor)
        new_width_un = int(frame_heigth * 370 / 200)
        new_width_atun = int(frame_heigth * 631 / 215)

        logo_un = CTkImage(light_image=self.imagen_un, size=(new_width_un, frame_heigth))
        logo_atun = CTkImage(light_image=self.imagen_atun, size=(new_width_atun, frame_heigth))

        self.logo_atun.configure(image=logo_atun)

        self.logo_un.configure(image=logo_un)

        self.master.update()
