''' Pagina de inicio de atun '''

from customtkinter import CTkFrame,CTkLabel,CTkButton,CTkEntry

class LoginFrame(CTkFrame):
    '''Clase que representa la pagina de inicio de atun'''
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="#2e1045", corner_radius=1)
        self.repartir_espacio()
        self.crear_login()


    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

    def crear_login(self):
        '''Crea el loggin del contenido de Inicio'''
        fuente_titulo = ("Libre Baskerville", 56, "bold")
        fuente_normal = ("Arial", 28)
        fuente_boton = ("Arial", 24, "bold")

        # --- TÍTULO ---
        titulo = CTkLabel(self, text="Ingresa tu usuario y\ncontraseña",
                          font=fuente_titulo, text_color="white", justify="center")
        titulo.grid(row=1, column=0, pady=(30, 30), sticky="s")

        # --- USUARIO ---
        usuario_frame = CTkFrame(self, fg_color="transparent")
        usuario_frame.grid(row=2, column=0, pady=(0, 15), padx=30, sticky="new")
        usuario_frame.grid_columnconfigure(0, weight=4)
        usuario_frame.grid_columnconfigure(1, weight=1)

        self.entry_usuario = CTkEntry(usuario_frame, placeholder_text=" Usuario", 
                                      font=fuente_normal, fg_color="whitesmoke", height=50)

        self.entry_usuario.grid(row=0, column=0, sticky="new")

        dominio = CTkLabel(usuario_frame, text="@unal.edu.co",
        font=("Libre Baskerville", 20, "bold"), text_color="#CCCCCC")

        dominio.grid(row=0, column=1, sticky="w", padx=(10, 0))

        # --- CONTRASEÑA ---
        self.entry_contra = CTkEntry(self, placeholder_text=" Contraseña",
        font=fuente_normal, show="•", fg_color="whitesmoke", height=50)

        # Eventos para cambiar el color al escribir
        self.entry_contra.grid(row=3, column=0, pady=(0, 15), padx=30, sticky="new")
        self.entry_contra.bind("<KeyRelease>", self.revisar_color_contra)

        # --- BOTÓN DE LOGIN ---
        boton_login = CTkButton(self, text="Iniciar sesión", font=fuente_boton,
        fg_color="#F6A623", text_color="black", cursor="hand2", hover_color="#d38e14",
        corner_radius=6, border_spacing=10)
        boton_login.grid(row=4, column=0, pady=(0, 50))

    def revisar_color_contra(self, event):
        '''Mantiene el color de texto de la contraseña en el tono correcto'''
        if self.entry_contra.get().strip() == "":
            self.entry_contra.configure(text_color="gray")
        else:
            self.entry_contra.configure(text_color="black")
