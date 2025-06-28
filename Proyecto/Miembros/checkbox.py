from customtkinter import CTkFrame
from customtkinter import CTkCheckBox

class MyCheckboxFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.checkbox_1 = CTkCheckBox(self, text="checkbox 1")
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_2 = CTkCheckBox(self, text="checkbox 2")
        self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
