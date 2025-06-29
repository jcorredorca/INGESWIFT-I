''' Pie de pagina de atun '''

import webbrowser
from customtkinter import CTkFrame
from customtkinter import CTkLabel

class PiePagina(CTkFrame):
    '''Clase que representa el pie de pagina'''

    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="#1a1a1a",corner_radius=1,height=160)
        self.grid_propagate(False)
        self.repartir_espacio()
        self.tamanio_fuente =  max(12, int(self.winfo_screenwidth() * 0.0057))

        #Agregar labels
        self.descripcion = CTkFrame(self, fg_color="#1a1a1a")
        self.descripcion.grid(row=0, column=0, sticky="nsew")
        self.crear_descripcion()

        self.contacto = CTkFrame(self, fg_color="#1a1a1a")
        self.contacto.grid(row=0, column=1, sticky="new")
        self.crear_contacto()

        self.direccion = CTkFrame(self, fg_color="#1a1a1a")
        self.direccion.grid(row=0, column=2, sticky="new")
        self.crear_direccion()

        self.separador = CTkFrame(self, height=2, fg_color="gray")
        self.separador.grid(row=1, column=0, sticky="new", padx=10, pady=5, columnspan=3)

        cp_mssg = "\u00A9 2025 Sistema ATUN Universidad Nacional de Colombia. All rights reserved."
        self.copy = CTkLabel(self, text=cp_mssg,
        text_color = "#b0b0b0",
        font = ("Libre Baskerville", self.tamanio_fuente),
        )
        self.copy.grid(row=2, column=0, sticky="new", padx=10, pady=5, columnspan=3)

    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2,weight=1)

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

        self.contacto.grid_columnconfigure(0, weight=1)  # Tu contenido
        self.contacto.grid_columnconfigure(1, weight=1)  # Tu contenido

        self.contacto.grid_rowconfigure(0, weight=0, minsize=0)
        self.contacto.grid_rowconfigure(1, weight=0, minsize=0)

        contacto_label = CTkLabel(self.contacto,
        text="Contacto: ",
        cursor="hand2",
        text_color = "whitesmoke" ,
        font = ("Libre Baskerville", self.tamanio_fuente, 'bold')
        )
        contacto_label.grid(row=0, column=0, sticky='e', pady=(padding_y,0))

        self.correo = CTkLabel(self.contacto,
        text="atunsoporte@unal.edu.co",
        cursor="hand2",
        text_color = "#F6A623" ,
        font = ("Libre Baskerville", self.tamanio_fuente)
        )
        self.correo.grid(row=0, column=1, sticky='w', pady=(padding_y,0))

        telefono_label = CTkLabel(self.contacto,
        text="Tel: ",
        text_color = "whitesmoke" ,
        font = ("Libre Baskerville", self.tamanio_fuente, 'bold')
        )
        telefono_label.grid(row=1, column=0, sticky='e')

        telefono = CTkLabel(self.contacto,
        text="(+57) 316 5000 ext:12345",
        text_color = "#F6A623" ,
        font = ("Libre Baskerville", self.tamanio_fuente)
        )
        telefono.grid(row=1, column=1, sticky='w')

        # Asociar evento de clic
        self.correo.bind("<Button-1>", self.abrir_correo)
        self.correo.bind("<Enter>", self.entrada)
        self.correo.bind("<Leave>", self.salida)

    def crear_direccion(self):
        '''Crea el espacio de direccion del footer'''
        direccion_label = CTkLabel(self.direccion, 
        text="Sede Bogotá - Edificio 454 - Salón 403",
        text_color = "whitesmoke" ,
        font = ("Libre Baskerville", self.tamanio_fuente),
        )
        direccion_label.pack(anchor="e", padx=20, pady=(20, 0))

    def abrir_correo(self, event):
        '''Abre el correo asociado a el label'''
        if event:
            webbrowser.open("mailto:atunsoporte@unal.edu.co")

    def entrada(self, event):
        '''Evento de entrada para simular un hover'''
        if event:
            self.correo.configure(text_color="#B7770F")

    def salida(self, event):
        '''Evento de salida para simular un hover'''
        if event:
            self.correo.configure(text_color="#F6A623")
    