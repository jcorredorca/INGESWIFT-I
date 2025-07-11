from customtkinter import *
from datetime import datetime, timedelta
from core import utils, rol_funci
from ..components import boton_adicional

class ModuloAsistencia(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#2e1045")
        self.master = master
        
        # Variables para el control de tiempo
        self.sesion_inicio = datetime.now()
        self.check_job = None
        
        self.tamanio_fuente_titulo = max(28, int(self.winfo_screenwidth() * 0.02))
        self.tamanio_fuente_campo = max(18, int(self.winfo_screenwidth() * 0.01))
        self.tamanio_fuente_boton = max(22, int(self.winfo_screenwidth() * 0.012))

        self.crear_encabezado_derecho()
        self.crear_contenido()
        
        # Iniciar el monitoreo de tiempo
        self.iniciar_monitoreo_sesion()

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

    def iniciar_monitoreo_sesion(self):
        """Inicia el monitoreo de la sesión actual"""
        print(f"Iniciando monitoreo de sesión a las {self.sesion_inicio}")
        self.verificar_estado_sesion()

    def verificar_estado_sesion(self):
        """Verifica el estado de la sesión y hace transiciones si es necesario"""
        try:
            # Verificar si han pasado 10 minutos desde el inicio
            tiempo_transcurrido = datetime.now() - self.sesion_inicio
            minutos_transcurridos = tiempo_transcurrido.total_seconds() / 60
            
            print(f"Minutos transcurridos: {minutos_transcurridos:.1f}")
            
            if minutos_transcurridos >= 10:
                # Verificar si todos los cupos están ocupados
                if rol_funci.verificar_cupos_llenos():
                    print("Cupos llenos - Cambiando a sesión cerrada")
                    self.cambiar_a_sesion_cerrada()
                    return
                
                # Si aún hay cupos disponibles, cambiar a registro extemporáneo
                elif rol_funci.verificar_cupos_disponibles():
                    print("Cupos disponibles - Cambiando a registro extemporáneo")
                    self.cambiar_a_registro_extemporaneo()
                    return
                else:
                    # Si no hay cupos disponibles, ir a sesión cerrada
                    print("No hay cupos disponibles - Cambiando a sesión cerrada")
                    self.cambiar_a_sesion_cerrada()
                    return
            
            # Programar la próxima verificación en 30 segundos
            self.check_job = self.after(30000, self.verificar_estado_sesion)
            
        except Exception as e:
            print(f"Error en verificar_estado_sesion: {e}")
            # Programar nueva verificación en caso de error
            self.check_job = self.after(30000, self.verificar_estado_sesion)

    def cambiar_a_registro_extemporaneo(self):
        """Cambia a la ventana de registro extemporáneo"""
        try:
            # Cancelar verificaciones pendientes
            if self.check_job:
                self.after_cancel(self.check_job)
            
            # Usar la función de rol_funci para cambiar de pantalla
            rol_funci.redirigir_pantalla_registro_extemporaneo(self.master)
            
        except Exception as e:
            print(f"Error cambiando a registro extemporáneo: {e}")

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

    def confirmar_asistencia(self):
        """Confirma la asistencia del usuario"""
        usuario = self.entrada_usuario.get().strip()
        codigo = self.entrada_codigo.get().strip()
        
        if not usuario or not codigo:
            self.mostrar_mensaje("Por favor, complete todos los campos", "error")
            return
        
        # Usar la función de rol_funci para registrar asistencia
        exito, mensaje = rol_funci.registrar_asistencia(usuario, codigo)
        
        if exito:
            self.mostrar_mensaje(mensaje, "exito")
            # Limpiar campos después de registro exitoso
            self.entrada_usuario.delete(0, 'end')
            self.entrada_codigo.delete(0, 'end')
            
            # Verificar si después de esta asistencia se llenaron todos los cupos
            if rol_funci.verificar_cupos_llenos():
                # Esperar un poco para que el usuario vea el mensaje y luego cambiar
                self.after(2000, self.cambiar_a_sesion_cerrada)
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
        if 7 <= hora < 22:
            siguiente = hora + 1
            sufijo_inicio = "am" if hora < 12 else "pm"
            sufijo_fin = "am" if siguiente < 12 else "pm"
            return f"{hora}–{siguiente}{sufijo_fin}"
        return "Fuera de horario"

    def destroy(self):
        """Limpia recursos al destruir el widget"""
        if self.check_job:
            self.after_cancel(self.check_job)
        super().destroy()