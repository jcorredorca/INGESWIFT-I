''' Vista de la ventana principal para Administradores'''
from os import path
from config import IMG_PATH
from customtkinter import CTkFrame, CTkLabel, CTkButton
from ..components.boton_adicional import BotonAdicional
from core import rol_admin

class Admin(CTkFrame):
    ''' Esta clase representa la venatana principal para administradores '''
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color= "#2e1045", corner_radius=1)
        self.repartir_espacio()

        self.crear_menu_opciones()


    def repartir_espacio(self):
        '''Reparte el espacio'''

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

    def crear_menu_opciones(self):
        '''Este metodo crea el menu de opciones'''

        fuente_opciones = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.012)), 'bold')
        ancho = self.winfo_screenwidth() * 0.25

        self.boton_funcionarios = CTkButton(self, text='GESTIONAR FUNCIONARIOS',
                                        anchor='center', font=fuente_opciones,
                                        fg_color="#F6A623", text_color="#2e1045",
                                        cursor="hand2", hover_color="#d38e14",
                                        corner_radius=6, border_spacing=10, width=ancho, 
                                        command=lambda: rol_admin.redirigir_pantalla_funcionarios(self.master))

        self.boton_funcionarios.grid(row=1, column=1)

        self.boton_horarios = CTkButton(self, text='HORARIOS SEMANALES',
                                        anchor='center', font=fuente_opciones,
                                        fg_color="#F6A623", text_color="#2e1045",
                                        cursor="hand2", hover_color="#d38e14",
                                        corner_radius=6, border_spacing=10, width=ancho,
                                        command=lambda: rol_admin.redirigir_pantalla_horarios(self.master))

        self.boton_horarios.grid(row=0, column=1)

        self.boton_miembros = CTkButton(self, text='GESTIONAR MIEMBROS',
                                        anchor='center', font=fuente_opciones,
                                        fg_color="#F6A623", text_color="#2e1045",
                                        cursor="hand2", hover_color="#d38e14",
                                        corner_radius=6, border_spacing=10, width=ancho, 
                                        command=lambda: rol_admin.redirigir_pantalla_estado_miembros(self.master))

        self.boton_miembros.grid(row=2, column=1)
