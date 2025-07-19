'''Este modulo se encarga del frame de creacion de horarios'''
from tkinter import messagebox
from services import administrador
from .crear_horario  import CrearHorario


class CrearHorarioMasivo(CrearHorario):
    '''Clase que representa una ventana emergente para crear varias sesiones'''

    def __init__(self, master, celdas):
        super().__init__(master)
        self.celdas = celdas

    def crear_horario(self):
        '''Este metodo recupera la información 
        del formulario y crea el horario'''

        publico = self.publico.get()
        ubicacion = self.ubicacion.get()

        if all([publico == 'PUBLICO', ubicacion == 'UBICACION']):
            messagebox.showerror('Error', 'Asegurese de escoger un público y ubicación')
            return

        seleccionados = [funcionario for funcionario, var in self.check_vars if var.get()]
        profesor = self.profesor

        if len(seleccionados) <= 0 or profesor is None:
            messagebox.showerror('Error',
                                 'Asegurese de escoger almenos un funcionario y un profesor')
            return

        celda = self.master.master
        seleccion_actividad = celda.master.master.opciones_busqueda

        for seleccion in self.celdas:
            fecha_hora = seleccion.fecha_hora
            actividad = seleccion_actividad.get()
            id_ubicacion = administrador.recuperar_id_ubicacion(ubicacion)
            id_horario = administrador.crear_horario([publico, fecha_hora, actividad, id_ubicacion])
            administrador.asignar_funcionarios(seleccionados, id_horario, profesor)
            seleccion.actualizar_colores('#c3f7c8', '#e3fae3')
            self.master.destroy()
