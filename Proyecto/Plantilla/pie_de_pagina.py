''' Pie de pagina de atun '''

from customtkinter import CTkFrame
from customtkinter import CTkLabel


class PiePagina(CTkFrame):
    '''Clase se que representa el pie de pagina'''

    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="#1a1a1a",corner_radius=1,height=160)
        self.grid_propagate(False)
        self.repartir_espacio()
        self.tamanio_fuente =  max(12, int(self.winfo_screenwidth() * 0.006))

        #Agregar labels
        self.descripcion = CTkFrame(self, fg_color="#1a1a1a")
        self.descripcion.grid(row=0, column=0, sticky="nsew")
        self.crear_descripcion()
        
        self.contacto = CTkFrame(self, fg_color="#00c3ff")
        self.contacto.grid(row=0, column=1, sticky="new")
        self.crear_contacto()

        self.direccion = CTkFrame(self, fg_color="#00ff11")
        self.direccion.grid(row=0, column=2, sticky="new")

    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def crear_descripcion(self):
        '''Crea la descripcion del footer'''
        padding_x = 20
        padding_y = 10

        nombre = CTkLabel(self.descripcion, 
        text="Sistema ATUN",
        text_color = "#F6A623" ,
        font = ("Libre Baskerville", self.tamanio_fuente, 'bold')
        )

        desc = CTkLabel(self.descripcion, 
        text="Asignación de turnos Universidad Nacional",
        text_color = "whitesmoke" ,
        font = ("Libre Baskerville", self.tamanio_fuente),
        )
        nombre.pack(anchor="w", padx=padding_x, pady=(padding_y, 0))
        desc.pack(anchor="nw", padx=padding_x)

    def crear_contacto(self):
        '''Crea el espacio de contacto del footer'''
        padding_y = 10

        correo = CTkLabel(self.contacto,
        text="atunoporte@unal.edu.co",
        cursor="hand2",
        text_color = "#F6A623" ,
        font = ("Libre Baskerville", self.tamanio_fuente)
        )
    