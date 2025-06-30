''' Pagina de inicio de atun '''
from os import path

from customtkinter import CTkFrame, CTkImage, CTkLabel
from Inicio.Login import login_frame
from PIL import Image


class Inicio(CTkFrame):
    '''Clase que representa la pagina de inicio de atun'''
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="#2e1045", corner_radius=1)
        self.repartir_espacio()
        # Enlazar para cambios en imagenes
        self.bind("<Configure>", self.redimensionar)
        self.tamanio_fuente =  max(12, int(self.winfo_screenwidth() * 0.0065))

        self.contenido_izq = CTkFrame(self, fg_color="#2e1045")
        self.contenido_izq.grid(row=0, column=0, sticky="nsew")
        self.crear_contenido_izq()

        self.separador = CTkFrame(self, width=3, fg_color="#a246cd")
        self.separador.grid(row=0, column=1, sticky="ns", padx=(50,0), pady=10,  rowspan=3)

        self.contenido_der = login_frame.LoginFrame(self)
        self.contenido_der.grid(row=0, column=2, sticky="ns", padx=5, pady=10,  rowspan=2)


    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0,weight=1)

    def crear_contenido_izq(self):
        '''Crea la zona izquierda del contenido de Inicio'''
        self.contenido_izq.grid_rowconfigure(0, weight=1)
        self.contenido_izq.grid_rowconfigure(1, weight=1)

        self.inicio_img = self.crear_imagenes_ctk()
        self.inicio_img_label = CTkLabel(self.contenido_izq, image=self.inicio_img, text='')
        self.inicio_img_label.grid(row=0, column=0, sticky="s", padx=(40,0), pady=(0,20))

        desc_afid = "AFID es un programa de la Universidad " \
        "Nacional de Colombia que promueve el bienestar " \
        "integral de la comunidad universitaria" \
        " a través del ejercicio físico. Ofrece acceso a un " \
        "gimnasio institucional con equipos modernos, clases dirigidas " \
        "y asesoría profesional, fomentando hábitos de vida saludables, " \
        "mejorando la condición física y reduciendo el estrés académico."

        desc = CTkLabel(self.contenido_izq, text=desc_afid, text_color = "whitesmoke",
        font = ("Libre Baskerville", self.tamanio_fuente), wraplength=700, justify="center")
        desc.grid(row=1, column=0, sticky="nwe", padx=(50,0), pady=(0,0))

    def redimensionar(self, event):
        '''Este metodo ajusta el tamaño de la imagen'''
        if event:
            # Calcular nuevo tamaño proporcional a la ventana
            nuevo_ancho = 622 * self.winfo_width()/2027
            nuevo_alto =  371 * self.winfo_width()/2027

            # Redimensionar imagen
            self.inicio_img.configure(size=(nuevo_ancho, nuevo_alto))
            self.update()

    def crear_imagenes_ctk(self):
        '''Este metodo crea los objetos imagen para mostrarlo en un label'''

        base_dir = path.dirname(__file__)
        # Rutas a imagenes
        ruta_inicio_img = path.join(base_dir,"..","Imagenes", "Inicio.png")

        inicio_img = CTkImage(light_image=Image.open(ruta_inicio_img),
        size= (622*1.5, 371*1.5))

        return inicio_img
