from customtkinter import CTkScrollableFrame


class Inicio(CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color='#2b133a',corner_radius=1)