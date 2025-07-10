'''Ventana emergente para el cambio de contraseña'''

from customtkinter import CTkScrollableFrame, CTkButton, BooleanVar, CTkLabel, CTkFrame, CTkCheckBox, CTkOptionMenu
from services import administrador

class CrearHorario(CTkFrame):
    '''Clase que representa una ventana emergente para crear un horario'''

    def __init__(self, master):
        super().__init__(master)
        self.fuente = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.012)), 'bold')
        self.profesor = None

        self.configure(fg_color="#3d1c57")
        self.repartir_espacio()

        self.opciones_optionmenu()

    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=1)

    def opciones_optionmenu(self):
        '''Crea los dos widget publico y ubicacion 
        de tipo optionMenu'''
        fuente = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.011)), 'bold')
        #---Publico---#
        self.publico = CTkOptionMenu(self, font=fuente,
        dropdown_font=fuente, fg_color= "#F6A623", text_color="#3d1c57",
        corner_radius=1, dropdown_fg_color="#3d1c57", dropdown_text_color= "#f0f0f0",
        dropdown_hover_color= "#F6A623", width= self.winfo_screenwidth() * 0.1,
        anchor= 'center', button_color="#3d1c57", button_hover_color="#3d1c57",
        values= ['PUBLICO','GENERAL', 'FUNCIONARIOS', 'FODUN'] )
        self.publico.grid(row=1, column=1)

        #---Ubicacion---#
        self.ubicacion = CTkOptionMenu(self, font=fuente,
        dropdown_font=fuente, fg_color= "#F6A623", text_color="#3d1c57",
        corner_radius=1, dropdown_fg_color="#3d1c57", dropdown_text_color= "#f0f0f0",
        dropdown_hover_color= "#F6A623", width= self.winfo_screenwidth() * 0.1,
        anchor= 'center', button_color="#3d1c57", button_hover_color="#3d1c57",
        values= ['UBICACION'] + administrador.recuperar_ubicaciones())
        self.ubicacion.grid(row=1, column=3)

        #---Funcionarios---
        funcionarios_label = CTkLabel(self, text='Funcionarios', text_color='whitesmoke',
                                      font=fuente)
        funcionarios_label.grid(row=3, column=1)

        self.funcionarios_frame = CTkScrollableFrame(self, fg_color="#2e1045")
        self.funcionarios_frame.grid(row=4, column=1, sticky='we')

        funcionarios = administrador.recuperar_funcionarios()
        #lista de marcados
        self.check_vars = []
        for indice, funcionario in enumerate(funcionarios):
            # Creamos la variable para controlar si está marcado o no
            check_var = BooleanVar(value=False)  # todos empiezan sin seleccionar

            fun_ceckbox = CTkCheckBox(
                self.funcionarios_frame,
                font=fuente,
                fg_color="#F6A623",
                text_color="whitesmoke",
                text=funcionario[0],
                hover_color="#FFD591",
                variable=check_var)
            fun_ceckbox.grid(row=indice, column=0, sticky='w')
            # Guardamos (usuario o ID, variable) para saber luego quién fue marcado
            self.check_vars.append((funcionario[1], check_var))
        boton_tmp = CTkButton(self,command=self.crear).grid(row = 5, column = 2)

    def crear(self):
        publico = self.publico.get()
        print(publico)
