'''Funciones de backend generales'''

from views.inicio import inicio, pantalla_roles
from views.miembros import miembros
from views.funcionarios import funcionario
from views.admin import admin

def redirigir_pantalla(origen, roles:list):
    '''Esta función construye la ventana de cada rol para ser redirigido luego del login'''

    ventana = pantalla_roles.PantallaRoles(origen, roles)
    origen.contenido.destroy()
    origen.contenido = ventana
    origen.contenido.grid(row=1, column=0, sticky="nsew")

def redirigir_pantalla_miembro(origen):
    '''Esta función construye la ventana de miembros'''

    ventana = miembros.Miembros(origen)
    origen.contenido.destroy()
    origen.contenido = ventana
    origen.contenido.grid(row=1, column=0, sticky="nsew")

def redirigir_pantalla_funcionario(origen):
    '''Esta función construye la ventana de funcionarios'''

    ventana = funcionario.Funcionario(origen)
    origen.contenido.destroy()
    origen.contenido = ventana
    origen.contenido.grid(row=1, column=0, sticky="nsew")

def redirigir_pantalla_admin(origen):
    '''Esta función construye la ventana de administradores'''

    ventana = admin.Admin(origen)
    origen.contenido.destroy()
    origen.contenido = ventana
    origen.contenido.grid(row=1, column=0, sticky="nsew")

def log_out(master):
    '''Esta fucnion devuelve al usuario a la ventana principal'''
    master.contenido.destroy()
    master.usuario = None
    master.contenido = inicio.Inicio(master)
    master.contenido.grid(row=1, column=0, sticky="nsew")
    for widget in master.encabezado.logout.winfo_children():
        widget.destroy()
    for widget in master.encabezado.links.winfo_children():
        widget.destroy()
