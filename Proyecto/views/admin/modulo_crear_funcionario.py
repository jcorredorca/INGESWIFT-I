from tkinter import messagebox

#import customtkinter  # pruebas
from customtkinter import (CTkButton, CTkEntry, CTkFrame, CTkLabel,
                           CTkScrollableFrame, CTkTextbox)


class CrearFuncionarios(CTkFrame):
    '''Módulo de Administrador: Lista y registro de funcionarios'''

    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#2e1045")

        self.registrados = {
            "jcorredorca@unal.edu.co": "Juan Pablo Corredor Castañeda",
            "nbolanosf@unal.edu.co": "Nicolás Andrés Bolaños Fernández",
            "lalvarezla@unal.edu.co": "Laura Vanesa Álvarez Lafont",
            "sfetecua@unal.edu.co": "Santiago Andrés Fetecua Pulgarín"
        }
        self.funcionarios_activos = ["Nombre 1", "Nombre 2", "Nombre 3", "Nombre 4", "Nombre 5"]

        self.repartir_espacio()
        self.crear_encabezado_derecho()

        self.seccion = CTkFrame(self, fg_color="transparent")
        self.seccion.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.mostrar_lista_funcionarios()

    def crear_encabezado_derecho(self):
        mini_encabezado = CTkFrame(self, fg_color="transparent")
        mini_encabezado.grid(row=0, column=2, sticky="ne", padx=20, pady=(20, 10))
        mini_encabezado.grid_columnconfigure(0, weight=1)
        mini_encabezado.grid_columnconfigure(1, weight=0)
        CTkButton(mini_encabezado, text="Log Out", font=("Arial", 14),
                  width=70, height=30,
                  fg_color="#a246cd", hover_color="#872fc0",
                  text_color="white", corner_radius=6).grid(row=0, column=1, sticky="e")

    def repartir_espacio(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def mostrar_lista_funcionarios(self):
        for widget in self.seccion.winfo_children():
            widget.destroy()

        self.seccion.grid_columnconfigure((0,1,2), weight=1)
        CTkLabel(self.seccion, text="FUNCIONARIOS ACTIVOS",
                 font=("Libre Baskerville", 28, "bold"), text_color="white")\
            .grid(row=0, column=1, pady=(30, 10))

        lista_scroll = CTkScrollableFrame(self.seccion, fg_color="#3d1c57")
        lista_scroll.grid(row=1, column=1, padx=30, pady=(10, 20), sticky="nsew")

        for nombre in self.funcionarios_activos:
            CTkLabel(lista_scroll, text=nombre, text_color="white",
                     font=("Libre Baskerville", 18), anchor="center", justify="center")\
                     .pack(fill="x", pady=6, padx=20)

        CTkButton(self.seccion, text="Registrar Funcionario",
                  font=("Segoe UI", 18, "bold"), width=220,
                  fg_color="#f6a623", hover_color="#d18c1a",
                  text_color="#2e1045", corner_radius=10,
                  command=self.mostrar_formulario_correo)\
            .grid(row=2, column=1, pady=(0, 30))

    def mostrar_formulario_correo(self):
        for widget in self.seccion.winfo_children():
            widget.destroy()
        self.seccion.grid_columnconfigure((0,1,2), weight=1)

        CTkButton(self.seccion, text="←", width=40, height=35,
                  font=("Segoe UI", 20, "bold"), fg_color="#f6a623",
                  hover_color="#d18c1a", text_color="#2e1045",
                  command=self.mostrar_lista_funcionarios).grid(row=0, column=0, padx=(30, 0), sticky="w")

        CTkLabel(self.seccion, text="MÓDULO DE REGISTRO",
                 font=("Libre Baskerville", 28, "bold"), text_color="white")\
            .grid(row=1, column=1, pady=(30, 10))

        CTkLabel(self.seccion, text="Introduce el correo electrónico para continuar",
                 font=("Libre Baskerville", 18), text_color="white")\
            .grid(row=2, column=1, pady=(10, 10))

        self.entry_correo = CTkEntry(self.seccion, placeholder_text="Correo",
                                     font=("Libre Baskerville", 16), width=400,
                                     fg_color="white", text_color="black")
        self.entry_correo.grid(row=3, column=1, pady=(5, 20))

        CTkButton(self.seccion, text="VALIDAR",
                  font=("Segoe UI", 18, "bold"), width=120,
                  fg_color="#f6a623", hover_color="#d18c1a",
                  text_color="#2e1045", corner_radius=10,
                  command=self.verificar_correo).grid(row=4, column=1, pady=(0, 30))

    def verificar_correo(self):
        correo = self.entry_correo.get().strip().lower()

        if not correo:
            messagebox.showwarning("Campo vacío", "Por favor ingrese un correo antes de validar.")
            return

        if correo in self.registrados:
            self.mostrar_confirmacion_existente(correo)
        else:
            self.mostrar_formulario_completo(correo)

    def mostrar_confirmacion_existente(self, correo):
        for widget in self.seccion.winfo_children():
            widget.destroy()
        self.seccion.grid_columnconfigure((0,1,2), weight=1)

        CTkButton(self.seccion, text="←", width=40, height=35,
                  font=("Segoe UI", 20, "bold"), fg_color="#f6a623",
                  hover_color="#d18c1a", text_color="#2e1045",
                  command=self.mostrar_formulario_correo).grid(row=0, column=0, padx=(30, 0), sticky="w")

        CTkLabel(self.seccion, text="MÓDULO DE REGISTRO",
                 font=("Libre Baskerville", 28, "bold"), text_color="white")\
            .grid(row=1, column=1, pady=(30, 10))

        CTkLabel(self.seccion,
                 text="Este usuario ya está en la base de datos, ¿Desea registrarlo?",
                 font=("Libre Baskerville", 18), text_color="white", wraplength=600, justify="center")\
            .grid(row=2, column=1, pady=(10, 20))

        CTkButton(self.seccion, text="VALIDAR",
                  font=("Segoe UI", 18, "bold"), width=120,
                  fg_color="#f6a623", hover_color="#d18c1a",
                  text_color="#2e1045", corner_radius=10,
                  command=lambda: self.registrar_existente(correo))\
            .grid(row=3, column=1, pady=(0, 30))

    def mostrar_formulario_completo(self, correo):
        for widget in self.seccion.winfo_children():
            widget.destroy()
        self.seccion.grid_columnconfigure((0,1,2), weight=1)

        CTkButton(self.seccion, text="←", width=40, height=35,
                  font=("Segoe UI", 20, "bold"), fg_color="#f6a623",
                  hover_color="#d18c1a", text_color="#2e1045",
                  command=self.mostrar_formulario_correo).grid(row=0, column=0, padx=(30, 0), sticky="w")

        CTkLabel(self.seccion, text="MÓDULO DE REGISTRO",
                 font=("Libre Baskerville", 28, "bold"), text_color="white")\
            .grid(row=1, column=1, pady=(30, 10))

        self.entry_nombre = CTkEntry(self.seccion, placeholder_text="Nombre completo",
                                     font=("Libre Baskerville", 16), width=400,
                                     fg_color="white", text_color="black")
        self.entry_nombre.grid(row=2, column=1, pady=(10, 10))

        self.entry_rol = CTkEntry(self.seccion, placeholder_text="Rol en la universidad",
                                  font=("Libre Baskerville", 16), width=400,
                                  fg_color="white", text_color="black")
        self.entry_rol.grid(row=3, column=1, pady=(10, 10))

        self.entry_correo_final = CTkEntry(self.seccion)
        self.entry_correo_final.insert(0, correo)
        self.entry_correo_final.configure(state="disabled")
        self.entry_correo_final.grid(row=4, column=1, pady=(10, 20))

        CTkButton(self.seccion, text="VALIDAR",
                  font=("Segoe UI", 18, "bold"), width=120,
                  fg_color="#f6a623", hover_color="#d18c1a",
                  text_color="#2e1045", corner_radius=10,
                  command=self.registrar_nuevo).grid(row=5, column=1, pady=(0, 30))

    def registrar_existente(self, correo):
        nombre = self.registrados.get(correo, correo)
        if nombre not in self.funcionarios_activos:
            self.funcionarios_activos.append(nombre)
        self.mostrar_lista_funcionarios()

    def registrar_nuevo(self):
        nombre = self.entry_nombre.get().strip()
        rol = self.entry_rol.get().strip()

        if not nombre or not rol:
            messagebox.showwarning("Campos incompletos", "Por favor complete todos los campos.")
            return

        if nombre in self.funcionarios_activos:
            messagebox.showinfo("Ya registrado", f"{nombre} ya se encuentra en la lista de funcionarios.")
            return

        self.funcionarios_activos.append(nombre)
        self.mostrar_lista_funcionarios()

# PRUEBAS
# class VentanaPrueba(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("Prueba Crear Funcionarios")
#         self.geometry("1200x700")
#         self.configure(fg_color="#2e1045")

#         self.gestion = CrearFuncionarios(self)
#         self.gestion.pack(fill="both", expand=True)

# if __name__ == "__main__":
#     app = VentanaPrueba()
#     app.mainloop()