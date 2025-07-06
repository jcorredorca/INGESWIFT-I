from customtkinter import *
from datetime import datetime

class ModuloAsistencia(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#2e1045")

        self.tamanio_fuente_titulo = max(28, int(self.winfo_screenwidth() * 0.02))
        self.tamanio_fuente_campo = max(18, int(self.winfo_screenwidth() * 0.01))
        self.tamanio_fuente_boton = max(22, int(self.winfo_screenwidth() * 0.012))

        self.crear_encabezado_derecho()
        self.crear_contenido()

    def crear_encabezado_derecho(self):
        '''Encabezado con TURNO y boton Log Out'''
        mini_encabezado = CTkFrame(self, fg_color="transparent")
        mini_encabezado.pack(fill="x", padx=20, pady=(10, 0), anchor="ne")

        mini_encabezado.grid_columnconfigure(0, weight=1)
        mini_encabezado.grid_columnconfigure(1, weight=0)

        # Texto turno
        turno_actual = self.obtener_turno_actual()
        turno_label = CTkLabel(mini_encabezado, text=f"TURNO: {turno_actual}",
                               text_color="white", font=("Arial", 16, "bold"))
        turno_label.grid(row=0, column=0, sticky="e", padx=(0, 10))

        # Botón Log Out
        boton_logout = CTkButton(mini_encabezado, text="Log Out", font=("Arial", 14),
                                 width=70, height=30,
                                 fg_color="#a246cd", hover_color="#872fc0",
                                 text_color="white", corner_radius=6)
        boton_logout.grid(row=0, column=1, sticky="e")

    def crear_contenido(self):
        '''Formulario central'''
        contenido = CTkFrame(self, fg_color="transparent")
        contenido.pack(expand=True)

        # Título
        titulo = CTkLabel(contenido, text="MÓDULO DE ASISTENCIA",
                          font=("Arial", self.tamanio_fuente_titulo, "bold"),
                          text_color="white")
        titulo.pack(pady=(0, 40))

        # Entrada Usuario
        entrada_usuario = CTkEntry(contenido, placeholder_text="👤 Usuario",
                                   font=("Arial", self.tamanio_fuente_campo),
                                   fg_color="white", text_color="#7a519d",
                                   height=50, width=int(self.winfo_screenwidth() * 0.35))
        entrada_usuario.pack(pady=10)

        # Entrada Código de reserva
        entrada_codigo = CTkEntry(contenido, placeholder_text="🔑 Código de reserva",
                                  font=("Arial", self.tamanio_fuente_campo),
                                  fg_color="white", text_color="#7a519d",
                                  height=50, width=int(self.winfo_screenwidth() * 0.35))
        entrada_codigo.pack(pady=10)

        # Botón Confirmar
        boton_confirmar = CTkButton(contenido, text="CONFIRMAR",
                                    font=("Arial", self.tamanio_fuente_boton, "bold"),
                                    fg_color="#f6a623", text_color="black",
                                    hover_color="#d38e14",
                                    height=50, width=int(self.winfo_screenwidth() * 0.35))
        boton_confirmar.pack(pady=30)

    def obtener_turno_actual(self):
        """Devuelve el turno actual como string"""
        hora = datetime.now().hour
        if 7 <= hora < 22:
            siguiente = hora + 1
            sufijo_inicio = "am" if hora < 12 else "pm"
            sufijo_fin = "am" if siguiente < 12 else "pm"
            return f"{hora}–{siguiente}{sufijo_fin}"
        return "Fuera de horario"
