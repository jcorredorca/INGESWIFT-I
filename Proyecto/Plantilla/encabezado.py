from customtkinter import CTkFrame

class Encabezado(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="white",corner_radius=1)
