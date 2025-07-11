''' Vista de la ventana principal para funcionarios'''
from os import path
from config import IMG_PATH
from customtkinter import CTkFrame, CTkButton
from core import rol_funci
from services.general import recuperar_actividades
from ..components import menu_opciones


class Funcionario(CTkFrame):
    ''' Esta clase representa la venatana principal para funcionarios '''
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
        ancho = self.winfo_screenwidth() * 0.2

        self.boton_asistencia = CTkButton(self, text='REGISTRAR ASISTENCIA',
                                        anchor='center', font=fuente_opciones,
                                        fg_color="#F6A623", text_color="#2e1045",
                                        cursor="hand2", hover_color="#d38e14",
                                        corner_radius=6, border_spacing=10, width=ancho,
                                        command=lambda:
                                        rol_funci.redirigir_pantalla_asistencia(self.master))

        self.boton_asistencia.grid(row=0, column=1, sticky='s', pady=(0,20))

        self.opciones_busqueda = CTkButton(self, text='PROGRAMA A REGISTRAR',
                                        anchor='center', font=fuente_opciones,
                                        fg_color="#F6A623", text_color="#2e1045",
                                        cursor="hand2", hover_color="#d38e14",
                                        corner_radius=6, border_spacing=10, width=ancho,
                                        command= self.mostrar_menu
                                        )
        self.opciones_busqueda.grid(row=1, column=1, sticky = 'n')

        self.boton_miembros = CTkButton(self, text='GESTIONAR MIEMBROS',
                                        anchor='center', font=fuente_opciones,
                                        fg_color="#F6A623", text_color="#2e1045",
                                        cursor="hand2", hover_color="#d38e14",
                                        corner_radius=6, border_spacing=10, width=ancho,
                                        command=lambda:
                                        rol_funci.redirigir_pantalla_miembros(self.master))

        self.boton_miembros.grid(row=2, column=1, sticky='n')

    def mostrar_menu(self):
        '''Despliega el menu de opciones'''
        menu_opciones.MenuOpciones(self.master, self.opciones_busqueda, "#2e1045",
                                   recuperar_actividades())
