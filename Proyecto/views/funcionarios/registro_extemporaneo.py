'''Modulo para el registro de asistencia extemporaneo'''
from datetime import datetime
from tkinter import messagebox

from core import utils
from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel
from services.funcionario import recuperar_cupos, registro_extemporaneo


class RegistroExtemporaneo(CTkFrame):
    """Clase que representa el módulo de registro extemporáneo para funcionarios"""
    def __init__(self, master, sesion):
        super().__init__(master)
        self.configure(fg_color="#2e1045")
        self.master = master
        self.sesion = sesion
        self.cupos = 0

        self.fuente_titulo = max(28, int(self.winfo_screenwidth() * 0.02))
        self.fuente_subtitulo = max(18, int(self.winfo_screenwidth() * 0.013))
        self.fuente_general = max(18, int(self.winfo_screenwidth() * 0.012))

        self.crear_encabezado()
        self.crear_contenido()
        self.verificar_cupos()

    def crear_encabezado(self):
        """Crea el encabezado con el turno actual"""
        encabezado = CTkFrame(self, fg_color="transparent")
        encabezado.pack(fill="x", padx=20, pady=(10, 0), anchor="ne")

        encabezado.grid_columnconfigure(0, weight=1)
        encabezado.grid_columnconfigure(1, weight=0)

        turno = self.obtener_turno_actual()
        turno_label = CTkLabel(encabezado, text=f"TURNO: {turno}",
                              text_color="white", font=("Arial", 16, "bold"))
        turno_label.grid(row=0, column=0, sticky="e", padx=(0, 10))

    def crear_contenido(self):
        """Crea el contenido principal de la ventana"""
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
        self.entry_usuario = CTkEntry(contenedor,
                                     placeholder_text="👤 Usuario",
                                     fg_color="white", height=50,
                                     font=("Arial", self.fuente_general),
                                     text_color="black")
        self.entry_usuario.pack(pady=(0, 40), ipadx=20, ipady=2)

        # CUPOS
        self.cupos_frame = CTkFrame(contenedor, fg_color="transparent")
        self.cupos_frame.pack(pady=(0, 30))

        label_cupos = CTkLabel(self.cupos_frame, text="Cupos disponibles:",
                              text_color="white", font=("Arial", self.fuente_general + 2, "bold"))
        label_cupos.grid(row=0, column=0, padx=(0, 10))

        self.numero_cupos = CTkLabel(self.cupos_frame, text=str(self.cupos),
                                    text_color="black", fg_color="white",
                                    corner_radius=6, width=45, height=35,
                                    font=("Arial", self.fuente_general + 2, "bold"))
        self.numero_cupos.grid(row=0, column=1)

        # Área de mensajes
        self.mensaje_label = CTkLabel(contenedor, text="",
                                     font=("Arial", self.fuente_general - 2),
                                     text_color="white")
        self.mensaje_label.pack(pady=10)

        # BOTÓN
        self.boton = CTkButton(contenedor, text="REGISTRAR EXTEMPORÁNEO",
                              font=("Arial", self.fuente_general + 2, "bold"),
                              fg_color="#f6a623", text_color="black",
                              hover_color="#d38e14",
                              height=50, corner_radius=6,
                              command=self.registrar_extemporaneo)
        self.boton.pack(pady=(10, 0))


    def verificar_cupos(self):
        """Verifica si aún hay cupos disponibles"""
        cupos_actuales = recuperar_cupos(self.sesion)
        if cupos_actuales == 'SIN RESERVA':
            cupos_actuales = 0

        # Actualizar el display de cupos
        self.numero_cupos.configure(text=str(cupos_actuales))
        self.cupos = cupos_actuales

    def registrar_extemporaneo(self):
        """Registra un usuario de forma extemporánea"""
        usuario = self.entry_usuario.get()
        self.revisar_pantalla()

        if not usuario:
            self.mostrar_mensaje("Por favor, ingrese un usuario", "error")
            return

        # Usar la función de rol_funci para registrar extemporáneo
        exito, mensaje = registro_extemporaneo(usuario, self.sesion)

        if exito:
            self.mostrar_mensaje(mensaje, "exito")
            # Limpiar campo después de registro exitoso
            self.entry_usuario.delete(0, 'end')

            # Actualizar cupos inmediatamente
            self.verificar_cupos()

        else:
            self.mostrar_mensaje(mensaje, "error")

    def mostrar_mensaje(self, mensaje, tipo="info"):
        """Muestra un mensaje en la interfaz"""
        if tipo == "error":
            color="#ff6b6b"
        elif tipo == "exito":
            color="#51cf66"
        else:
            color='white'

        self.mensaje_label.configure(text=mensaje, text_color=color)

        # Limpiar mensaje después de 5 segundos
        self.after(5000, lambda: self.mensaje_label.configure(text=""))

    def obtener_turno_actual(self):
        """Obtiene el turno actual basado en la hora"""
        hora = datetime.now().hour
        if 7 <= hora < 22:
            siguiente = hora + 1
            sufijo = "am" if siguiente < 12 else "pm"
            return f"{hora}-{siguiente}{sufijo}"
        return "Fuera de horario"

    def revisar_pantalla(self):
        '''Funcón para revisar si la pantalla de registro debe cambiar'''
        self.verificar_cupos()

        if self.cupos <= 0:
            messagebox.showwarning('Cupos agotados',
                                   'Los cupos extemporaneos ya se agotaron')
            utils.redirigir_pantalla_funcionario(self.master)
