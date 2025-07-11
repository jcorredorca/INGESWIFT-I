'''Funciones de backend para el rol Administrador'''

from views.admin import gestor_estado, ventana_horarios

from views.admin import crear_funcionario


def redirigir_pantalla_horarios(origen):
    '''Esta función construye la ventana de crear horarios'''

    ventana = ventana_horarios.VentanaHorarios(origen)
    origen.contenido.destroy()
    origen.contenido = ventana
    origen.contenido.grid(row=1, column=0, sticky="nsew")

def redirigir_pantalla_estado_miembros(origen):
    '''Esta función construye la ventana para gestionar el estado de los miembros'''

    ventana = gestor_estado.GestionEstado(origen)
    origen.contenido.destroy()
    origen.contenido = ventana
    origen.contenido.grid(row=1, column=0, sticky="nsew")

def redirigir_pantalla_funcionarios(origen):
    '''Esta función construye la ventana para gestionar a los funcionarios'''

    ventana = crear_funcionario.CrearFuncionarios(origen)
    origen.contenido.destroy()
    origen.contenido = ventana
    origen.contenido.grid(row=1, column=0, sticky="nsew")
