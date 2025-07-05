''' Vista del panel de horarios para miembros'''
from customtkinter import CTkFrame,CTkOptionMenu,CTkButton
from .horario_semanal import HorarioSemanal
from Funcionalidades import horarios,logout
from Plantilla import boton_adicional

class Miembros(CTkFrame):
    ''' Esta clase representa el panel de horarios para miembros '''
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color= "#2e1045", corner_radius=1)
        self.repartir_espacio()

        self.crear_menu_opciones()

        self.horario = HorarioSemanal(self)
        self.horario.grid(row=1, column=3, sticky='e')

        self.logout = boton_adicional.BotonAdicional(master.encabezado.links,
                                                    texto='LogOut', comando= self.llamar_a_logout)
        self.logout.pack(padx=(10,0))


    def repartir_espacio(self):
        '''Reparte el espacio '''

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
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
        values= ['Escoge tu Plan'] + horarios.recuperar_actividades()
        )
        self.opciones_busqueda.grid(row=1, column=1, sticky = 'n', padx=(5,0) )

    def llamar_a_logout(self):
        '''Este metodo llama a la funcion logout'''
        logout.log_out(self.master,self)
