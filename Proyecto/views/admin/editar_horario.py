'''Este modulo se encarga del frame de edicion de horarios'''
from tkinter import messagebox
from customtkinter import (CTkScrollableFrame,
                           CTkButton, BooleanVar,
                           CTkLabel, CTkFrame,
                           CTkCheckBox, CTkOptionMenu)
from services import administrador, general

class EditarHorario(CTkFrame):
    '''Clase que representa una ventana emergente para la edicion de horarios'''

    def __init__(self, master):
        super().__init__(master)
        self.fuente = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.011)), 'bold')
        self.profesor = None
        self.publico = None
        self.ubicacion = None
        self.funcionarios_frame = None
        self.profesor_frame = None
        self.check_vars = []
        self.profesores = []

        self.configure(fg_color="#3d1c57")

        self.contenido = None

        self.crear_seleccion()

    def crear_seleccion(self):
        '''Este metodo crea el menu de seleccion entre editar y eliminar'''

        self.contenido = CTkFrame(self, fg_color="#3d1c57")
        self.contenido.pack(fill="both", expand=True)
        self.repartir_espacio_seleccion()
        CTkButton(self.contenido, text = 'ELIMINAR',
                  font= self.fuente,
                  command=self.eliminar_sesion,
                  fg_color= "#F6A623",
                  text_color="#3d1c57",
                  hover_color="#FFB641").grid(row=1, column=1, sticky='we')

        CTkButton(self.contenido, text = 'EDITAR',
                  font= self.fuente,
                  command=self.editar_sesion,
                  fg_color= "#F6A623",
                  text_color="#3d1c57",
                  hover_color="#FFB641").grid(row=3, column=1, sticky='we')

    def repartir_espacio_seleccion(self):
        '''Reparte el espacio '''
        self.contenido.grid_columnconfigure(0, weight=1)
        self.contenido.grid_columnconfigure(1, weight=1)
        self.contenido.grid_columnconfigure(2, weight=1)

        self.contenido.grid_rowconfigure(0, weight=1)
        self.contenido.grid_rowconfigure(1, weight=1)
        self.contenido.grid_rowconfigure(2, weight=1)
        self.contenido.grid_rowconfigure(3, weight=1)
        self.contenido.grid_rowconfigure(4, weight=1)

    def eliminar_sesion(self):
        '''Este metodo trae la informacion necesaria para eliminar
          la sesion asociada a la celda'''

        administrador.eliminar_sesion(self.recuperar_id_sesion())

        self.master.master.master.actualizar_colores("#f0f0f0", "#A8A4A4")
        self.master.destroy()

    def editar_sesion(self):
        '''Este metodo despliega la ventana de edicion'''
        self.contenido.destroy()
        self.contenido = CTkFrame(self, fg_color="#3d1c57")
        self.contenido.pack(fill="both", expand=True)
        self.repartir_espacio()
        self.opciones()

    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.contenido.grid_columnconfigure(0, weight=1)
        self.contenido.grid_columnconfigure(1, weight=0)
        self.contenido.grid_columnconfigure(2, weight=1)
        self.contenido.grid_columnconfigure(3, weight=0)
        self.contenido.grid_columnconfigure(4, weight=1)

        self.contenido.grid_rowconfigure(0, weight=1)
        self.contenido.grid_rowconfigure(1, weight=0)
        self.contenido.grid_rowconfigure(2, weight=1)
        self.contenido.grid_rowconfigure(3, weight=0)
        self.contenido.grid_rowconfigure(4, weight=0)
        self.contenido.grid_rowconfigure(5, weight=1)
        self.contenido.grid_rowconfigure(6, weight=0)
        self.contenido.grid_rowconfigure(7, weight=1)

    def opciones(self):
        '''Crea los widget publico y ubicacion 
        junto con las opciones de funcionarios y profesor'''
        id_sesion = self.recuperar_id_sesion()
        publico, ubicacion = administrador.recuperar_ubicacion_publico(id_sesion)
        #---Publico---#
        self.publico = CTkOptionMenu(self.contenido, font=self.fuente,
        dropdown_font=self.fuente, fg_color= "#F6A623", text_color="#3d1c57",
        corner_radius=1, dropdown_fg_color="#3d1c57", dropdown_text_color= "#f0f0f0",
        dropdown_hover_color= "#F6A623", width= self.winfo_screenwidth() * 0.1,
        anchor= 'center', button_color="#3d1c57", button_hover_color="#3d1c57",
        values= ['PUBLICO','GENERAL', 'FUNCIONARIOS', 'FODUN'] )
        self.publico.grid(row=1, column=1)
        self.publico.set(publico)

        #---Ubicacion---#
        self.ubicacion = CTkOptionMenu(self.contenido, font=self.fuente,
        dropdown_font=self.fuente, fg_color= "#F6A623", text_color="#3d1c57",
        corner_radius=1, dropdown_fg_color="#3d1c57", dropdown_text_color= "#f0f0f0",
        dropdown_hover_color= "#F6A623", width= self.winfo_screenwidth() * 0.1,
        anchor= 'center', button_color="#3d1c57", button_hover_color="#3d1c57",
        values= ['UBICACION'] + administrador.recuperar_ubicaciones())
        self.ubicacion.grid(row=1, column=3)
        self.ubicacion.set(ubicacion)

        #---Funcionarios---
        funcionarios_label = CTkLabel(self.contenido, text='Funcionarios', text_color='whitesmoke',
                                      font=self.fuente, anchor='w')
        funcionarios_label.grid(row=3, column=1, sticky='w')

        self.funcionarios_frame = CTkScrollableFrame(self.contenido, fg_color="#2e1045")
        self.funcionarios_frame.grid(row=6, column=1, sticky='we')

        #---Profesor---
        profesor_label = CTkLabel(self.contenido, text='Profesor', text_color='whitesmoke',
                                      font=self.fuente, anchor='w')
        profesor_label.grid(row=3, column=3, sticky='w')

        self.profesor_frame = CTkScrollableFrame(self.contenido, fg_color="#2e1045")
        self.profesor_frame.grid(row=6, column=3, sticky='we')

        self.desplegable_funcionarios()
        self.desplegable_profesor()

        CTkButton(self.contenido, text = 'EDITAR',
                  font= self.fuente,
                  command=self.actualizar_sesion,
                  fg_color= "#F6A623",
                  text_color="#3d1c57",
                  hover_color="#FFB641").grid(row=7, column=2, sticky='we')

    def recuperar_id_sesion(self):
        '''Este_metodo_recupera el id de la sesion seleccionada '''
        celda = self.master.master.master
        seleccion_actividad: CTkOptionMenu = celda.master.master.opciones_busqueda

        fecha_hora = celda.fecha_hora
        actividad = seleccion_actividad.get()

        return general.hay_sesiones(actividad, fecha_hora)

    def desplegable_funcionarios(self):
        '''Crea el desplegable para escoger funcinarios'''

        funcionarios = administrador.recuperar_funcionarios()
        id_sesion = self.recuperar_id_sesion()
        asignados = administrador.recuperar_funcionarios_en_sesion(id_sesion)
        self.check_vars = []
        for indice, funcionario in enumerate(funcionarios):
            check_var = BooleanVar(value=funcionario[1] in asignados)
            fun_ceckbox = CTkCheckBox(
                self.funcionarios_frame,
                font=self.fuente,
                fg_color="#F6A623",
                text_color="whitesmoke",
                text=funcionario[0],
                hover_color="#FFD591",
                variable=check_var)
            fun_ceckbox.grid(row=indice, column=0, sticky='w')
            self.check_vars.append((funcionario[1], check_var))

    def desplegable_profesor(self):
        '''Crea el desplegable para escoger funcinarios'''
        funcionarios = administrador.recuperar_funcionarios()
        id_sesion = self.recuperar_id_sesion()
        asignado = administrador.recuperar_profesor_en_sesion(id_sesion)
        self.profesor = asignado
        self.profesores = []
        for indice, funcionario in enumerate(funcionarios):

            check_var = BooleanVar(value=funcionario[1] in asignado)

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
                    self.profesor = opcion

    def actualizar_sesion(self):
        '''Este metodo recupera la información 
        del formulario y actualiza los datos'''
        id_sesion = self.recuperar_id_sesion()
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

        administrador.eliminar_funcionarios_en_sesion(id_sesion=id_sesion)
        administrador.asignar_funcionarios(seleccionados, id_sesion, profesor[0])
        administrador.actualizar_publico_ubicacion(id_sesion, publico=publico, ubicacion=ubicacion)
        self.master.destroy()
