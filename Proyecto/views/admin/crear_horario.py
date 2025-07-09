'''Ventana emergente para el cambio de contraseña'''

from customtkinter import CTkScrollableFrame, CTkButton, CTkCheckBox, CTkOptionMenu

class CrearHorario(CTkScrollableFrame):
    '''Clase que representa una ventana emergente para crear un horario'''

    def __init__(self, master):
        super().__init__(master)
        self.fuente = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.012)), 'bold')

        self.configure(fg_color="#3d1c57")
        self.repartir_espacio()

        self.opciones_optionmenu()

    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)

    def opciones_optionmenu(self):
        '''Crea los dos widget publico y ubicacion 
        de tipo optionMenu'''
        fuente = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.012)), 'bold')
        #---Publico---#
        self.publico = CTkOptionMenu(self, font=fuente,
        dropdown_font=fuente, fg_color= "#F6A623", text_color="#2e1045",
        corner_radius=4, dropdown_fg_color="#3d1c57", dropdown_text_color= "#f0f0f0",
        dropdown_hover_color= "#F6A623", width= self.winfo_screenwidth() * 0.1,
        anchor= 'center',
        values= ['PUBLICO'] )#+ general.recuperar_actividades())
        self.publico.grid(row=0, column=0)

        #---Ubicacion--#
        self.ubicacion = CTkOptionMenu(self, font=fuente,
        dropdown_font=fuente, fg_color= "#F6A623", text_color="#2e1045",
        corner_radius=4, dropdown_fg_color="#3d1c57", dropdown_text_color= "#f0f0f0",
        dropdown_hover_color= "#F6A623", width= self.winfo_screenwidth() * 0.1,
        anchor= 'center',
        values= ['UBICACION'] )#+ general.recuperar_actividades())
        self.ubicacion.grid(row=0, column=1)
