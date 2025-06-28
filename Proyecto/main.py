'''Programa principal desde el cual se crea la ventana'''
from ctypes import windll
import Plantilla.ventana_principal as vp

windll.shcore.SetProcessDpiAwareness(1)
app = vp.App()
app.mainloop()
