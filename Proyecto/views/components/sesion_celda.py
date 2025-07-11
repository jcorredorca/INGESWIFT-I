'''Este modulo trae las celdas que representan una sesion'''
from datetime import datetime
from customtkinter import CTkLabel

class SesionCelda(CTkLabel):
    '''Esta clase representa una celda de sesion'''

    def __init__(self, master, fecha_hora:datetime, fg_color="#f0f0f0", hover_color="#A8A4A4"):
        super().__init__(master)
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.configure(fg_color=self.fg_color,
                       text='',
                       corner_radius=3,
                       cursor="hand2")
        self.fecha_hora= fecha_hora

        self.bind("<Enter>", self.entrada)
        self.bind("<Leave>", self.salida)

    def entrada(self, event):
        '''Simula el hover'''
        if event:
            self.configure(fg_color=self.hover_color)
            self.update()

    def salida(self, event):
        '''Simula la salida del hover'''
        if event:
            self.configure(fg_color=self.fg_color)
            self.update()

    def actualizar_colores(self, fg, hover):
        '''Este metodo actualiza los colores de la celda'''
        self.fg_color = fg
        self.hover_color = hover
        self.configure(fg_color=self.fg_color)
        self.update()
