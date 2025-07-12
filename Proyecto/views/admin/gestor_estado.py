'''Modulo para gestionar el estado de miembros activos e inactivos'''

from datetime import datetime
from tkinter import Event, messagebox

from customtkinter import (CTkButton, CTkEntry, CTkFrame, CTkLabel,
                           CTkScrollableFrame)
from services import administrador


class GestionEstado(CTkFrame):
    '''Módulo de Administrador: gestión de estado de miembros activos/inactivos'''

    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="#2e1045")
        self.repartir_espacio()

        self.titulo = CTkLabel(self, text="GESTIÓN DE ESTADO DE MIEMBROS",
                                font=("Segoe UI", 28, "bold"), text_color="white")
        self.titulo.grid(row=0, column=0, columnspan=3, pady=20)

        self.crear_encabezado_derecho()
        self.crear_listas()
        self.crear_botones()
        self.crear_busqueda()

    def crear_encabezado_derecho(self):
        '''Encabezado con TURNO y botón Log Out'''
        mini_encabezado = CTkFrame(self, fg_color="transparent")
        mini_encabezado.grid(row=0, column=2, sticky="ne", padx=20, pady=(20, 10))

        mini_encabezado.grid_columnconfigure(0, weight=1)
        mini_encabezado.grid_columnconfigure(1, weight=0)

        turno_actual = self.obtener_turno_actual()
        turno_label = CTkLabel(mini_encabezado, text=f"TURNO: {turno_actual}",
                            text_color="white", font=("Arial", 16, "bold"))
        turno_label.grid(row=0, column=0, sticky="e", padx=(0, 10))

    def obtener_turno_actual(self):
        '''Devuelve el turno actual como string (7-8am, etc)'''
        hora = datetime.now().hour
        if 7 <= hora < 19:
            siguiente = hora + 1
            sufijo_fin = "am" if siguiente < 12 else "pm"
            return f"{hora}-{siguiente}{sufijo_fin}"
        return "Fuera de horario"

    def repartir_espacio(self):
        '''Configura el espacio de la ventana'''
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)

        self.grid_rowconfigure(0, weight=0)  # Título
        self.grid_rowconfigure(1, weight=1)  # Espacio entre título y listas
        self.grid_rowconfigure(2, weight=4)  # Contenedores de listas y botones
        self.grid_rowconfigure(3, weight=0)  # Barra de búsqueda


    def crear_listas(self):
        '''Crea los scrollables para miembros activos e inactivos'''
        self.fuente_label = ("Segoe UI", 20, "bold")

        self.botones: dict[str: CTkButton] = {}
        self.botones_seleccionados: list[CTkButton] = []
        self.usuarios_inactivos: dict[CTkButton: str] = {}

        # Título INACTIVOS
        label_inactivos = CTkLabel(self, text="INACTIVOS", anchor='center',
                       font=self.fuente_label, text_color="whitesmoke")
        label_inactivos.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="ew")

        # ScrollFrame INACTIVOS
        self.scroll_inactivos = CTkScrollableFrame(self, fg_color="#3d1c57")
        self.scroll_inactivos.grid(row=2, column=0, padx=20, sticky="nsew")

        self.inactivos = administrador.recuperar_miembros_inactivos()
        for miembro in self.inactivos.keys():
            boton = CTkButton(self.scroll_inactivos, text=self.inactivos[miembro],
                              text_color='whitesmoke',
                      fg_color='transparent', font=self.fuente_label, hover_color="#d18c1a")
            boton.pack(pady=5, fill='x')
            boton.bind("<Button-1>", self.actualizar_seleccion)
            self.usuarios_inactivos[boton] = miembro
            self.botones[miembro] = boton

        # Título ACTIVOS
        label_activos = CTkLabel(self, text="ACTIVOS", anchor='center',
                     font=self.fuente_label, text_color="whitesmoke")
        label_activos.grid(row=1, column=2, padx=20, pady=(10, 0), sticky="ew")

        # ScrollFrame ACTIVOS
        self.scroll_activos = CTkScrollableFrame(self, fg_color="#3d1c57")
        self.scroll_activos.grid(row=2, column=2, padx=20, sticky="nsew")

        self.activos = administrador.recuperar_miembros_activos()
        for miembro in self.activos.keys():
            boton = CTkButton(self.scroll_activos, text=self.activos[miembro],
                              text_color='whitesmoke',
                      fg_color='transparent', font=self.fuente_label, hover_color="#d18c1a")
            boton.pack(pady=5, fill='x')
            self.botones[miembro] = boton

    def crear_botones(self):
        '''Botones para mover miembros entre listas'''
        contenedor = CTkFrame(self, fg_color="transparent")
        contenedor.grid(row=2, column=1, sticky="nsew")

        contenedor.grid_rowconfigure((0, 1, 2), weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        self.boton_derecha = CTkButton(contenedor, text="-->", font=("Segoe UI", 26, "bold"),
                                    width=50, height=35, anchor="center",
                                    fg_color="#f6a623", hover_color="#d18c1a", text_color="#2e1045",
                                    command=self.activar_miembro)
        self.boton_derecha.grid(row=0, column=0, pady=10)

        self.boton_izquierda = CTkButton(contenedor, text="Inactivar a todos",
                                        font=self.fuente_label,
                                        width=50, height=35,
                                        fg_color="#f6a623", hover_color="#d18c1a",
                                        text_color="#2e1045",
                                        command=self.desactivar_miembros)
        self.boton_izquierda.grid(row=2, column=0, pady=10)

    def crear_busqueda(self):
        '''Barra para buscar miembros'''
        self.frame_busqueda = CTkFrame(self, fg_color="transparent")
        self.frame_busqueda.grid(row=3, column=0, columnspan=3, pady=(30, 20), sticky="n")
        self.frame_busqueda.grid_columnconfigure(0)
        self.frame_busqueda.grid_columnconfigure(1)

        self.entry_busqueda = CTkEntry(self.frame_busqueda, placeholder_text="Búsqueda de usuario",
                                    fg_color="white", text_color="black",
                                    width=300, height=30, font=("Segoe UI", 16),
                                    corner_radius=1, border_width=0)
        self.entry_busqueda.grid(row=0, column=0, sticky='ne')

        self.boton_busqueda = CTkButton(self.frame_busqueda, text="Buscar",
                                        font=("Segoe UI", 16, "bold"),
                                        width=50, height=30, corner_radius=1,
                                        fg_color="#f6a623", hover_color="#d18c1a",
                                        text_color="#2e1045", command=self.buscar_miembro)
        self.boton_busqueda.grid(row=0, column=1, sticky='w')

    def actualizar_seleccion(self, event:Event):
        '''Actualiza la selección de miembros activos/inactivos'''
        if event:
            boton = event.widget.master
            if boton not in self.botones_seleccionados:
                self.botones_seleccionados.append(boton)
                boton.configure(fg_color="#f6a623", hover_color="#d18c1a",)
            else:
                self.botones_seleccionados.remove(boton)
                boton.configure(fg_color='#3d1c57', hover_color='#f6a623')

    def actualizar_listas(self):
        '''Esta funcion refresca los valores de cada scrollableframe'''
        # Elimina los frames scrollables actuales
        self.scroll_inactivos.destroy()
        self.scroll_activos.destroy()
        # Limpia las listas de selección
        self.botones_seleccionados.clear()
        self.usuarios_inactivos.clear()
        # Vuelve a crear las listas
        self.crear_listas()

    def activar_miembro(self):
        '''Función para cambiar el estado de un miembro a activo'''
        usuarios = []
        for boton in self.botones_seleccionados:
            usuarios.append(self.usuarios_inactivos[boton])

        administrador.activar_miembros(usuarios)
        self.actualizar_listas()

    def desactivar_miembros(self):
        '''Funcion para inactivar a todos los miembros'''
        #Ventana de confirmacion
        confirmacion = messagebox.askokcancel('Confirmación de acción',
                '¿Está seguro de inactivar a TODOS los miembros?\nEsta acción NO se puede deshacer')

        if confirmacion:
            usuarios = [usuario for usuario in self.activos.keys()]
            administrador.desactivar_miembros(usuarios)

            self.actualizar_listas()

    def buscar_miembro(self):
        '''Esta funcion encuentra un mimebro por su usuario'''
        usuario_a_buscar = self.entry_busqueda.get()
        if  usuario_a_buscar == '':
            messagebox.showerror('Campos vacíos',
                                 'Por favor ingrese el usuario de un miembro para buscarlo.')
            return
        else:
            boton = None

            for miembro in self.activos:
                if miembro == usuario_a_buscar:
                    boton = self.botones[miembro]
                    messagebox.showinfo('Consulta exitosa',
                                        'El miembro se encuentra ACTIVO. ' +
                                        'Recorra los miembros activos hasta encontrarlo')

            for miembro in self.inactivos:
                if miembro == usuario_a_buscar:
                    boton = self.botones[miembro]
                    messagebox.showinfo('Consulta exitosa', 'El miembro se encuentra INACTIVO.' +
                                        ' Recorra los miembros inactivos hasta encontrarlo')

            if boton:
                self.resaltar_boton_temporal(boton, color_original=boton.cget('fg_color'))
            else:
                messagebox.showerror('Usuario no encontrado',
                    'No se encontró ningun miembro con este usuario, por favor verifiquelo')

    def resaltar_boton_temporal(self, boton:CTkButton, tiempo=3000, color_original="transparent"):
        '''Resalta un boton de forma temporal'''
        color_resaltado="#f65f23"

        boton.configure(fg_color=color_resaltado)
        boton.focus()

        # Restaurar color después de 'tiempo' milisegundos
        self.after(tiempo, lambda: boton.configure(fg_color=color_original))
