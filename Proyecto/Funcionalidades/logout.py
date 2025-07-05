'''Se encarga de volver a la ventana principal'''
from Inicio import inicio

def log_out(master,actual):
    '''Esta fucnion devuelve al usuario a la ventana principal'''
    actual.destroy()
    master.contenido = inicio.Inicio(master)
    master.contenido.grid(row=1, column=0, sticky="nsew")
    for widget in master.encabezado.links.winfo_children():
        widget.destroy()
