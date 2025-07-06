from customtkinter import *
from datetime import datetime


class RegistroExtemporaneo(CTkFrame):
    def __init__(self, master, cupos=5):
        super().__init__(master)
        self.configure(fg_color="#2e1045")
        self.cupos = cupos

        self.fuente_titulo = max(28, int(self.winfo_screenwidth() * 0.02))
        self.fuente_subtitulo = max(18, int(self.winfo_screenwidth() * 0.013))
        self.fuente_general = max(18, int(self.winfo_screenwidth() * 0.012))

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

        boton_logout = CTkButton(encabezado, text="Log Out", font=("Arial", 14),
                                 width=70, height=30,
                                 fg_color="#a246cd", hover_color="#872fc0",
                                 text_color="white", corner_radius=6)
        boton_logout.grid(row=0, column=1, sticky="e")

    def crear_contenido(self):
        contenedor = CTkFrame(self, fg_color="transparent")
        contenedor.pack(expand=True, pady=60)

        titulo = CTkLabel(contenedor, text="MÓDULO DE ASISTENCIA",
                          font=("Arial", self.fuente_titulo, "bold"),
                          text_color="white")
        titulo.pack(pady=(0, 10))

        subtitulo = CTkLabel(contenedor, text=">>REGISTRO EXTEMPORÁNEO<<",
                             font=("Arial", self.fuente_subtitulo, "bold"),
                             text_color="white")
        subtitulo.pack(pady=(0, 40))

        # CAMPO USUARIO con el ícono dentro del placeholder
        entry_usuario = CTkEntry(contenedor,
                                 placeholder_text="👤 Usuario",
                                 fg_color="white", height=50,
                                 font=("Arial", self.fuente_general),
                                 text_color="black")
        entry_usuario.pack(pady=(0, 40), ipadx=20, ipady=2)

        # CUPOS
        cupos_frame = CTkFrame(contenedor, fg_color="transparent")
        cupos_frame.pack(pady=(0, 50))

        label_cupos = CTkLabel(cupos_frame, text="Cupos disponibles:",
                               text_color="white", font=("Arial", self.fuente_general + 2, "bold"))
        label_cupos.grid(row=0, column=0, padx=(0, 10))

        numero_cupos = CTkLabel(cupos_frame, text=str(self.cupos),
                                text_color="black", fg_color="white",
                                corner_radius=6, width=45, height=35,
                                font=("Arial", self.fuente_general + 2, "bold"))
        numero_cupos.grid(row=0, column=1)

        # BOTÓN
        boton = CTkButton(contenedor, text="REGISTRAR EXTEMPORÁNEO",
                          font=("Arial", self.fuente_general + 2, "bold"),
                          fg_color="#f6a623", text_color="black",
                          hover_color="#d38e14",
                          height=50, corner_radius=6)
        boton.pack(pady=(10, 0))

    def obtener_turno_actual(self):
        hora = datetime.now().hour
        if 7 <= hora < 22:
            siguiente = hora + 1
            sufijo = "am" if siguiente < 12 else "pm"
            return f"{hora}–{siguiente}{sufijo}"
        return "Fuera de horario"

