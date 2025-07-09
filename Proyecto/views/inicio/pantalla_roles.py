'''Módulo para crear la pantalla inciial luego de hacer login'''

from customtkinter import CTkFrame, CTkLabel
from ..components.boton_adicional import BotonAdicional
from core import utils

class PantallaRoles(CTkFrame):
    '''Clase que representa el formulario de login de atun'''
    def __init__(self, master, roles:list):
        super().__init__(master)
        self.roles = roles

        self.configure(fg_color="#2e1045", corner_radius=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        fuente = ("Segoe UI", max(40,int(self.winfo_screenwidth() * 0.02)), 'bold')

        label = CTkLabel(self, text='Bienvenido!', font=fuente,
                         text_color='Whitesmoke', anchor='center')
        label.grid(row=1, column=1)
        
        self.crear_botones()

    def crear_botones(self):
        '''Crea los botones de acuerdo a los roles de cada usuario'''
        origen = self.master
        pantalla = {
            'MIEMBRO': lambda: utils.redirigir_pantalla_miembro(origen),
            'FUNCIONARIO': lambda: utils.redirigir_pantalla_funcionario(origen),
            'ADMINISTRADOR': lambda: utils.redirigir_pantalla_admin(origen),
        }

        frame_botones = self.master.encabezado.links
        botones = [BotonAdicional(frame_botones, comando=pantalla[rol], texto=rol)
                        for rol in self.roles]

        for index, boton in enumerate(botones):
            boton.grid(column=index, row=0, padx=10)

        self.logout = BotonAdicional(self.master.encabezado.logout,
                                    texto='LogOut', comando= self.llamar_a_logout)
        self.logout.pack(padx=10)

    def llamar_a_logout(self):
        '''Este metodo llama a la funcion logout'''
        utils.log_out(self.master)
