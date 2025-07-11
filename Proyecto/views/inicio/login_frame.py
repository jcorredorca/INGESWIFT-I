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

        self.fuente_titulo = ("Segoe UI",
                              max(40, int(self.winfo_screenwidth() * 0.02)), "bold")

        self.fuente_normal = ("Segoe UI",
                              max(25, int(self.winfo_screenwidth() * 0.01)))

        self.fuente_boton = ("Segoe UI",
                             max(22,int(self.winfo_screenwidth() * 0.009)), "bold")

        self.crear_titulo()
        self.crear_login()
        self.crear_cambio_contra()

    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=0)
        self.grid_rowconfigure(6, weight=1)

    def crear_titulo(self):
        '''Crea el titulo del log in'''
        titulo = CTkLabel(self, text="Ingresa tu usuario\ny contraseña",
                          font=self.fuente_titulo, text_color="white", justify="center")
        titulo.grid(row=1, column=0, pady=(30, 30), sticky="ns")

    def crear_login(self):
        '''Crea el loggin del contenido de Inicio'''
        # --- USUARIO ---
        usuario_frame = CTkFrame(self, fg_color="transparent")
        usuario_frame.grid(row=2, column=0, pady=(0, 15), padx=30, sticky="new")

        usuario_frame.grid_columnconfigure(0, weight=4)
        usuario_frame.grid_columnconfigure(1, weight=1)

        self.entry_usuario = CTkEntry(usuario_frame, placeholder_text="Usuario",
                                      font=self.fuente_normal, fg_color="whitesmoke", height=50)

        self.entry_usuario.grid(row=0, column=0, sticky="new")
        self.entry_usuario.bind("<KeyRelease>",
                                lambda event: self.revisar_color_entry(self.entry_usuario, event))
        self.entry_usuario.focus()

        dominio = CTkLabel(usuario_frame, text="@unal.edu.co",
        font=("Segoe UI", 20, "bold"), text_color="#CCCCCC")

        dominio.grid(row=0, column=1, sticky="w", padx=(10, 0))

        # --- CONTRASEÑA ---
        self.entry_contra = CTkEntry(self, placeholder_text="Contraseña",
                                    font=self.fuente_normal, fg_color="whitesmoke",
                                    height=50, show='•' )

        self.entry_contra.grid(row=3, column=0, pady=(0, 15), padx=30, sticky="nsew")


        # Eventos para cambiar el color al escribir
        self.entry_contra.bind("<KeyRelease>",
                               lambda event: self.revisar_color_entry(self.entry_contra, event))

        # --- BOTÓN DE LOGIN ---
        boton_login = CTkButton(self, text="Iniciar sesión", font=self.fuente_boton,
                    fg_color="#F6A623", text_color="#2e1045", cursor="hand2", hover_color="#d38e14",
                    corner_radius=6, border_spacing=10, command=self.verificar_login)
        boton_login.grid(row=4, column=0, pady=(0, 50))

        #Asociar evento de enter
        self.entry_contra.bind("<Return>", self.verificar_login)

    def crear_cambio_contra(self):
        '''Crea el boton de cambio de contraseña'''
        self.cambio_contra = CTkLabel(self, text="Cambiar mi contraseña",
                cursor="hand2", text_color = "#F6A623",
                font = self.fuente_normal)

        self.cambio_contra.grid(row=5, column=0, sticky='w')

        # Asociar evento de clic
        self.cambio_contra.bind("<Button-1>", self.desplegar_popup)
        self.cambio_contra.bind("<Enter>", self.entrada)
        self.cambio_contra.bind("<Leave>", self.salida)

    def desplegar_popup(self, event):
        '''Crea una ventana para el cambio de contraseña'''
        if event:
            CambioPopup(self)

    def revisar_color_entry(self, entry, event):
        '''Mantiene el color de texto de las entradas en el tono correcto'''
        if event:
            if entry.get().strip() in ["", "-- Seleccionar --"]:
                entry.configure(text_color="gray")
            else:
                entry.configure(text_color="black")

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

            #Creación de flags
            campos_vacios = self.verificar_campos_vacios()

            if campos_vacios:
                return

            try:
                login.autenticar_credenciales(usuario, contra)
            except ValueError as e:
                messagebox.showerror('Error', str(e))
            else:
                origen = self.master.master
                roles = login.recuperar_roles(usuario)
                utils.redirigir_pantalla(origen, roles)
                self.master.master.usuario = usuario

    def verificar_campos_vacios(self):
        '''Verifica si hay algún campo sin llenar'''
        alguno_vacio = False
        if self.entry_usuario.get() == "":
            alguno_vacio = True
        if self.entry_contra.get() == "":
            alguno_vacio = True

        if alguno_vacio:
            messagebox.showerror('Error', 'Hay al menos un campo sin llenar')

        return alguno_vacio
