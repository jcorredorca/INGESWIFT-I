''' Vista del panel de horarios para miembros'''
from os import path
from config import IMG_PATH
from PIL import Image
from customtkinter import CTkFrame, CTkOptionMenu, CTkImage, CTkLabel
from ..components.horario_semanal import HorarioSemanal
from ..components.boton_adicional import BotonAdicional
from core import utils
from services import miembros

class Miembros(CTkFrame):
    ''' Esta clase representa el panel de horarios para miembros '''
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color= "#2e1045", corner_radius=1)
        self.repartir_espacio()

        self.crear_menu_opciones()

        self.abrir_imagen()

        self.imagen_convencion_label = CTkLabel(self, text='')
        self.imagen_convencion_label.grid(row=2, column=1, sticky="ns")

        self.actualizar_dimensiones_imagen()

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
        values= ['Escoge tu Plan'] + miembros.recuperar_actividades()
        )
        self.opciones_busqueda.grid(row=1, column=1, sticky = 'n', padx=(5,0) )

    def abrir_imagen(self):
        '''Este metodo crea los objetos imagen para mostrarlo en un label'''

        # Rutas a imagen
        ruta_convencion_img = path.join(IMG_PATH, "Convencion.png")

        self.imagen_convencion = Image.open(ruta_convencion_img)


    def actualizar_dimensiones_imagen(self):
        '''Ajusta automáticamente las dimensiones de la imagen al frame'''

        factor = 1/6
        frame_height = self.master.winfo_screenheight()*factor

        new_width = frame_height* 407/277

        imagen_inicio_tk = CTkImage(light_image=self.imagen_convencion,
                                    size=(new_width,frame_height))

        self.imagen_convencion_label.configure(image= imagen_inicio_tk)

        self.master.update()
