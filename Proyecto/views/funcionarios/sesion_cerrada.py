'''Modulo para la sesion cerrada'''
from datetime import datetime

from customtkinter import CTkFrame, CTkLabel, CTkButton
from core import utils

class SesionCerrada(CTkFrame):
    """Clase que representa la ventana de sesión cerrada para funcionarios"""
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#2e1045")

        self.tamanio_fuente_titulo = max(28, int(self.winfo_screenwidth() * 0.02))
        self.tamanio_fuente_texto = max(18, int(self.winfo_screenwidth() * 0.012))

        self.crear_encabezado_derecho()
        self.crear_contenido()

    def crear_encabezado_derecho(self):
        '''Encabezado con TURNO y boton Log Out'''
        mini_encabezado = CTkFrame(self, fg_color="transparent")
        mini_encabezado.pack(fill="x", padx=20, pady=(10, 0), anchor="ne")

        mini_encabezado.grid_columnconfigure(0, weight=1)
        mini_encabezado.grid_columnconfigure(1, weight=0)

        turno_actual = self.obtener_turno_actual()
        turno_label = CTkLabel(mini_encabezado, text=f"TURNO: {turno_actual}",
                               text_color="white", font=("Arial", 16, "bold"))
        turno_label.grid(row=0, column=0, sticky="e", padx=(0, 10))

    def crear_contenido(self):
        '''Contenido central de advertencia'''
        contenido = CTkFrame(self, fg_color="transparent")
        contenido.pack(expand=True, pady=40)

        # TITULO
        titulo = CTkLabel(contenido, text="MÓDULO DE ASISTENCIA",
                          font=("Arial", self.tamanio_fuente_titulo, "bold"),
                          text_color="white")
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 50), sticky="n")

        # Texto de alerta
        lado_derecho = CTkFrame(contenido, fg_color="transparent")
        lado_derecho.grid(row=1, column=1, padx=60, sticky="w")

        label_alerta = CTkLabel(lado_derecho, text="SESIÓN CERRADA",
                                text_color="#f6a623",
                                font=("Arial", self.tamanio_fuente_texto + 4, "bold"))
        label_alerta.pack(anchor="w", pady=(20, 20))

        # Separamos las líneas para controlar el espacio
        linea = CTkLabel(lado_derecho, text="No se pueden registrar\nmás entradas", anchor='center',
                          text_color="gainsboro", font=("Arial", self.tamanio_fuente_texto, "bold"))

        linea.pack(anchor="w", pady=(0, 30))

        boton_salir = CTkButton(lado_derecho, text="SALIR",
                                font=("Arial", self.tamanio_fuente_texto, "bold"),
                                fg_color="#f6a623", text_color="black",
                                hover_color="#d38e14",
                                width=100, height=35, anchor='center',
                                command=lambda: utils.redirigir_pantalla_funcionario(self.master))
        boton_salir.pack()

    def obtener_turno_actual(self):
        '''Devuelve el turno actual como string (7-8am, etc)'''
        hora = datetime.now().hour
        if 7 <= hora < 22:
            siguiente = hora + 1
            sufijo_fin = "am" if siguiente < 12 else "pm"
            return f"{hora}-{siguiente}{sufijo_fin}"
        return "Fuera de horario"
