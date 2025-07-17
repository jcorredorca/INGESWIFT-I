from datetime import datetime

from core import rol_funci, utils
from customtkinter import *

from ..components import boton_adicional


class RegistroExtemporaneo(CTkFrame):
    """Clase que representa el módulo de registro extemporáneo para funcionarios"""
    def __init__(self, master, cupos=5):
        super().__init__(master)
        self.configure(fg_color="#2e1045")
        self.master = master
        self.cupos = cupos

        # Variables para el control de tiempo
        self.check_job = None

        self.fuente_titulo = max(28, int(self.winfo_screenwidth() * 0.02))
        self.fuente_subtitulo = max(18, int(self.winfo_screenwidth() * 0.013))
        self.fuente_general = max(18, int(self.winfo_screenwidth() * 0.012))

        self.crear_encabezado()
        self.crear_contenido()

        # Iniciar monitoreo de cupos
        self.iniciar_monitoreo_cupos()

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

    def iniciar_monitoreo_cupos(self):
        """Inicia el monitoreo de cupos disponibles"""
        self.verificar_cupos()

    def verificar_cupos(self):
        """Verifica si aún hay cupos disponibles"""
        try:
            cupos_actuales = rol_funci.obtener_cupos_disponibles_sesion_actual()

            # Actualizar el display de cupos
            self.numero_cupos.configure(text=str(cupos_actuales))
            self.cupos = cupos_actuales

            # Si no hay cupos disponibles, cambiar a sesión cerrada
            if cupos_actuales <= 0:
                self.cambiar_a_sesion_cerrada()
                return

            # Programar la próxima verificación en 15 segundos
            self.check_job = self.after(15000, self.verificar_cupos)

        except Exception as e:
            print(f"Error verificando cupos: {e}")
            # Programar nueva verificación en caso de error
            self.check_job = self.after(15000, self.verificar_cupos)

    def registrar_extemporaneo(self):
        """Registra un usuario de forma extemporánea"""
        usuario = self.entry_usuario.get().strip()

        if not usuario:
            self.mostrar_mensaje("Por favor, ingrese un usuario", "error")
            return

        # Usar la función de rol_funci para registrar extemporáneo
        exito, mensaje = rol_funci.registrar_extemporaneo(usuario)

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
            self.mensaje_label.configure(text=mensaje, text_color="#ff6b6b")
        elif tipo == "exito":
            self.mensaje_label.configure(text=mensaje, text_color="#51cf66")
        else:
            self.mensaje_label.configure(text=mensaje, text_color="white")

        # Limpiar mensaje después de 5 segundos
        self.after(5000, lambda: self.mensaje_label.configure(text=""))

    def cambiar_a_sesion_cerrada(self):
        """Cambia a la ventana de sesión cerrada"""
        try:
            # Cancelar verificaciones pendientes
            if self.check_job:
                self.after_cancel(self.check_job)

            # Usar la función de rol_funci para cambiar de pantalla
            rol_funci.redirigir_pantalla_sesion_cerrada(self.master)

        except Exception as e:
            print(f"Error cambiando a sesión cerrada: {e}")

    def obtener_turno_actual(self):
        """Obtiene el turno actual basado en la hora"""
        hora = datetime.now().hour
        if 7 <= hora < 22:
            siguiente = hora + 1
            sufijo = "am" if siguiente < 12 else "pm"
            return f"{hora}–{siguiente}{sufijo}"
        return "Fuera de horario"

    def destroy(self):
        """Limpia recursos al destruir el widget"""
        if self.check_job:
            self.after_cancel(self.check_job)
        super().destroy()
