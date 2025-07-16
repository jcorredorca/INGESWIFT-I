'''Este modulo se encarga del frame de creacion de horarios'''
from tkinter import messagebox

from customtkinter import (BooleanVar, CTkButton, CTkCheckBox, CTkFrame,
                           CTkLabel, CTkOptionMenu, CTkScrollableFrame)
from services import administrador


class CrearHorario(CTkFrame):
    '''Clase que representa una ventana emergente para crear un horario'''

    def __init__(self, master):
        super().__init__(master)
        self.fuente = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.011)), 'bold')
        self.profesor = None

        self.configure(fg_color="#3d1c57")
        self.repartir_espacio()

        self.opciones_optionmenu()

        self.desplegable_funcionarios()

        self.desplegable_profesor()

        CTkButton(self,
                  text = 'CREAR',
                  font= self.fuente,
                  command=self.crear_horario,
                  fg_color= "#F6A623",
                  text_color="#3d1c57",
                  hover_color="#FEB745").grid(row=7,column=2)

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
        self.grid_rowconfigure(6, weight=0)
        self.grid_rowconfigure(7, weight=1)

    def opciones_optionmenu(self):
        '''Crea los widget publico y ubicacion 
        junto con las opciones de funcionarios y profesor'''
        #---Publico---#
        self.publico = CTkOptionMenu(self, font=self.fuente,
        dropdown_font=self.fuente, fg_color= "#F6A623", text_color="#3d1c57",
        corner_radius=1, dropdown_fg_color="#3d1c57", dropdown_text_color= "#f0f0f0",
        dropdown_hover_color= "#F6A623", width= self.winfo_screenwidth() * 0.1,
        anchor= 'center', button_color="#3d1c57", button_hover_color="#3d1c57",
        values= ['PUBLICO','GENERAL', 'FUNCIONARIO', 'FODUN'] )
        self.publico.grid(row=1, column=1)

        #---Ubicacion---#
        self.ubicacion = CTkOptionMenu(self, font=self.fuente,
        dropdown_font=self.fuente, fg_color= "#F6A623", text_color="#3d1c57",
        corner_radius=1, dropdown_fg_color="#3d1c57", dropdown_text_color= "#f0f0f0",
        dropdown_hover_color= "#F6A623", width= self.winfo_screenwidth() * 0.1,
        anchor= 'center', button_color="#3d1c57", button_hover_color="#3d1c57",
        values= ['UBICACION'] + administrador.recuperar_ubicaciones())
        self.ubicacion.grid(row=1, column=3)

        #---Funcionarios---
        funcionarios_label = CTkLabel(self, text='Funcionarios', text_color='whitesmoke',
                                      font=self.fuente, anchor='w')
        funcionarios_label.grid(row=3, column=1, sticky='w')

        self.funcionarios_frame = CTkScrollableFrame(self, fg_color="#2e1045")
        self.funcionarios_frame.grid(row=6, column=1, sticky='we')

        #---Profesor---
        profesor_label = CTkLabel(self, text='Profesor', text_color='whitesmoke',
                                      font=self.fuente, anchor='w')
        profesor_label.grid(row=3, column=3, sticky='w')

        self.profesor_frame = CTkScrollableFrame(self, fg_color="#2e1045")
        self.profesor_frame.grid(row=6, column=3, sticky='we')

    def desplegable_funcionarios(self):
        '''Crea el desplegable para escoger funcinarios'''
        funcionarios = administrador.recuperar_funcionarios()
        #lista de marcados
        self.check_vars = []
        for indice, funcionario in enumerate(funcionarios):
            # Creamos la variable para controlar si está marcado o no
            check_var = BooleanVar(value=False)  # todos empiezan sin seleccionar

            fun_ceckbox = CTkCheckBox(
                self.funcionarios_frame,
                font=self.fuente,
                fg_color="#F6A623",
                text_color="whitesmoke",
                text=funcionario[0],
                hover_color="#FFD591",
                variable=check_var)

            fun_ceckbox.grid(row=indice, column=0, sticky='w')
            # Guardamos (usuario) para saber luego quién fue marcado
            self.check_vars.append((funcionario[1], check_var))

    def desplegable_profesor(self):
        '''Crea el desplegable para escoger funcinarios'''
        funcionarios = administrador.recuperar_funcionarios()
        #lista de marcados
        self.profesores = []
        for indice, funcionario in enumerate(funcionarios):
            # Creamos la variable para controlar si está marcado o no
            check_var = BooleanVar(value=False)  # todos empiezan sin seleccionar

            fun_ceckbox = CTkCheckBox(
                self.profesor_frame,
                font=self.fuente,
                fg_color="#F6A623",
                text_color="whitesmoke",
                text=funcionario[0],
                hover_color="#FFD591",
                variable=check_var,
                command=lambda indice=indice: self.desactivar_checks(indice) )

            fun_ceckbox.grid(row=indice, column=0, sticky='w')
            # Guardamos (usuario) para saber luego quién fue marcado
            self.profesores.append((funcionario[1], check_var))

    def desactivar_checks(self, indice):
        '''Desactiva los otros checks tan pronto se presiona uno'''
        if self.profesores[indice][1]:
            for ind, opcion in enumerate(self.profesores):
                if ind != indice:
                    opcion[1].set(False) #desactivamos el check
                else:
                    self.profesor = opcion[0]

    def crear_horario(self):
        '''Este metodo recupera la información 
        del formulario y crea el horario'''

        publico = self.publico.get()
        ubicacion = self.ubicacion.get()

        if all([publico == 'PUBLICO', ubicacion == 'UBICACION']):
            messagebox.showerror('Error', 'Asegurese de escoger un público y ubicación')
            return

        seleccionados = [funcionario for funcionario, var in self.check_vars if var.get()]
        profesor = self.profesor

        if len(seleccionados) <= 0 or profesor is None:
            messagebox.showerror('Error',
                                 'Asegurese de escoger almenos un funcionario y un profesor')
            return

        celda = self.master.master.master
        seleccion_actividad: CTkOptionMenu = celda.master.master.opciones_busqueda

        fecha_hora = celda.fecha_hora
        actividad = seleccion_actividad.get()

        id_ubicacion = administrador.recuperar_id_ubicacion(ubicacion)

        if actividad == 'PLANES':
            messagebox.showerror('Error',
                                'No se ha escogido ningun plan!')
            return

        id_horario = administrador.crear_horario([publico, fecha_hora, actividad, id_ubicacion])
        administrador.asignar_funcionarios(seleccionados, id_horario, profesor)
        self.master.master.master.actualizar_colores('#c3f7c8', '#e3fae3')
        self.master.destroy()
