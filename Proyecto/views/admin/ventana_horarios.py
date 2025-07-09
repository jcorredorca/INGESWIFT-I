''' Vista del panel de horarios para Administradores'''

from datetime import datetime, timedelta
from customtkinter import CTkFrame, CTkOptionMenu, CTkLabel
from ..components.horario_semanal import HorarioSemanal
from services.general import recuperar_actividades

class VentanaHorarios(CTkFrame):
    ''' Esta clase representa el panel de creacion y edicion de horarios para miembros '''
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color= "#2e1045", corner_radius=1)
        self.repartir_espacio()

        self.crear_menu_opciones()

        self.indicador_semana()

        self.horario = HorarioSemanal(self)
        self.horario.grid(row=1, column=3, sticky='e', rowspan=2)


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

        self.opciones_busqueda = CTkOptionMenu(self, font=fuente_seleccion,
        dropdown_font=fuente_opciones, fg_color= "#F6A623", text_color="#2e1045",
        button_color="", button_hover_color="", corner_radius=0,
        dropdown_fg_color="#3d1c57", dropdown_text_color= "#f0f0f0",
        dropdown_hover_color= "#F6A623", width= self.winfo_screenwidth() * 0.2,
        anchor= 'center',
        values= ['Escoge tu Plan'] + recuperar_actividades()
        )
        self.opciones_busqueda.grid(row=1, column=1, sticky = 'n', padx=(5,0) )

    def indicador_semana(self):
        '''Este metodo crea el indicador de la semana a editar'''
        fuente = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.02)), 'bold')
        self.semana = self.rango_semana_actual()
        texto = 'Semana del '+ str(self.semana[0]) + ' al '+ str(self.semana[1])
        self.label_semana = CTkLabel(self, text=texto, font=fuente)
        self.label_semana.grid(row=0, column=1, columnspan=3)

    def rango_semana_actual(self):
        '''Crea el rango de una determinada semana'''
        hoy = datetime.now()

        # Lunes = 0, Domingo = 6
        lunes = hoy - timedelta(days=hoy.weekday()) + timedelta(days=7)
        sabado = lunes + timedelta(days=5)

        return lunes.date(), sabado.date()
    
    def crear_ventana()
