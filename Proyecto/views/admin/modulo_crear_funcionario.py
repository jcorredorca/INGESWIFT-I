from tkinter import messagebox

from core import utils
from customtkinter import (CTkButton, CTkEntry, CTkFrame, CTkLabel,
                           CTkScrollableFrame, CTkTextbox)

from ..components.boton_adicional import BotonAdicional


class CrearFuncionarios(CTkFrame):
    '''Módulo de Administrador: Lista y registro de funcionarios'''

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#2e1045", corner_radius=1)

        self.registrados = {
            "jcorredorca@unal.edu.co": "Juan Pablo Corredor Castañeda",
            "nbolanosf@unal.edu.co": "Nicolás Andrés Bolaños Fernández",
            "lalvarezla@unal.edu.co": "Laura Vanesa Álvarez Lafont",
            "sfetecua@unal.edu.co": "Santiago Andrés Fetecua Pulgarín"
        }
        self.funcionarios_activos = ["Nombre 1", "Nombre 2", "Nombre 3", "Nombre 4", "Nombre 5"]

        self.repartir_espacio()
        self.crear_encabezado_derecho()

        self.seccion = CTkFrame(self, fg_color="transparent")
        self.seccion.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.mostrar_lista_funcionarios()

    def crear_encabezado_derecho(self):
        '''Crea el encabezado superior derecho con el botón de cierre de sesión.'''
        mini_encabezado = CTkFrame(self, fg_color="transparent")
        mini_encabezado.grid(row=0, column=2, sticky="ne", padx=20, pady=(20, 10))
        mini_encabezado.grid_columnconfigure(0, weight=1)
        mini_encabezado.grid_columnconfigure(1, weight=0)

    def repartir_espacio(self):
        '''Configura el layout del frame principal,
        distribuyendo el espacio entre filas y columnas.'''
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def mostrar_lista_funcionarios(self):
        '''Muestra la lista de funcionarios activos en una sección scrollable.'''
        for widget in self.seccion.winfo_children():
            widget.destroy()

        self.seccion.grid_columnconfigure((0,1,2), weight=1)
        CTkLabel(self.seccion, text="FUNCIONARIOS ACTIVOS",
                 font=("Segoe UI", 28, "bold"), text_color="white")\
            .grid(row=0, column=1, pady=(30, 10))

        lista_scroll = CTkScrollableFrame(self.seccion, fg_color="#3d1c57")
        lista_scroll.grid(row=1, column=1, padx=30, pady=(10, 20), sticky="nsew")

        for nombre in self.funcionarios_activos:
            CTkLabel(lista_scroll, text=nombre, text_color="white",
                     font=("Segoe UI", 18), anchor="center", justify="center")\
                     .pack(fill="x", pady=6, padx=20)

        CTkButton(self.seccion, text="Registrar Funcionario",
                  font=("Segoe UI", 18, "bold"), width=220,
                  fg_color="#f6a623", hover_color="#d18c1a",
                  text_color="#2e1045", corner_radius=10,
                  command=self.mostrar_formulario_correo)\
            .grid(row=2, column=1, pady=(0, 30))

    def mostrar_formulario_correo(self):
        '''Muestra el formulario inicial para ingresar y validar el correo del nuevo funcionario.'''
        for widget in self.seccion.winfo_children():
            widget.destroy()
        self.seccion.grid_columnconfigure((0,1,2), weight=1)

        CTkButton(self.seccion, text="←", width=40, height=35,
                  font=("Segoe UI", 20, "bold"), fg_color="#f6a623",
                  hover_color="#d18c1a", text_color="#2e1045",
                  command=self.mostrar_lista_funcionarios).grid(row=0, column=0, padx=(30, 0), sticky="w")

        CTkLabel(self.seccion, text="MÓDULO DE REGISTRO",
                 font=("Segoe UI", 28, "bold"), text_color="white")\
            .grid(row=1, column=1, pady=(30, 10))

        CTkLabel(self.seccion, text="Introduce el correo electrónico para continuar",
                 font=("Segoe UI", 18), text_color="white")\
            .grid(row=2, column=1, pady=(10, 10))

        self.entry_correo = CTkEntry(self.seccion, placeholder_text="Correo",
                                     font=("Segoe UI", 16), width=400,
                                     fg_color="white", text_color="black")
        self.entry_correo.grid(row=3, column=1, pady=(5, 20))

        CTkButton(self.seccion, text="VALIDAR",
                  font=("Segoe UI", 18, "bold"), width=120,
                  fg_color="#f6a623", hover_color="#d18c1a",
                  text_color="#2e1045", corner_radius=10,
                  command=self.verificar_correo).grid(row=4, column=1, pady=(0, 30))

    def verificar_correo(self):
        '''Verifica si el correo ingresado está registrado previamente o es nuevo.'''
        correo = self.entry_correo.get().strip().lower()

        if not correo:
            messagebox.showwarning("Campo vacío", "Por favor ingrese un correo antes de validar.")
            return

        if correo in self.registrados:
            self.mostrar_confirmacion_existente(correo)
        else:
            self.mostrar_formulario_completo(correo)

    def mostrar_confirmacion_existente(self, correo):
        '''Muestra confirmación si el correo ya está en la base de datos.'''
        for widget in self.seccion.winfo_children():
            widget.destroy()
        self.seccion.grid_columnconfigure((0,1,2), weight=1)

        CTkButton(self.seccion, text="←", width=40, height=35,
                  font=("Segoe UI", 20, "bold"), fg_color="#f6a623",
                  hover_color="#d18c1a", text_color="#2e1045",
                  command=self.mostrar_formulario_correo).grid(row=0, column=0, padx=(30, 0), sticky="w")

        CTkLabel(self.seccion, text="MÓDULO DE REGISTRO",
                 font=("Segoe UI", 28, "bold"), text_color="white")\
            .grid(row=1, column=1, pady=(30, 10))

        CTkLabel(self.seccion,
                 text="Este usuario ya está en la base de datos, ¿Desea registrarlo?",
                 font=("Segoe UI", 18), text_color="white", wraplength=600, justify="center")\
            .grid(row=2, column=1, pady=(10, 20))

        CTkButton(self.seccion, text="VALIDAR",
                  font=("Segoe UI", 18, "bold"), width=120,
                  fg_color="#f6a623", hover_color="#d18c1a",
                  text_color="#2e1045", corner_radius=10,
                  command=lambda: self.registrar_existente(correo))\
            .grid(row=3, column=1, pady=(0, 30))

    def mostrar_formulario_completo(self, correo):
        '''Muestra el formulario completo para registrar un nuevo funcionario.'''
        for widget in self.seccion.winfo_children():
            widget.destroy()
        self.seccion.grid_columnconfigure((0,1,2), weight=1)

        CTkButton(self.seccion, text="←", width=40, height=35,
                  font=("Segoe UI", 20, "bold"), fg_color="#f6a623",
                  hover_color="#d18c1a", text_color="#2e1045",
                  command=self.mostrar_formulario_correo).grid(row=0, column=0, padx=(30, 0), sticky="w")

        CTkLabel(self.seccion, text="MÓDULO DE REGISTRO",
                 font=("Segoe UI", 28, "bold"), text_color="white")\
            .grid(row=1, column=1, pady=(30, 10))

        self.entry_nombre = CTkEntry(self.seccion, placeholder_text="Nombre completo",
                                     font=("Segoe UI", 16), width=400,
                                     fg_color="white", text_color="black")
        self.entry_nombre.grid(row=2, column=1, pady=(10, 10))

        self.entry_rol = CTkEntry(self.seccion, placeholder_text="Rol en la universidad",
                                  font=("Segoe UI", 16), width=400,
                                  fg_color="white", text_color="black")
        self.entry_rol.grid(row=3, column=1, pady=(10, 10))

        self.entry_correo_final = CTkEntry(self.seccion)
        self.entry_correo_final.insert(0, correo)
        self.entry_correo_final.configure(state="disabled")
        self.entry_correo_final.grid(row=4, column=1, pady=(10, 20))

        CTkButton(self.seccion, text="VALIDAR",
                  font=("Segoe UI", 18, "bold"), width=120,
                  fg_color="#f6a623", hover_color="#d18c1a",
                  text_color="#2e1045", corner_radius=10,
                  command=self.registrar_nuevo).grid(row=5, column=1, pady=(0, 30))

    def registrar_existente(self, correo):
        '''Agrega a la lista de activos a un funcionario ya registrado si aún no está.'''
        nombre = self.registrados.get(correo, correo)
        if nombre not in self.funcionarios_activos:
            self.funcionarios_activos.append(nombre)
        self.mostrar_lista_funcionarios()

    def registrar_nuevo(self):
        '''Valida y registra un nuevo funcionario, si no existe ya en la lista.'''
        nombre = self.entry_nombre.get().strip()
        rol = self.entry_rol.get().strip()

        if not nombre or not rol:
            messagebox.showwarning("Campos incompletos", "Por favor complete todos los campos.")
            return

        if nombre in self.funcionarios_activos:
            messagebox.showinfo("Ya registrado", f"{nombre} ya se encuentra en la lista de funcionarios.")
            return

        self.funcionarios_activos.append(nombre)
        self.mostrar_lista_funcionarios()

