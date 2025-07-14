'''Este modulo se encarga del frame de reservas '''

from customtkinter import CTkButton, CTkFrame, CTkLabel
from services import miembros, general

class Reservar(CTkFrame):
    '''Clase que representa una ventana emergente para reservas'''

    def __init__(self, master):
        super().__init__(master)
        self.master  = master
        self.usuario = self.master.master.master.master.master.usuario
        self.fuente = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.018)), 'bold')
        self.celda = self.master.master.master
        seleccion_actividad = self.celda.master.master.opciones_busqueda

        fecha_hora = self.celda.fecha_hora
        actividad = seleccion_actividad.get()
        self.id_sesion = general.hay_sesiones(actividad, fecha_hora)
        self.configure(fg_color="#3d1c57")

        self.repartir_espacio()


        self.contenido = CTkButton(self,
                  text = 'RESERVAR',
                  font= self.fuente,
                  command=self.reservar,
                  fg_color= "#F6A623",
                  text_color="#3d1c57",
                  hover_color="#FEB745")
        self.contenido.grid(row=1,column=1)

    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

    def reservar(self):
        '''Crea la reserva'''

        codigo_reserva = miembros.generar_codigo_reserva(self.usuario, self.id_sesion)
        miembros.crear_reserva(codigo=codigo_reserva, sesion=self.id_sesion, usuario=self.usuario)
        self.contenido.destroy()
        self.contenido = CTkLabel(self,
                  text = f'Tu código de confirmación es: {codigo_reserva}',
                  font= self.fuente,
                  fg_color= "#50276f",
                  anchor = 'center',
                  text_color="whitesmoke").grid(row=1,column=1)
        self.celda.actualizar_colores('#c3f7c8','#e3fae3')
