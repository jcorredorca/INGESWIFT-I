import re
from tkinter import messagebox

from customtkinter import (CTkButton, CTkEntry, CTkFrame, CTkLabel,
                           CTkOptionMenu, CTkScrollableFrame)
from models.conexion import Conexion
from services import login


class CrearFuncionarios(CTkFrame):
    '''Módulo de Administrador: Lista y registro de funcionarios'''

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#2e1045", corner_radius=1)

        self.funcionarios_activos = self.cargar_funcionarios_activos()

        self.repartir_espacio()

        self.seccion = CTkFrame(self, fg_color="transparent")
        self.seccion.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.mostrar_lista_funcionarios()

        self.entry_correo = None
        self.entry_correo_final = None
        self.entry_grupo = None
        self.rol_seleccionado = None
        self.opciones_rol = None
        self.opciones_grupo = None
        self.entry_apellido = None
        self.entry_nombre = None

    def repartir_espacio(self):
        '''Configura el layout del frame principal, distribuyendo el espacio entre filas y columnas.'''
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)

    def mostrar_lista_funcionarios(self):
        '''Muestra la lista de funcionarios activos en una sección scrollable.'''
        self.funcionarios_activos = self.cargar_funcionarios_activos()
        for widget in self.seccion.winfo_children():
            widget.destroy()

        self.seccion.grid_columnconfigure((0,1,2), weight=1)
        CTkLabel(self.seccion, text="FUNCIONARIOS ACTIVOS",
                 font=("Libre Baskerville", 28, "bold"), text_color="white")\
            .grid(row=0, column=1, pady=(30, 10))

        lista_scroll = CTkScrollableFrame(self.seccion, fg_color="#3d1c57")
        lista_scroll.grid(row=1, column=1, padx=30, pady=(10, 20), sticky="nsew")

        for nombre, apellido, correo in self.funcionarios_activos:
            texto = f"👤 {nombre} {apellido}\n📧 {correo}"
            CTkLabel(lista_scroll, text=texto, text_color="white",
                    font=("Libre Baskerville", 26), anchor="center", justify="center")\
                    .pack(fill="x", pady=6, padx=20)

        CTkButton(self.seccion, text="Registrar Funcionario",
                  font=("Segoe UI", 20, "bold"), width=260, height=45,
                  fg_color="#f6a623", hover_color="#d18c1a",
                  text_color="#2e1045", corner_radius=12,
                  command=self.mostrar_formulario_correo)\
                    .grid(row=2, column=1, pady=(0, 40))

    def mostrar_formulario_correo(self):
        '''Muestra el formulario inicial para ingresar y validar el correo del nuevo funcionario.'''
        for widget in self.seccion.winfo_children():
            widget.destroy()

        self.seccion.grid_columnconfigure((0,1,2), weight=1)

        CTkButton(self.seccion, text="←", width=80, height=70,
                  font=("Segoe UI", 40, "bold"), fg_color="#f6a623",
                  hover_color="#d18c1a", text_color="#2e1045",
                  command=self.mostrar_lista_funcionarios)\
                    .grid(row=0, column=0, padx=(30, 0), sticky="nw")

        CTkLabel(self.seccion, text="MÓDULO DE REGISTRO",
                 font=("Libre Baskerville", 56, "bold"), text_color="white")\
            .grid(row=1, column=1, pady=(40, 20))

        CTkLabel(self.seccion, text="Introduce el correo electrónico para continuar",
                 font=("Libre Baskerville", 36), text_color="white")\
            .grid(row=2, column=1, pady=(10, 10))

        self.entry_correo = CTkEntry(self.seccion, placeholder_text="Correo",
                                     font=("Libre Baskerville", 32), width=400,
                                     fg_color="white", text_color="black")
        self.entry_correo.grid(row=3, column=1, pady=(5, 20))

        CTkButton(self.seccion, text="VALIDAR",
                  font=("Segoe UI", 36, "bold"), width=240,
                  fg_color="#f6a623", hover_color="#d18c1a",
                  text_color="#2e1045", corner_radius=10,
                  command=self.verificar_correo).grid(row=4, column=1, pady=(0, 30))

    def verificar_correo(self):
        '''Consulta en la base de datos si el correo existe y decide a dónde ir.'''
        correo = self.entry_correo.get().strip().lower()

        if not correo:
            messagebox.showwarning("Campo vacío", "Por favor ingrese un correo antes de validar.")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            messagebox.showwarning("Correo inválido", "Por favor ingrese un correo válido.")
            return

        conexion = Conexion()

        query_usuario = "SELECT usuario FROM personas WHERE correo = ?"
        resultado = conexion.ejecutar_consulta(query_usuario, [correo])

        if not resultado:
            self.mostrar_formulario_completo(correo)
            return

        usuario = resultado[0][0]

        query_funcionario = """
            SELECT 1 FROM rol_persona
            WHERE personas_usuario = ? AND rol_nombre = 'FUNCIONARIO'
        """
        es_funcionario = conexion.ejecutar_consulta(query_funcionario, [usuario])

        if es_funcionario:
            messagebox.showerror("Acción inválida", "El usuario ya es Funcionario. Ingrese un correo válido.")
            return

        query_miembro = """
            SELECT 1 FROM rol_persona
            WHERE personas_usuario = ? AND rol_nombre = 'MIEMBRO'
        """
        es_miembro = conexion.ejecutar_consulta(query_miembro, [usuario])

        if es_miembro:
            self.mostrar_confirmacion_existente(correo)
        else:
            self.mostrar_formulario_completo(correo)


    def mostrar_confirmacion_existente(self, correo):
        '''Muestra confirmación si el correo ya está en la base de datos.'''
        for widget in self.seccion.winfo_children():
            widget.destroy()
        self.seccion.grid_columnconfigure((0,1,2), weight=1)

        CTkButton(self.seccion, text="←", width=80, height=70,
                  font=("Segoe UI", 40, "bold"), fg_color="#f6a623",
                  hover_color="#d18c1a", text_color="#2e1045",
                  command=self.mostrar_formulario_correo)\
                    .grid(row=0, column=0, padx=(30, 0), sticky="w")

        CTkLabel(self.seccion, text="MÓDULO DE REGISTRO",
                 font=("Libre Baskerville", 56, "bold"), text_color="white")\
            .grid(row=1, column=1, pady=(40, 20))

        CTkLabel(self.seccion,
                 text="Este usuario ya está en la base de datos, ¿Desea registrarlo?",
                 font=("Libre Baskerville", 36), text_color="white",
                 wraplength=600, justify="center")\
            .grid(row=2, column=1, pady=(10, 20))

        CTkButton(self.seccion, text="VALIDAR",
                  font=("Segoe UI", 36, "bold"), width=240,
                  fg_color="#f6a623", hover_color="#d18c1a",
                  text_color="#2e1045", corner_radius=10,
                  command=lambda: self.registrar_existente(correo))\
            .grid(row=3, column=1, pady=(0, 30))

    def mostrar_formulario_completo(self, correo):
        '''Muestra el formulario completo para registrar un nuevo funcionario.'''
        for widget in self.seccion.winfo_children():
            widget.destroy()
        self.seccion.grid_columnconfigure((0,1,2), weight=1)

        CTkButton(self.seccion, text="←", width=80, height=70,
                font=("Segoe UI", 40, "bold"), fg_color="#f6a623",
                hover_color="#d18c1a", text_color="#2e1045",
                command=self.mostrar_formulario_correo)\
                    .grid(row=0, column=0, padx=(30, 0), sticky="w")

        CTkLabel(self.seccion, text="MÓDULO DE REGISTRO",
                font=("Libre Baskerville", 56, "bold"), text_color="white")\
            .grid(row=1, column=1, pady=(40, 20))

        self.entry_nombre = CTkEntry(self.seccion, placeholder_text="Nombre *",
                                    font=("Libre Baskerville", 32), width=400,
                                    fg_color="white", text_color="black")
        self.entry_nombre.grid(row=2, column=1, pady=(10, 10))

        self.entry_apellido = CTkEntry(self.seccion, placeholder_text="Apellido *",
                                    font=("Libre Baskerville", 32), width=400,
                                    fg_color="white", text_color="black")
        self.entry_apellido.grid(row=3, column=1, pady=(10, 10))

        self.opciones_rol = ["GENERAL", "FUNCIONARIO", "FODUN", "CUIDADO"]
        self.rol_seleccionado = CTkOptionMenu(self.seccion, values=self.opciones_rol,
                                            font=("Libre Baskerville", 32), width=400,
                                            fg_color="white", button_color="#e5e5e5",
                                            text_color="black", dropdown_fg_color="white",
                                            dropdown_text_color="black")
        self.rol_seleccionado.set("GENERAL")
        self.rol_seleccionado.grid(row=4, column=1, pady=(10, 10))

        self.opciones_grupo = ['JOVENES', 'SELECCION']
        self.entry_grupo = CTkOptionMenu(self.seccion, values=self.opciones_grupo,
                                            font=("Libre Baskerville", 32), width=400,
                                            fg_color="white", button_color="#e5e5e5",
                                            text_color="black", dropdown_fg_color="white",
                                            dropdown_text_color="black")
        self.entry_grupo.grid(row=5, column=1, pady=(10, 10))

        self.entry_correo_final = CTkEntry(self.seccion,
                                           font=("Libre Baskerville", 32),
                                           width=400,
                                           fg_color="white",
                                           text_color="black")
        self.entry_correo_final.insert(0, correo)
        self.entry_correo_final.configure(state="disabled")
        self.entry_correo_final.grid(row=6, column=1, pady=(10, 20))

        CTkButton(self.seccion, text="REGISTRAR",
                font=("Segoe UI", 36, "bold"), width=240,
                fg_color="#f6a623", hover_color="#d18c1a",
                text_color="#2e1045", corner_radius=10,
                command=self.registrar_nuevo)\
            .grid(row=7, column=1, pady=(0, 30))

    def registrar_existente(self, correo):
        '''Agrega a la base de datos el rol FUNCIONARIO si aún no lo tiene'''
        conexion = Conexion()
        query = "SELECT usuario FROM personas WHERE correo = ?"
        resultado = conexion.ejecutar_consulta(query, [correo])

        if resultado:
            usuario = resultado[0][0]

            rol_existente = conexion.ejecutar_consulta("""
                SELECT 1 FROM rol_persona WHERE personas_usuario = ? AND rol_nombre = 'FUNCIONARIO'
            """, [usuario])

            if not rol_existente:
                conexion.ejecutar_consulta("""
                    INSERT INTO rol_persona (personas_usuario, rol_nombre)
                    VALUES (?, 'FUNCIONARIO')
                """, [usuario])

            if correo not in self.funcionarios_activos:
                self.funcionarios_activos.append(correo)

            self.mostrar_lista_funcionarios()

    def registrar_nuevo(self):
        '''Agrega a la base de datos a un nuevo funcionario.'''
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        rol_uni = self.rol_seleccionado.get()
        grupo = self.entry_grupo.get().strip().upper() or None
        correo = self.entry_correo_final.get().strip().lower()

        if not nombre or not apellido or not rol_uni or not correo:
            messagebox.showwarning("Campos incompletos", "Por favor complete todos los campos obligatorios.")
            return

        if rol_uni not in ['GENERAL', 'FUNCIONARIO', 'FODUN', 'CUIDADO']:
            messagebox.showwarning("Rol inválido", "El rol en la universidad no es válido.")
            return

        usuario = correo.split('@')[0]
        contrasena_default = login.hash_contrasena("1")
        estado = "ACTIVO"

        conexion = Conexion()

        try:
            conexion.ejecutar_consulta("""
                INSERT INTO personas (usuario, nombre, apellido, hash_contrasena, estado, correo, rol_en_universidad, grupo_especial)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [usuario, nombre, apellido, contrasena_default, estado, correo, rol_uni, grupo])

            conexion.ejecutar_consulta("""
                INSERT INTO rol_persona (personas_usuario, rol_nombre)
                VALUES (?, ?), (?, ?)
            """, [usuario, "FUNCIONARIO", usuario, "MIEMBRO"])

            self.funcionarios_activos.append(correo)
            messagebox.showinfo("Éxito", f"Funcionario {nombre} registrado con éxito.")
            self.mostrar_lista_funcionarios()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al registrar: {e}")

    def cargar_funcionarios_activos(self):
        '''Carga los correos de los funcionarios activos desde la base de datos.'''
        conexion = Conexion()
        query = """
            SELECT p.nombre, p.apellido, p.correo
            FROM personas p
            JOIN rol_persona rp ON p.usuario = rp.personas_usuario
            JOIN rol r ON rp.rol_nombre = r.nombre
            WHERE r.nombre IN ('FUNCIONARIO', 'ADMINISTRADOR')
            GROUP BY p.usuario
        """
        resultados = conexion.ejecutar_consulta(query)
        return [(nombre, apellido, correo) for (nombre, apellido, correo) in resultados]
