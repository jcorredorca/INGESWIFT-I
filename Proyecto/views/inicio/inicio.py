''' Pagina de inicio de atun '''
from os import path
from customtkinter import CTkFrame, CTkImage, CTkLabel
from PIL import Image
from . import login_frame
from config import IMG_PATH


class Inicio(CTkFrame):
    '''Clase que representa la pagina de inicio de atun'''
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="#2e1045", corner_radius=1)
        self.repartir_espacio()

        self.tamanio_fuente =  max(12, int(self.winfo_screenwidth() * 0.006))

        self.contenido_izq = CTkFrame(self, fg_color="#2e1045")
        self.contenido_izq.grid(row=0, column=0, sticky="ns")
        self.abrir_imagen()
        self.crear_contenido_izq()

        self.separador = CTkFrame(self, width=3, fg_color="#a246cd")
        self.separador.grid(row=0, column=1, sticky="ns")

        self.contenido_der = login_frame.LoginFrame(self)
        self.contenido_der.grid(row=0, column=2, sticky="ns")

        self.actualizar_dimensiones_imagen()

    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0,weight=1)

    def crear_contenido_izq(self):
        '''Crea la zona izquierda del contenido de Inicio'''
        self.contenido_izq.grid_rowconfigure(0, weight=2)
        self.contenido_izq.grid_rowconfigure(1, weight=1)

        self.imagen_inicio_label = CTkLabel(self.contenido_izq, text='')
        self.imagen_inicio_label.grid(row=0, column=0, sticky="ns")

        desc_afid = "AFID es un programa de la Universidad " \
        "Nacional de Colombia que promueve el bienestar " \
        "integral de la comunidad universitaria" \
        " a través del ejercicio físico. Ofrece acceso a un " \
        "gimnasio institucional con equipos modernos, clases dirigidas " \
        "y asesoría profesional, fomentando hábitos de vida saludables, " \
        "mejorando la condición física y reduciendo el estrés académico."

        wrap = 600 if self.winfo_screenwidth() < 2000 else 750
        desc = CTkLabel(self.contenido_izq, text=desc_afid, text_color = "whitesmoke",
        font = ("Segoe UI", self.tamanio_fuente), wraplength= wrap, justify="center")
        desc.grid(row=1, column=0, sticky="n")

    def abrir_imagen(self):
        '''Este metodo crea los objetos imagen para mostrarlo en un label'''

        # Rutas a imagen
        ruta_inicio_img = path.join(IMG_PATH, "Inicio.png")

        self.imagen_inicio = Image.open(ruta_inicio_img)


    def actualizar_dimensiones_imagen(self):
        '''Ajusta automáticamente las dimensiones de la imagen al frame'''

        factor = 1/3
        frame_height = self.master.winfo_screenheight()*factor

        new_width = frame_height* 622/371

        imagen_inicio_tk = CTkImage(light_image=self.imagen_inicio, size=(new_width,frame_height))

        self.imagen_inicio_label.configure(image= imagen_inicio_tk)

        self.master.update()
