'''Módulo para la pantalla de registrar miembros en el sistema'''

from datetime import datetime
from tkinter import messagebox

from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkComboBox,  CTkButton
from services.login import hash_contrasena
from services import funcionario
from ..components import boton_adicional

class RegistroMiembro(CTkFrame):
    '''Frame para la pantalla de regitrar miembros'''

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#2e1045")

        self.fuente_titulo = max(28, int(self.winfo_screenwidth() * 0.02))
        self.fuente_general = max(16, int(self.winfo_screenwidth() * 0.012))

        self.crear_encabezado()
        self.crear_contenido()

    def crear_encabezado(self):
        '''Funcion para crear el encabezado interno de la pantalla'''
        encabezado = CTkFrame(self, fg_color="transparent")
        encabezado.pack(fill="x", padx=20, pady=(10, 0), anchor="ne")

        encabezado.grid_columnconfigure(0, weight=1)
        encabezado.grid_columnconfigure(1, weight=0)

        turno = self.obtener_turno_actual()
        turno_label = CTkLabel(encabezado, text=f"TURNO: {turno}",
                               text_color="white", font=("Arial", 16, "bold"))
        turno_label.grid(row=0, column=0, sticky="e", padx=(0, 10))

    def crear_contenido(self):
        '''Funcion para llenar el frame'''
        contenedor = CTkFrame(self, fg_color="transparent")
        contenedor.pack(expand=True, pady=60)

        titulo = CTkLabel(contenedor, text="MÓDULO DE REGISTRO DE MIEMBRO",
                          font=("Arial", self.fuente_titulo, "bold"),
                          text_color="white")
        titulo.pack(pady=(0, 40))
        disclaimer = CTkLabel(contenedor, text="Los campos marcados con * son obligatorios",
                          font=("Arial", self.fuente_general), anchor='w',
                          text_color="white")
        disclaimer.pack(pady=(0, 40))

        # Campos organizados en una cuadrícula 3x2
        formulario = CTkFrame(contenedor, fg_color="transparent")
        formulario.pack()

        campos = [
            ("Nombres *", 0, 0),
            ("Apellidos *", 0, 1),
            ("Identificación *", 1, 0),
        ]

        self.entries = {}

        for texto, fila, columna in campos:
            entry = CTkEntry(formulario, placeholder_text=texto,
                             font=("Arial", self.fuente_general),
                             fg_color="white", text_color="black", height=40, width=200)
            entry.grid(row=fila, column=columna, padx=15, pady=10, ipadx=10)
            self.entries[texto] = (entry, True)

        #ComboBox para el rol en la universidad
        roles = ["--Rol en la universidad--", "GENERAL", "FUNCIONARIO", "FODUN", "CUIDADO"]
        combo_rol = CTkComboBox(formulario,
                                values=roles, font=("Arial", self.fuente_general),
                                width=220, height=40, fg_color="white", text_color="black",
                                button_color="#dddddd",
                                dropdown_font=("Arial", self.fuente_general),
                                dropdown_fg_color="white", dropdown_text_color="black")
        combo_rol.set("--Rol en la universidad--")
        combo_rol.grid(row=1, column=1, padx=15, pady=10)
        self.entries["Rol"] = (combo_rol, False)

        #Frame para el correo
        usuario_frame = CTkFrame(formulario, fg_color="transparent")
        usuario_frame.grid(row=2, column=0, pady=10, padx=15, sticky="new")

        usuario_frame.grid_columnconfigure(0, weight=4)
        usuario_frame.grid_columnconfigure(1, weight=1)

        entry_usuario = CTkEntry(usuario_frame, placeholder_text='Correo *',
                             font=("Arial", self.fuente_general),
                             fg_color="white", text_color="black", height=40, width=100)
        entry_usuario.grid(row=0, column=0, sticky='e', ipadx=10)
        self.entries["Correo *"] = (entry_usuario, True)

        dominio = CTkLabel(usuario_frame, text="@unal.edu.co", text_color="whitesmoke",
                           font=("Arial", self.fuente_general), width=90)

        dominio.grid(row=0, column=1, sticky="w", padx=(10, 0))

        # ComboBox para Programa
        programas = ["--Programa--", "Jóvenes a la U", "Selección deportiva"]
        combo_programa = CTkComboBox(formulario,
                                     values=programas, font=("Arial", self.fuente_general),
                                     width=220, height=40,
                                     fg_color="white", text_color="black",
                                     button_color="#dddddd",
                                     dropdown_font=("Arial", self.fuente_general),
                                     dropdown_fg_color="white", dropdown_text_color="black")
        combo_programa.set("--Programa--")
        combo_programa.grid(row=2, column=1, padx=15, pady=10)
        self.entries["Programa"] = (combo_programa, False)

        # Boton registrar
        boton = CTkButton(contenedor, text="REGISTRAR",
                          font=("Arial", self.fuente_general + 2, "bold"),
                          fg_color="#f6a623", text_color="black",
                          hover_color="#d38e14",
                          height=50, corner_radius=6, width=300,
                          command=self.registrar_miembro)
        boton.pack(pady=(30, 0))

    def obtener_turno_actual(self):
        '''Funcion que devuelve el turno actual y se actualiza según la hora del dispositivo'''
        hora = datetime.now().hour
        if 7 <= hora < 19:
            siguiente = hora + 1
            sufijo = "am" if siguiente < 12 else "pm"
            return f"{hora}-{siguiente}{sufijo}"
        return "Fuera de horario"

    def registrar_miembro(self):
        '''Esta función realiza la inscripcion del miembro en la db'''
        #Verifica que todos los campos estén llenos para poder registrar a la persona
        if self.campos_estan_vacios() or self.ya_esta_registrado(self.entries['Correo *'][0].get()):
            return

        contrasena = hash_contrasena(self.entries['Identificación *'][0].get())


        if self.entries['Rol'][0].get() != "--Rol en la universidad--":
            rol = self.entries['Rol'][0].get()
        else:
            rol = 'GENERAL'

        programa = None
        if self.entries["Programa"][0].get() == "--Programa--":
            programa = None
        elif self.entries["Programa"][0].get() == "Jóvenes a la U":
            programa = 'JOVENES'
        elif self.entries["Programa"][0].get() == "Selección deportiva":
            programa = 'SELECCION'

        info_miembro = {
            "usuario": self.entries['Correo *'][0].get().lower(),
            "nombre": self.entries['Nombres *'][0].get(),
            "apellido": self.entries['Apellidos *'][0].get(),
            "contrasena": contrasena,
            "correo": self.entries['Correo *'][0].get() + '@unal.edu.co',
            "rol": rol,
            "programa": programa,
        }

        try:
            funcionario.registrar_miembro(info_miembro)
        except ValueError as e:
            messagebox.showerror('Error', str(e))

        messagebox.showinfo('Registro exitoso', 'El miembro ha sido registrado exitosamente. \
                            Recuerde cambiar su contraseña al iniciar sesión por primera vez.')

        # Reinicia los campos del formulario
        for entry, _ in self.entries.values():
            if isinstance(entry, CTkComboBox):
                if entry == self.entries['Rol'][0]:
                    entry.set("--Rol en la universidad--")
                else:
                    entry.set("--Programa--")
            else:
                entry.delete(0, 'end')

    def campos_estan_vacios(self):
        '''Esta funcion verifica la información en los campos para hacer el registro'''

        alguno_vacio = False

        for entry, obligatorio in self.entries.values():
            if not obligatorio:
                continue
            if entry.get() == '':
                alguno_vacio = True

        if alguno_vacio:
            messagebox.showerror('Error', 'Hay al menos un campo obligatorio sin llenar')

        return alguno_vacio

    def ya_esta_registrado(self, usuario):
        '''Esta función valida si un usuario ya está registrado en la base de datos'''
        if funcionario.usuario_ya_registrado(usuario):
            messagebox.showerror('Error', 'El usuario ya está registrado en el sistema')
            return True

        return False
