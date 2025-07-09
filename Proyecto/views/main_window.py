'''Ventana principal de atun. 
    Inicia el encabezado y pie de pagina'''

import customtkinter
from .components import encabezado,pie_de_pagina
from .inicio import inicio

class App(customtkinter.CTk):
    '''Representa la ventana  sobre la cual se pondran todos los elementos'''

    def __init__(self):
        super().__init__()

        self.title("ATUN")
        self.configure(fg_color = "#09FF00")
        self.configurar_dimensiones()
        self.repartir_espacio()

        #Colocamos los 3 elementos principales
        self.encabezado = encabezado.Encabezado(self)

        self.encabezado.grid(row=0, column=0, sticky="nsew")

        self.contenido = inicio.Inicio(self)

        self.contenido.grid(row=1, column=0, sticky="nsew")

        self.pie = pie_de_pagina.PiePagina(self)
        self.pie.grid(row=2, column=0, sticky="nsew")

    def configurar_dimensiones(self):
        '''Hace las configuraciones iniciales en cuanto a tamaños de pantalla'''
        self.activar_fullscreen()
        ancho,alto = self.get_size()
        self.geometry(f"{ancho}x{alto}+0+0")
        self.minsize(width=1000, height=600)
        self.bind("<F11>", lambda e: self.activar_fullscreen())   # F11 para activar
        self.bind("<Escape>", lambda e: self.desactivar_fullscreen())  # ESC para salir

    def repartir_espacio(self):
        '''Reparte el espacio entre el encabezado contenido y pie de pagina'''
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight= 6)
        self.grid_rowconfigure(2, weight=0)

    def get_size(self):
        '''Trae las dimensiones de la pantalla actual'''
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        return screen_width,screen_height

    def activar_fullscreen(self):
        '''Activa la pantalla completa'''
        self.attributes("-fullscreen", True)

    def desactivar_fullscreen(self):
        '''Desactiva la pantalla completa'''
        self.attributes("-fullscreen", False)
