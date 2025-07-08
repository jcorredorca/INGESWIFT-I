'''Funciones de backend generales'''

from views.admin import modulo_crear_funcionario
from views.funcionarios import modulo_asistencia
from views.inicio import inicio
from views.miembros import miembros

from views.admin import admin

def redirigir_pantalla(origen, rol):
    '''Esta función construye la ventana de cada rol para ser redirigido luego del login'''
    ventanas = {
        'MIEMBRO': miembros.Miembros,
        'FUNCIONARIO': modulo_asistencia.ModuloAsistencia,
        'ADMINISTRADOR': admin.Admin
    }

    ventana = ventanas[rol](origen)
    origen.contenido.destroy()
    origen.contenido = ventana
    origen.contenido.grid(row=1, column=0, sticky="nsew")

def log_out(master):
    '''Esta fucnion devuelve al usuario a la ventana principal'''
    master.contenido.destroy()
    master.contenido = inicio.Inicio(master)
    master.contenido.grid(row=1, column=0, sticky="nsew")
    for widget in master.encabezado.logout.winfo_children():
        widget.destroy()
    for widget in master.encabezado.links.winfo_children():
        widget.destroy()
