'''Ventana emergente para el cambio de contraseña'''

from tkinter import messagebox
from customtkinter import CTkToplevel, CTkFrame, CTkLabel, CTkEntry, CTkButton
from services import login


class CambioPopup(CTkToplevel):
    '''Clase que representa una ventana emergente para cambiar la contraseña'''

    color_fondo ="#5A317A"

    def __init__(self, master):
        super().__init__(master)
        self.fuente = ("Arial", max(18, int(self.winfo_screenwidth() * 0.007)))

        self.configure(fg_color=CambioPopup.color_fondo)
        ancho = self.master.winfo_screenwidth() // 2
        alto = self.master.winfo_screenheight()//2
        x = (self.winfo_screenwidth() - ancho)//2 
        y = (self.winfo_screenheight() - alto) //2 
        self.geometry(f"{ancho}x{alto}+{x}+{y}")


        self.title("Cambio de contraseña")

        self.repartir_espacio()
        self.crear_espacio_formulario()
        self.construir_formulario()

        self.transient(master)
        self.grab_set()
        self.focus()

    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)

    def crear_espacio_formulario(self):
        '''Reserva el espacio para el formulario'''
        alto_rows = int(self.winfo_height()*0.2)

        self.campos_frame = CTkFrame(self, fg_color=CambioPopup.color_fondo)
        self.campos_frame.grid(row=0)
        self.campos_frame.grid_columnconfigure(0, weight=1)
        self.campos_frame.grid_columnconfigure(1, weight=4)
        self.campos_frame.grid_rowconfigure(0, weight=1, minsize=alto_rows)
        self.campos_frame.grid_rowconfigure(1, weight=2, minsize=alto_rows)
        self.campos_frame.grid_rowconfigure(2, weight=2, minsize=alto_rows)
        self.campos_frame.grid_rowconfigure(3, weight=2, minsize=alto_rows)
        self.campos_frame.grid_rowconfigure(4, weight=2, minsize=alto_rows)
        self.campos_frame.grid_rowconfigure(5, weight=1)

    def construir_formulario(self):
        '''Crea el formulario para la renovacion de la contraseña'''
        # TITULO
        fuente_titulo = ("Libre Baskerville", max(25, int(self.winfo_screenwidth()* 0.015)), "bold")
        titulo = CTkLabel(self.campos_frame, text="Módulo de cambio de contraseña",
                          font=fuente_titulo, text_color="white", justify="center")
        titulo.grid(row=0, columnspan=2)

        #Confirguar las etiquetas
        usuario_label=CTkLabel(self.campos_frame, text="Usuario:",
                               font=self.fuente, text_color='whitesmoke')
        usuario_label.grid(row=1, column=0, sticky='e')

        contra_antigua_label=CTkLabel(self.campos_frame, text="Contraseña antigua:",
                                      font=self.fuente, text_color='whitesmoke')
        contra_antigua_label.grid(row=2, column=0, sticky='e')

        contra_nueva_label=CTkLabel(self.campos_frame, text="Contraseña nueva:",
                                    font=self.fuente, text_color='whitesmoke')
        contra_nueva_label.grid(row=3, column=0, sticky='e')

        self.confirmacion_label=CTkLabel(self.campos_frame, text="Confirmar contraseña nueva:",
                                    font=self.fuente, text_color='whitesmoke')
        self.confirmacion_label.grid(row=4, column=0, sticky='e')

        #Configurar las entradas
        ancho_entry = int(self.winfo_width())*0.7
        self.entry_usuario = CTkEntry(self.campos_frame, fg_color="whitesmoke",
                                    font=self.fuente, width=ancho_entry)
        self.entry_usuario.grid(row=1, column=1)

        self.entry_contra_antigua = CTkEntry(self.campos_frame, fg_color="whitesmoke",
                                        font=self.fuente, width=ancho_entry, show='•')
        self.entry_contra_antigua.grid(row=2, column=1)

        self.entry_contra_nueva = CTkEntry(self.campos_frame, fg_color="whitesmoke",
                                        font=self.fuente, width=ancho_entry, show='•')
        self.entry_contra_nueva.grid(row=3, column=1)

        self.entry_contra_confirmacion = CTkEntry(self.campos_frame, fg_color="whitesmoke",
                                                font=self.fuente, width=ancho_entry, show='•')
        self.entry_contra_confirmacion.grid(row=4, column=1)

        #Frame para ubicar botones
        botones = CTkFrame(self, fg_color=CambioPopup.color_fondo)
        botones.grid(row=1)
        botones.grid_columnconfigure(0)
        botones.grid_columnconfigure(1)

        padx_botones = int(self.winfo_width()*0.25)
        boton_aceptar = CTkButton(
                    botones, text="Modificar contraseña", command=self.modificar_contra,
                    font=self.fuente, fg_color="#F6A623", text_color="black",
                    cursor="hand2", hover_color="#d38e14", corner_radius=6)
        boton_aceptar.grid(row=0, column=0, padx=padx_botones)

        button = CTkButton(botones, text="Cancelar", command=self.destroy, font=self.fuente,
                        fg_color="#F6A623", text_color="black", cursor="hand2", hover_color="#d38e14",
                        corner_radius=6)
        button.grid(row=0, column=1, padx=padx_botones)

    def verificar_confirmacion(self):
        '''Verifica que los campos nueva contraseña y confirmación coincidan'''
        nueva = self.entry_contra_nueva.get()
        confirmacion = self.entry_contra_confirmacion.get()

        if confirmacion != nueva:
            self.confirmacion_label.configure(text_color="#a70c0c")
            messagebox.showerror('Error', 'La contraseña y la confirmación no coinciden')
            return False

        self.confirmacion_label.configure(text_color='whitesmoke')
        return True

    def verificar_campos_vacios(self):
        '''Verifica si hay algún campo sin llenar'''
        alguno_vacio = False
        if self.entry_usuario.get() == "":
            alguno_vacio = True
        if self.entry_contra_antigua.get() == "":
            alguno_vacio = True
        if self.entry_contra_nueva.get() == "":
            alguno_vacio = True
        if self.entry_contra_confirmacion.get() == "":
            alguno_vacio = True

        if alguno_vacio:
            messagebox.showerror('Error', 'Hay al menos un campo vacío')

        return alguno_vacio


    def modificar_contra(self):
        '''Funcion para modificar la contraseña'''
        usuario = self.entry_usuario.get()
        contra = self.entry_contra_antigua.get()
        contra_nueva = self.entry_contra_nueva.get()
        credenciales_correctas = False

        #Declaración de flags
        campos_vacios = self.verificar_campos_vacios()
        coincidencia_confirmacion = self.verificar_confirmacion()

        if campos_vacios or not coincidencia_confirmacion:
            return

        try:
            credenciales_correctas = login.autenticar_credenciales(usuario, contra)
        except ValueError as e:
            messagebox.showerror('Error', str(e))

        if credenciales_correctas:
            #TODO: que mande correo
            login.cambiar_contrasena(usuario, contra_nueva)
            messagebox.showinfo('Actualización de contraseña',
                                'Su contraseña fue actualizada exitosamente')
            self.destroy()
