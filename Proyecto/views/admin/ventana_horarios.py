''' Vista del panel de horarios para Administradores'''

from datetime import datetime, timedelta
from tkinter import Event, messagebox
from customtkinter import CTkFrame, CTkOptionMenu, CTkLabel, CTkButton
from services.general import recuperar_actividades
from services import general
from views.components.horario_semanal import HorarioSemanal
from .state_horario import StateHorario, Creacion, EdicionEliminacion, CreacionMasiva


class VentanaHorarios(CTkFrame):
    ''' Esta clase representa el panel de creacion y edicion de horarios para miembros '''
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color= "#2e1045", corner_radius=1)

        self.repartir_espacio()

        self.frame_izq = CTkFrame(self, fg_color="#2e1045")
        self.frame_izq.rowconfigure(1, weight=1)
        self.frame_izq.grid(row=1, column=1, sticky = 'ns')
        self.crear_menu_opciones()

        self.indicador_semana()

        self.botones_navegacion()

        self.crear_horario()

        self.ctrl_pressed = False
        self.celdas_seleccionadas = set()
        # Eventos globales
        self.winfo_toplevel().bind("<Control_L>", self.on_ctrl_press)
        self.winfo_toplevel().bind("<KeyRelease-Control_L>", self.on_ctrl_release)


    def crear_horario(self):
        '''Crea los horarios a desplegar tanto de la semana actual como la siguiente'''
        self.horario_actual= HorarioSemanal(self, 'ADMINISTRADOR', 1)
        self.horario_siguiente = HorarioSemanal(self, 'ADMINISTRADOR', 0)
        self.horario_siguiente.grid(row=1, column=3, sticky='e', rowspan=2)
        self.horario_activo= self.horario_siguiente
        for columna in self.horario_siguiente.celdas:
            for celda in columna:
                celda.bind('<Button-1>', self.crear_ventana)

    def botones_navegacion(self):
        '''Este metodo crea las flechas de navegacion entre horarios'''
        font = ("Segoe UI", 60, 'bold')
        # Botón con flecha a la izquierda
        self.boton_izq = CTkButton(self.frame_izq,
                                   text="<",
                                   font=font,
                                   fg_color="#F6A623",
                                   text_color="#2e1045",
                                   hover_color="#FFB947",
                                   cursor='hand2',
                                   command=self.get_semana_actual)
        self.boton_izq.grid(row=2 , column=0)

        # Botón con flecha a la derecha
        self.boton_der = CTkButton(self.frame_izq,
                                   text=">",
                                   font=font,
                                   fg_color="#F6A623",
                                   text_color="#2e1045",
                                   hover_color="#FFB947",
                                   cursor='hand2',
                                   state='disabled',
                                   command=self.get_semana_siguiente)
        self.boton_der.grid(row=3 , column=0)

    def get_semana_actual(self):
        '''Este metodo despliega el horario de la semana actual'''

        self.horario_actual.grid(row=1, column=3, sticky='e', rowspan=2)
        self.horario_actual.lift()
        self.horario_activo= self.horario_actual
        for columna in self.horario_actual.celdas:
            for celda in columna:
                celda.unbind('<Button-1>')
                celda.bind('<Button-1>', self.crear_ventana)

        self.label_semana_actual.lift()
        self.horario_actual.actualizar_celdas_administrador(self.opciones_busqueda.get())
        self.boton_der.configure(state='normal')
        self.boton_izq.configure(state='disabled')

    def get_semana_siguiente(self):
        '''Este metodo despliega el horario de la semana siguiente'''

        self.horario_siguiente.grid(row=1, column=3, sticky='e', rowspan=2)
        self.horario_siguiente.lift()
        self.horario_activo= self.horario_siguiente
        for columna in self.horario_siguiente.celdas:
            for celda in columna:
                celda.unbind('<Button-1>')
                celda.bind('<Button-1>', self.crear_ventana)

        self.label_semana_siguiente.lift()
        self.horario_siguiente.actualizar_celdas_administrador(self.opciones_busqueda.get())
        self.boton_der.configure(state='disabled')
        self.boton_izq.configure(state='normal')

    def repartir_espacio(self):
        '''Reparte el espacio '''

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=1)

    def crear_menu_opciones(self):
        '''Este metodo crea el menu de opciones para escoger un plan'''

        fuente_seleccion = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.02)), 'bold')
        fuente_opciones = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.012)), 'bold')

        self.opciones_busqueda = CTkOptionMenu(self.frame_izq, font=fuente_seleccion,
        dropdown_font=fuente_opciones, fg_color= "#F6A623", text_color="#2e1045",
        button_color="", button_hover_color="", corner_radius=0,
        dropdown_fg_color="#3d1c57", dropdown_text_color= "#f0f0f0",
        dropdown_hover_color= "#F6A623", width= self.winfo_screenwidth() * 0.2,
        anchor= 'center',
        values= ['PLANES'] + recuperar_actividades(),
        command= self.actualizar_horario
        )
        self.opciones_busqueda.grid(row=0, column=0, sticky = 'n')

    def indicador_semana(self):
        '''Este metodo crea el indicador de la semana a editar'''
        fuente = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.02)), 'bold')
        self.semana_siguiente = self.rango_semana_siguiente()
        self.semana_actual = self.rango_semana_actual()

        texto_actual =\
        'Semana del '+ str(self.semana_actual[0]) + ' \nal '+ str(self.semana_actual[1])

        texto_siguiente =\
        'Semana del '+ str(self.semana_siguiente[0]) + ' \nal '+ str(self.semana_siguiente[1])

        self.label_semana_actual = CTkLabel(self, text=texto_actual,
                                            font=fuente,
                                            text_color='whitesmoke',
                                            fg_color="#3d1c57")
        self.label_semana_actual.grid(row=2, column=1)

        self.label_semana_siguiente = CTkLabel(self,
                                               text=texto_siguiente,
                                               font=fuente,
                                               text_color='whitesmoke',
                                               fg_color="#3d1c57")
        self.label_semana_siguiente.grid(row=2, column=1)

    def rango_semana_siguiente(self):
        '''Crea el rango de una determinada semana'''
        hoy = datetime.now()

        # Lunes = 0, Domingo = 6
        lunes = hoy - timedelta(days=hoy.weekday()) + timedelta(days=7)
        sabado = lunes + timedelta(days=5)

        return lunes.date(), sabado.date()

    def rango_semana_actual(self):
        '''Crea el rango de una determinada semana'''
        hoy = datetime.now()

        # Lunes = 0, Domingo = 6
        lunes = hoy - timedelta(days=hoy.weekday())
        sabado = lunes + timedelta(days=5)

        return lunes.date(), sabado.date()

    def actualizar_horario(self, actividad=None):
        '''Actualiza la ventana de horarios para el nuevo plan'''
        self.horario_activo.actualizar_celdas_administrador(actividad)

    def crear_ventana(self, event:Event):
        '''Esta funcion crea la ventana emergente luego de un click'''
        celda = event.widget
        plan = self.opciones_busqueda.get()
        if not self.revisar_actividad(plan):
            return
        fecha_hora = celda.master.fecha_hora
        id_horario = general.hay_sesiones(plan, fecha_hora)

        if event and not self.ctrl_pressed:
            if id_horario:
                ventana = StateHorario(celda, EdicionEliminacion())
                ventana.renderizar_contenido()
            else:
                ventana = StateHorario(celda, Creacion())
                ventana.renderizar_contenido()
        else:

            if celda.master in self.celdas_seleccionadas:
                self.celdas_seleccionadas.remove(celda.master)
                celda.master.configure(fg_color="lightgray")
                celda.master.fg_color = "#f0f0f0"

            else:
                if celda.master.fg_color != '#c3f7c8':
                    self.celdas_seleccionadas.add(celda.master)
                    celda.master.configure(fg_color="lightblue")
                    celda.master.fg_color = "lightblue"


    def revisar_actividad(self, actividad):
        '''Revisa que haya una actividad para renderizar la ventana de creacion'''
        if actividad == 'PLANES':
            messagebox.showwarning('Plan','Escoja alguno de los planes para poder crear un horario')
            return False
        return True

    def on_ctrl_press(self, event):
        '''Verifica si el control esta siendo presionado'''
        if event:
            self.ctrl_pressed = True

    def on_ctrl_release(self, event):
        '''Llama a la ventana emergente cuando se suelta el control'''
        if event:
            self.ctrl_pressed = False
            if self.celdas_seleccionadas:
                ventana = StateHorario(
                                      next(iter(self.celdas_seleccionadas)),
                                      CreacionMasiva(),
                                      self.celdas_seleccionadas
                                      )
                ventana.renderizar_contenido()
