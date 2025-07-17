''' Vista del panel de horarios para miembros'''
from os import path
from datetime import datetime, timedelta
from tkinter import messagebox
from config import IMG_PATH
from PIL import Image
from customtkinter import CTkFrame, CTkOptionMenu, CTkImage, CTkLabel
from services import general, miembros
from ..components.horario_semanal import HorarioSemanal
from .state_horario import StateHorarioMiembros, Reservar, Eliminar


class Miembros(CTkFrame):
    ''' Esta clase representa el panel de horarios para miembros '''
    def __init__(self, master):
        super().__init__(master)

        self.usuario = self.master.usuario
        self.estado = None

        self.configure(fg_color= "#2e1045", corner_radius=1)
        self.repartir_espacio()

        self.crear_menu_opciones()

        self.abrir_imagen()

        self.imagen_convencion_label = CTkLabel(self, text='')
        self.imagen_convencion_label.grid(row=4, column=1, sticky="n")

        self.actualizar_dimensiones_imagen()

        self.indicador_semana()

        self.indicador_estado()

        self.horario = HorarioSemanal(self, 'MIEMBRO')
        self.horario.grid(row=1, column=3, sticky='e', rowspan=7)
        self.habilitar_celdas()
        self.revisar_y_actualizar()


    def habilitar_celdas(self):
        '''Habilita las celdas en las que se puede hacer reserva'''

        for columna in self.horario.celdas:
            for celda in columna:

                plan = self.opciones_busqueda.get()
                fecha_hora = celda.fecha_hora
                id_sesion = general.hay_sesiones(plan, fecha_hora)

                if id_sesion is False or fecha_hora < datetime.now():
                    celda.unbind('<Button-1>')
                    celda.configure(text='')
                    fg_color= "#f0f0f0"
                    hover_color ="#A8A4A4"
                    celda.actualizar_colores(fg_color, hover_color)
                else:
                    estado_activo = miembros.recuperar_estado(self.usuario) == 'ACTIVO'
                    publico_adecuado = miembros.rol_sesion(self.usuario, id_sesion)

                    if estado_activo and miembros.sesion_disponible(id_sesion):
                        celda.unbind('<Button-1>')
                        funcion = self.crear_ventana if publico_adecuado else self.advertencia
                        celda.bind('<Button-1>', funcion)

                        celda.update()

                    celda.configure(text=miembros.recuperar_cupos(id_sesion))
                    fg_color, hover_color = self.colores_correspondientes(id_sesion)
                    celda.actualizar_colores(fg_color, hover_color)

    def revisar_y_actualizar(self):
        '''Este metodo actualiza la ventana de horario cada 30s'''
        self.habilitar_celdas()
        self.after(5000,self.revisar_y_actualizar)

    def advertencia(self, event):
        '''Advierte que no pertenece al publico objetivo de la sesion'''
        if event:
            messagebox.showinfo('','No pertenece al publico objetivo de la sesión')
    def colores_correspondientes(self, id_sesion):
        '''Este metodo devuelve los colores correspondientes\
            dependiendo de si hay o no una reserva a el momento'''
        usuario = self.usuario
        if miembros.buscar_reserva(usuario, id_sesion):
            return '#c3f7c8', '#e3fae3'
        if general.hay_cupos_disponibles(id_sesion):
            return '#fff7a1', '#fcfcca'
        return '#ffd9d9', '#fff0f0'

    def repartir_espacio(self):
        '''Reparte el espacio '''

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=0)
        self.grid_columnconfigure(6, weight=1)
        self.grid_columnconfigure(7, weight=0)
        self.grid_columnconfigure(8, weight=1)

    def crear_menu_opciones(self):
        '''Este metodo crea el menu de opciones para escoger un plan'''

        fuente_seleccion = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.02)), 'bold')
        fuente_opciones = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.012)), 'bold')

        self.opciones_busqueda = CTkOptionMenu(self, font=fuente_seleccion,
            dropdown_font=fuente_opciones, fg_color= "#F6A623", text_color="#2e1045",
            button_color="", button_hover_color="", corner_radius=0,
            dropdown_fg_color="#3d1c57", dropdown_text_color= "#f0f0f0",
            dropdown_hover_color= "#F6A623", width= self.winfo_screenwidth() * 0.2,
            anchor= 'center', command= self.actualizar_horario,
            values= ['Escoge tu Plan'] + general.recuperar_actividades())

        self.opciones_busqueda.grid(row=1, column=1, sticky = 'n', padx=(5,0) )

    def actualizar_horario(self, actividad=None):
        '''Actualiza la ventana de horarios para el nuevo plan'''
        self.horario.actualizar_celdas_miembro(actividad)
        self.habilitar_celdas()

    def abrir_imagen(self):
        '''Este metodo crea los objetos imagen para mostrarlo en un label'''

        # Rutas a imagen
        ruta_convencion_img = path.join(IMG_PATH, "Convencion.png")

        self.imagen_convencion = Image.open(ruta_convencion_img)

    def indicador_semana(self):
        '''Este metodo crea el indicador de la semana a editar'''
        fuente = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.02)), 'bold')
        semana = self.rango_semana_actual()
        texto = 'Semana del '+ str(semana[0]) + '\nal '+ str(semana[1])
        self.label_semana = CTkLabel(self, text=texto, font=fuente, text_color='whitesmoke')
        self.label_semana.grid(row=3, column=1)

    def rango_semana_actual(self):
        '''Crea el rango de una determinada semana'''
        hoy = datetime.now()

        # Lunes = 0, Domingo = 6
        lunes = hoy - timedelta(days=hoy.weekday())
        sabado = lunes + timedelta(days=5)

        return lunes.date(), sabado.date()

    def indicador_estado(self):
        '''Este metodo crea el indicador del estado del miembro'''
        fuente = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.01)), 'bold')
        estado = miembros.recuperar_estado(self.usuario)
        texto = f'Actualmente estas: {estado}'
        color = '#ffd9d9' if estado == 'INACTIVO' else '#e3fae3'
        self.label_estado = CTkLabel(self, text=texto, font=fuente, text_color=color)
        self.label_estado.grid(row=5, column=1)

    def actualizar_dimensiones_imagen(self):
        '''Ajusta automáticamente las dimensiones de la imagen al frame'''

        factor = 1/6
        frame_height = self.master.winfo_screenheight()*factor

        new_width = frame_height* 407/277

        imagen_inicio_tk = CTkImage(light_image=self.imagen_convencion,
                                    size=(new_width,frame_height))

        self.imagen_convencion_label.configure(image= imagen_inicio_tk)

        self.master.update()

    def crear_ventana(self, event):
        '''Esta funcion crea la ventana emergente luego de un click'''
        if event:
            celda = event.widget
            plan = self.opciones_busqueda.get()
            fecha_hora = celda.master.fecha_hora
            id_horario = general.hay_sesiones(plan, fecha_hora)


            if miembros.buscar_reserva(self.usuario, id_horario):

                if not self.fuera_de_intervalo(fecha_hora):
                    ventana = StateHorarioMiembros(celda, Eliminar())
                else:
                    messagebox.showinfo('Ups','No es posible cancelar tu reserva.' \
                    '\nTienes hasta 15 minutos antes de la sesion para cancelar una')
                    return

            else:
                ventana = StateHorarioMiembros(celda, Reservar())
            ventana.renderizar_contenido()

    def fuera_de_intervalo(self, fecha_hora:datetime) -> bool:
        """Devuelve False si estamos entre el minuto 45 y 
        el siguiente cambio de hora (inclusive),
        y True en cualquier otro minuto."""
        ahora = datetime.now()
        minuto = ahora.minute
        hora = ahora.hour

        return (45 <= minuto <= 59) and (hora == fecha_hora.hour-1)
