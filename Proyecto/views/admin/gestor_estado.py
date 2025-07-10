from datetime import datetime

from customtkinter import (CTkButton, CTkEntry, CTkFrame, CTkLabel,
                           CTkScrollableFrame)


class GestionEstado(CTkFrame):
    '''Módulo de Administrador: gestión de estado de miembros activos/inactivos'''

    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="#2e1045")
        self.repartir_espacio()

        self.titulo = CTkLabel(self, text="GESTIÓN DE ESTADO DE MIEMBROS", 
                                font=("Segoe UI", 28, "bold"), text_color="white")
        self.titulo.grid(row=0, column=0, columnspan=3, pady=20)

        self.crear_encabezado_derecho()
        self.crear_listas()
        self.crear_botones()
        self.crear_busqueda()

    def crear_encabezado_derecho(self):
        '''Encabezado con TURNO y botón Log Out'''
        mini_encabezado = CTkFrame(self, fg_color="transparent")
        mini_encabezado.grid(row=0, column=2, sticky="ne", padx=20, pady=(20, 10))

        mini_encabezado.grid_columnconfigure(0, weight=1)
        mini_encabezado.grid_columnconfigure(1, weight=0)

        turno_actual = self.obtener_turno_actual()
        turno_label = CTkLabel(mini_encabezado, text=f"TURNO: {turno_actual}",
                            text_color="white", font=("Arial", 16, "bold"))
        turno_label.grid(row=0, column=0, sticky="e", padx=(0, 10))

    def obtener_turno_actual(self):
        '''Devuelve el turno actual como string (7–8am, etc)'''
        hora = datetime.now().hour
        if 7 <= hora < 22:
            siguiente = hora + 1
            sufijo_fin = "am" if siguiente < 12 else "pm"
            return f"{hora}–{siguiente}{sufijo_fin}"
        return "Fuera de horario"

    def repartir_espacio(self):
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)

        self.grid_rowconfigure(0, weight=0)  # Título
        self.grid_rowconfigure(1, weight=1)  # Espacio entre título y listas
        self.grid_rowconfigure(2, weight=4)  # Contenedores de listas y botones
        self.grid_rowconfigure(3, weight=0)  # Barra de búsqueda


    def crear_listas(self):
        '''Crea los scrollables para miembros activos e inactivos'''
        fuente_label = ("Segoe UI", 20, "bold")

        # Activos
        self.scroll_activos = CTkScrollableFrame(self, fg_color="#3d1c57")
        self.scroll_activos.grid(row=2, column=0, padx=20, sticky="nsew")
        
        label_activos = CTkLabel(self.scroll_activos, text="ACTIVOS", font=fuente_label, text_color="white")
        label_activos.pack(pady=(10, 10))

        for nombre in ["Miembro1", "Miembro2", "Miembro3", "Miembro4", "Miembro5"]:
            CTkLabel(self.scroll_activos, text=nombre, text_color="white",
                    font=("Segoe UI", 16), anchor="center", justify="center"
            ).pack(fill="x", padx=10, pady=4)

        # Inactivos
        self.scroll_inactivos = CTkScrollableFrame(self, fg_color="#3d1c57")
        self.scroll_inactivos.grid(row=2, column=2, padx=20, sticky="nsew")

        label_inactivos = CTkLabel(self.scroll_inactivos, text="INACTIVOS", font=fuente_label, text_color="white")
        label_inactivos.pack(pady=(10, 10))

        for nombre in ["MiembroA", "MiembroB", "MiembroC", "MiembroD", "MiembroE"]:
            CTkLabel(self.scroll_inactivos, text=nombre, text_color="white",
                    font=("Segoe UI", 16), anchor="center", justify="center"
            ).pack(fill="x", padx=10, pady=4)

    def crear_botones(self):
        '''Botones para mover miembros entre listas'''
        contenedor = CTkFrame(self, fg_color="transparent")
        contenedor.grid(row=2, column=1, sticky="nsew")

        contenedor.grid_rowconfigure((0, 1, 2), weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        self.boton_derecha = CTkButton(contenedor, text="→", font=("Segoe UI", 26, "bold"), 
                                    width=50, height=35,
                                    fg_color="#f6a623", hover_color="#d18c1a", text_color="#2e1045")
        self.boton_derecha.grid(row=0, column=0, pady=10)

        self.boton_izquierda = CTkButton(contenedor, text="←", font=("Segoe UI", 26, "bold"), 
                                        width=50, height=35,
                                        fg_color="#f6a623", hover_color="#d18c1a", text_color="#2e1045")
        self.boton_izquierda.grid(row=2, column=0, pady=10)


    def crear_busqueda(self):
        '''Barra para buscar miembros'''
        self.entry_busqueda = CTkEntry(self, placeholder_text="BUSCAR MIEMBRO",
                                       fg_color="white", text_color="black",
                                       font=("Segoe UI", 16), width=300)
        self.entry_busqueda.grid(row=3, column=0, columnspan=3, pady=(30, 20), sticky="n")
