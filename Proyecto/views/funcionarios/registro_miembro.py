from customtkinter import *
from datetime import datetime
from core import utils
from ..components import boton_adicional

class RegistroMiembro(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#2e1045")

        self.fuente_titulo = max(28, int(self.winfo_screenwidth() * 0.02))
        self.fuente_general = max(16, int(self.winfo_screenwidth() * 0.012))

        self.crear_encabezado()
        self.crear_contenido()

    def crear_encabezado(self):
        encabezado = CTkFrame(self, fg_color="transparent")
        encabezado.pack(fill="x", padx=20, pady=(10, 0), anchor="ne")

        encabezado.grid_columnconfigure(0, weight=1)
        encabezado.grid_columnconfigure(1, weight=0)

        turno = self.obtener_turno_actual()
        turno_label = CTkLabel(encabezado, text=f"TURNO: {turno}",
                               text_color="white", font=("Arial", 16, "bold"))
        turno_label.grid(row=0, column=0, sticky="e", padx=(0, 10))

    def crear_contenido(self):
        contenedor = CTkFrame(self, fg_color="transparent")
        contenedor.pack(expand=True, pady=60)

        titulo = CTkLabel(contenedor, text="MÓDULO DE REGISTRO DE MIEMBRO",
                          font=("Arial", self.fuente_titulo, "bold"),
                          text_color="white")
        titulo.pack(pady=(0, 40))

        # Campos organizados en una cuadrícula 3x2
        formulario = CTkFrame(contenedor, fg_color="transparent")
        formulario.pack()

        campos = [
            ("Nombres", 0, 0),
            ("Apellidos", 0, 1),
            ("Identificación", 1, 0),
            ("Edad", 1, 1),
            ("Rol universidad", 2, 0),
            ("Correo", 3, 0),
            ("Teléfono", 3, 1),
        ]

        self.entries = {}

        for texto, fila, columna in campos:
            entry = CTkEntry(formulario, placeholder_text=texto,
                             font=("Arial", self.fuente_general),
                             fg_color="white", text_color="black", height=40, width=200)
            entry.grid(row=fila, column=columna, padx=15, pady=10, ipadx=10)
            self.entries[texto] = entry

        # ComboBox para Programa
        combo_programa = CTkComboBox(formulario,
                                     values=["Jóvenes a la U", "Selección deportiva"],
                                     font=("Arial", self.fuente_general),
                                     width=200, height=40,
                                     fg_color="white", text_color="black",
                                     button_color="#dddddd",
                                     dropdown_font=("Arial", self.fuente_general),
                                     dropdown_fg_color="white",
                                     dropdown_text_color="black")
        combo_programa.set("Programa")
        combo_programa.grid(row=2, column=1, padx=15, pady=10)
        self.entries["Programa"] = combo_programa

        # Boton registrar
        boton = CTkButton(contenedor, text="REGISTRAR",
                          font=("Arial", self.fuente_general + 2, "bold"),
                          fg_color="#f6a623", text_color="black",
                          hover_color="#d38e14",
                          height=50, corner_radius=6, width=300)
        boton.pack(pady=(30, 0))

    def obtener_turno_actual(self):
        hora = datetime.now().hour
        if 7 <= hora < 22:
            siguiente = hora + 1
            sufijo = "am" if siguiente < 12 else "pm"
            return f"{hora}–{siguiente}{sufijo}"
        return "Fuera de horario"
