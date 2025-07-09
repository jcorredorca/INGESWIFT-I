'''Ventana emergente para menu de opciones'''

from customtkinter import CTkToplevel, CTkButton, CTkScrollableFrame


class MenuOpciones(CTkToplevel):
    '''Clase que representa una ventana emergente para escoger opciones'''

    def __init__(self, master, activador, fg_color, valores):
        super().__init__(master)
        self.fuente = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.012)), 'bold')
        self.activador = activador
        self.transient(master)
        self.configure(fg_color= fg_color, text_color= 'whitesmoke', font=self.fuente)
        self.overrideredirect(True)
        self.ancho =  int(self.winfo_screenwidth() * 0.2)
        self.alto = int(self.ancho)//2

        # Calcula el centro del activador
        act_x = activador.winfo_rootx()
        act_y = activador.winfo_rooty()
        act_h = activador.winfo_height()

        # Centra el menú respecto al activador
        x = act_x
        y = act_y + act_h
        self.geometry(f"{self.ancho}x{self.alto}+{x}+{y}")
        self.grab_set()
        self.opciones = {}

        frame_contenido = CTkScrollableFrame(self,fg_color=fg_color)
        frame_contenido.pack(fill="both", expand=True)
        for indice, opcion in enumerate(valores):

            boton = CTkButton(frame_contenido, text=opcion, fg_color=fg_color,
                              text_color="whitesmoke", font=self.fuente, anchor='w',
                              command=lambda opt=opcion: self.cambiar_opcion(opt),
                              hover_color="#F6A623")
            boton.grid(row=indice, column=0, sticky='ew')
            frame_contenido.columnconfigure(0, weight=1)

           # Bind global para cerrar al hacer clic fuera
        self.after(10, self._bind_click_outside)

    def _bind_click_outside(self):
        '''Capta los clicks fuera del menu desplegable'''
        self.master.bind_all("<Button-1>", self._on_click_outside, add="+")

    def _on_click_outside(self, event):
        '''Se asegura que e click haya sido por fuera'''
        if self.winfo_containing(event.x_root, event.y_root) is not self:
            self.master.unbind_all("<Button-1>")
            self.destroy()
            self.master.grab_set()

    def cambiar_opcion(self, opcion):
        '''Cambia la opcion del boton padre'''
        self.activador.configure(text=opcion)
        self.activador.update()
