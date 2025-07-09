''' Login para atun '''



from tkinter import messagebox

from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel, CTkOptionMenu, CTkToplevel
from services import login
from .cambio_popup import CambioPopup
from core import utils

class LoginFrame(CTkFrame):
    '''Clase que representa el formulario de login de atun'''
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="#2e1045", corner_radius=1)
        self.repartir_espacio()
        self.crear_login()

    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=0)
        self.grid_rowconfigure(6, weight=1)

    def crear_login(self):
        '''Crea el loggin del contenido de Inicio'''
        fuente_titulo = ("Libre Baskerville", max(40, int(self.winfo_screenwidth() * 0.02)), "bold")
        fuente_normal = ("Arial", max(25, int(self.winfo_screenwidth() * 0.01)))
        fuente_boton = ("Arial", max(22,int(self.winfo_screenwidth() * 0.009)), "bold")

        # --- TÍTULO ---
        titulo = CTkLabel(self, text="Ingresa tu usuario\ny contraseña",
                          font=fuente_titulo, text_color="white", justify="center")
        titulo.grid(row=1, column=0, pady=(30, 30), sticky="ns")

        # --- USUARIO ---
        usuario_frame = CTkFrame(self, fg_color="transparent")
        usuario_frame.grid(row=2, column=0, pady=(0, 15), padx=30, sticky="new")
        usuario_frame.grid_columnconfigure(0, weight=4)
        usuario_frame.grid_columnconfigure(1, weight=1)

        self.entry_usuario = CTkEntry(usuario_frame, placeholder_text="Usuario",
                                      font=fuente_normal, fg_color="whitesmoke", height=50)

        self.entry_usuario.grid(row=0, column=0, sticky="new")
        self.entry_usuario.bind("<KeyRelease>",
                                lambda event: self.revisar_color_entry(self.entry_usuario, event))

        dominio = CTkLabel(usuario_frame, text="@unal.edu.co",
        font=("Libre Baskerville", 20, "bold"), text_color="#CCCCCC")

        dominio.grid(row=0, column=1, sticky="w", padx=(10, 0))

        # --- ROL ---
        roles = ['-- Seleccionar --'] + login.recuperar_roles()
        self.entry_rol = CTkOptionMenu(self, values=roles,
            font=fuente_normal, text_color="gray", fg_color="whitesmoke",
            command=lambda _: self.revisar_color_entry(self.entry_rol, True))

        self.entry_rol.grid(row=3, column=0, pady=(0, 15), padx=30, sticky="new")

        self.entry_rol.set("-- Seleccionar --")

        # --- CONTRASEÑA ---
        self.entry_contra = CTkEntry(self, placeholder_text="Contraseña",
                                    font=fuente_normal, fg_color="whitesmoke", height=50, show='•' )

        # Eventos para cambiar el color al escribir
        self.entry_contra.grid(row=4, column=0, pady=(0, 15), padx=30, sticky="nsew")
        self.entry_contra.bind("<KeyRelease>",
                               lambda event: self.revisar_color_entry(self.entry_contra, event))

        # --- BOTÓN DE LOGIN ---
        boton_login = CTkButton(self, text="Iniciar sesión", font=fuente_boton,
                    fg_color="#F6A623", text_color="#2e1045", cursor="hand2", hover_color="#d38e14",
                    corner_radius=6, border_spacing=10, command=self.verificar_login)
        boton_login.grid(row=5, column=0, pady=(0, 50))

        # --- CAMBIO DE CONTRASEÑA ---
        self.cambio_contra = CTkLabel(self,
        text="Cambiar mi contraseña",
        cursor="hand2",
        text_color = "#F6A623" ,
        font = ("Libre Baskerville", self.winfo_screenwidth() * 0.01)
        )

        self.cambio_contra.grid(row=6, column=0, sticky='w')

        # Asociar evento de clic
        self.cambio_contra.bind("<Button-1>", self.desplegar_popup)
        self.cambio_contra.bind("<Enter>", self.entrada)
        self.cambio_contra.bind("<Leave>", self.salida)

        #Asociar evento de enter
        self.entry_contra.bind("<Return>", self.verificar_login)

    def revisar_color_entry(self, entry, event):
        '''Mantiene el color de texto de las entradas en el tono correcto'''
        if event:
            if entry.get().strip() in ["", "-- Seleccionar --"]:
                entry.configure(text_color="gray")
            else:
                entry.configure(text_color="black")

    def desplegar_cambio_contra(self, event):
        '''Despliega una ventana emergente para cambiar la conntraseña'''

        color_fondo = "#a783c2"

        if event:
            #Creación de la ventana emergente
            popup = CTkToplevel(self, fg_color=color_fondo)
            ancho = self.winfo_screenwidth()//2
            alto = self.winfo_screenheight()//2
            popup.geometry(f"{ancho}x{alto}")
            popup.title("Cambio de contraseña")

            popup.grid_columnconfigure(0, weight=1)

            popup.grid_rowconfigure(0, weight=2)
            popup.grid_rowconfigure(1, weight=1)

            #Creación de un fram para ubicar el formulario de cambio de contraseña
            cambio_frame = CTkFrame(popup, fg_color=color_fondo)
            cambio_frame.grid(row=0)
            cambio_frame.grid_columnconfigure(0, weight=1)
            cambio_frame.grid_columnconfigure(1, weight=2)
            cambio_frame.grid_columnconfigure(2, weight=1)
            cambio_frame.grid_rowconfigure(0, weight=1)
            cambio_frame.grid_rowconfigure(1, weight=2)
            cambio_frame.grid_rowconfigure(2, weight=1)

            label=CTkLabel(cambio_frame, text="Cambia la contraseñaaaa!")
            label.grid(row=1, column=1)

            #Frame para ubicar botones
            botones = CTkFrame(popup, fg_color=color_fondo)
            botones.grid(row=1)

            button = CTkButton(botones, text="Cerrar", command=popup.destroy)
            button.grid()

            popup.transient(self)
            popup.grab_set()
            popup.focus()

    def entrada(self, event):
        '''Evento de entrada para simular un hover'''
        if event:
            self.cambio_contra.configure(text_color="#B7770F")

    def salida(self, event):
        '''Evento de salida para simular un hover'''
        if event:
            self.cambio_contra.configure(text_color="#F6A623")

    def verificar_login(self, event=True):
        '''Función para verificar las credenciales'''
        if event:
            usuario = self.entry_usuario.get()
            contra = self.entry_contra.get()
            rol = self.entry_rol.get()

            #Creación de flags
            campos_vacios = self.verificar_campos_vacios()

            if campos_vacios:
                return

            try:
                login.autenticar_credenciales(usuario, contra)
                login.verificar_rol(usuario, rol)
            except ValueError as e:
                messagebox.showerror('Error', str(e))
            else:
                origen = self.master.master
                utils.redirigir_pantalla(origen, rol)

    def verificar_campos_vacios(self):
        '''Verifica si hay algún campo sin llenar'''
        alguno_vacio = False
        if self.entry_usuario.get() == "":
            alguno_vacio = True
        if self.entry_contra.get() == "":
            alguno_vacio = True
        if self.entry_rol.get() == "-- Seleccionar --":
            alguno_vacio = True

        if alguno_vacio:
            messagebox.showerror('Error', 'Hay al menos un campo sin llenar')

        return alguno_vacio

    def desplegar_popup(self, event):
        '''Crea una ventana para el cambio de contraseña'''
        if event:
            CambioPopup(self)
