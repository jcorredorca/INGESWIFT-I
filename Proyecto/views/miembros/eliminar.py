'''Este modulo se encarga del frame de reservas '''
from tkinter import messagebox
from customtkinter import CTkButton, CTkFrame
from services import miembros, general

class Eliminar(CTkFrame):
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
                  text = 'ELIMINAR RESERVA',
                  font= self.fuente,
                  command=self.eliminar,
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

    def eliminar(self):
        '''Elimina la reserva'''

        codigo_reserva = miembros.buscar_reserva(self.usuario, self.id_sesion)
        miembros.eliminar_reserva(codigo=codigo_reserva)
        self.master.destroy()
        messagebox.showinfo('Eliminado', 'La reserva se ha eliminado correctamente')
        if general.hay_cupos_disponibles(self.id_sesion):
            self.celda.actualizar_colores('#fff7a1','#fcfcca')
        else:
            self.celda.actualizar_colores('#ffd9d9', '#fff0f0')
