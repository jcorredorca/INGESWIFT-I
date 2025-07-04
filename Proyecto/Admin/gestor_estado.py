from datetime import datetime

import customtkinter
from customtkinter import (CTkButton, CTkEntry, CTkFrame, CTkLabel,
                           CTkScrollableFrame)


class GestionEstado(CTkFrame):
    '''Módulo de Administrador: gestión de estado de miembros activos/inactivos'''

    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="#2e1045")
        self.repartir_espacio()

        self.titulo = CTkLabel(self, text="GESTIÓN DE ESTADO DE MIEMBROS", 
                                font=("Libre Baskerville", 28, "bold"), text_color="white")
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

        boton_logout = CTkButton(mini_encabezado, text="Log Out", font=("Arial", 14),
                                width=70, height=30,
                                fg_color="#a246cd", hover_color="#872fc0",
                                text_color="white", corner_radius=6)
        boton_logout.grid(row=0, column=1, sticky="e")

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
        self.grid_rowconfigure(3, weight=0)

    def crear_listas(self):
        '''Crea los scrollables para miembros activos e inactivos'''
        fuente_label = ("Libre Baskerville", 20, "bold")

        self.activos_label = CTkLabel(self, text="ACTIVOS", font=fuente_label, text_color="white")
        self.activos_label.grid(row=1, column=0, sticky="n", pady=(10, 5))

        self.scroll_activos = CTkScrollableFrame(self, fg_color="#3d1c57")
        self.scroll_activos.grid(row=1, column=0, padx=20, sticky="nsew")

        self.inactivos_label = CTkLabel(self, text="INACTIVOS", font=fuente_label, text_color="white")
        self.inactivos_label.grid(row=1, column=2, sticky="n", pady=(10, 5))

        self.scroll_inactivos = CTkScrollableFrame(self, fg_color="#3d1c57")
        self.scroll_inactivos.grid(row=1, column=2, padx=20, sticky="nsew")

        self.scroll_activos.configure(height=350)
        self.scroll_inactivos.configure(height=350)

        # Test data
        for nombre in ["Miembro1", "Miembro2", "Miembro3", "Miembro4", "Miembro5"]:
            CTkLabel(self.scroll_activos, text=nombre, text_color="white", anchor="w", font=("Libre Baskerville", 16)).pack(fill="x", padx=10, pady=4)

        for nombre in ["MiembroA", "MiembroB", "MiembroC", "MiembroD", "MiembroE"]:
            CTkLabel(self.scroll_inactivos, text=nombre, text_color="white", anchor="w", font=("Libre Baskerville", 16)).pack(fill="x", padx=10, pady=4)


    def crear_botones(self):
        '''Botones para mover miembros entre listas'''
        contenedor = CTkFrame(self, fg_color="transparent")
        contenedor.grid(row=1, column=1, sticky="nsew")

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
                                       font=("Libre Baskerville", 16), width=300)
        self.entry_busqueda.grid(row=3, column=0, columnspan=3, pady=(30, 20), sticky="n")
class VentanaPrueba(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Prueba Gestión Estado")
        self.geometry("1200x700")
        self.configure(fg_color="#2e1045")

        self.gestion = GestionEstado(self)
        self.gestion.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = VentanaPrueba()
    app.mainloop()