'''Modulo para la ventana de registro de asistencia'''

from datetime import datetime
from tkinter import messagebox
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton
from . import registro_extemporaneo, sesion_cerrada
from services.funcionario import registrar_asistencia, hay_cupos_disponibles

class ModuloAsistencia(CTkFrame):
    """Clase que representa el módulo de asistencia para funcionarios"""
    def __init__(self, master, sesion):
        super().__init__(master)
        self.configure(fg_color="#2e1045")
        self.master = master

        # Variables para el control de tiempo
        self.sesion_inicio = datetime.now()
        self.sesion = sesion

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
        self.entrada_usuario = CTkEntry(contenido, placeholder_text="👤 Usuario",
                                       font=("Arial", self.tamanio_fuente_campo),
                                       fg_color="white", text_color="#7a519d",
                                       height=50, width=int(self.winfo_screenwidth() * 0.35))
        self.entrada_usuario.pack(pady=10)

        # Entrada Código de reserva
        self.entrada_codigo = CTkEntry(contenido, placeholder_text="🔑 Código de reserva",
                                      font=("Arial", self.tamanio_fuente_campo),
                                      fg_color="white", text_color="#7a519d",
                                      height=50, width=int(self.winfo_screenwidth() * 0.35))
        self.entrada_codigo.pack(pady=10)

        # Botón Confirmar
        boton_confirmar = CTkButton(contenido, text="CONFIRMAR",
                                    font=("Arial", self.tamanio_fuente_boton, "bold"),
                                    fg_color="#f6a623", text_color="black",
                                    hover_color="#d38e14",
                                    height=50, width=int(self.winfo_screenwidth() * 0.35),
                                    command=self.confirmar_asistencia)
        boton_confirmar.pack(pady=30)

        # Área de mensajes (opcional)
        self.mensaje_label = CTkLabel(contenido, text="",
                                     font=("Arial", self.tamanio_fuente_campo - 2),
                                     text_color="white")
        self.mensaje_label.pack(pady=10)


    def confirmar_asistencia(self):
        """Confirma la asistencia del usuario"""
        self.revisar_pantalla()
        usuario = self.entrada_usuario.get().strip()
        codigo = self.entrada_codigo.get().strip()

        if not usuario or not codigo:
            self.mostrar_mensaje("Por favor, complete todos los campos", "error")
            return

        # Usar la función de rol_funci para registrar asistencia
        exito, mensaje = registrar_asistencia(usuario, self.sesion, codigo)

        if exito:
            self.mostrar_mensaje(mensaje, 'exito')
            self.entrada_codigo.delete(0, 'end')
            self.entrada_usuario.delete(0, 'end')
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

    def obtener_turno_actual(self):
        """Devuelve el turno actual como string"""
        hora = datetime.now().hour
        if 7 <= hora < 20:
            siguiente = hora + 1
            sufijo_fin = "am" if siguiente < 12 else "pm"
            return f"{hora}-{siguiente}{sufijo_fin}"
        return "Fuera de horario"

    def revisar_pantalla(self):
        '''Funcón para revisar si la pantalla de registro debe cambiar'''
        minutos = datetime.now().minute

        if 10 < minutos < 55:
            messagebox.showwarning('Revisar hora',
                                   'El tiempo para registro de sesión con reserva ha finalizado')

            if hay_cupos_disponibles(self.sesion):
                ventana = registro_extemporaneo.RegistroExtemporaneo(self.master, self.sesion)
            else:
                ventana = sesion_cerrada.SesionCerrada(self.master)

            self.master.contenido.destroy()
            self.master.contenido = ventana
            self.master.contenido.grid(row=1, column=0, sticky="nsew")

