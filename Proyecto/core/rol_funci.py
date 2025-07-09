'''Funciones de backend para el rol Funcionario'''

from views.funcionarios import modulo_asistencia, registro_extemporaneo, registro_miembro, sesion_cerrada

def redirigir_pantalla_miembros(origen):
    '''Esta función construye la ventana para registrar miembros'''

    ventana = registro_miembro.RegistroMiembro(origen)
    origen.contenido.destroy()
    origen.contenido = ventana
    origen.contenido.grid(row=1, column=0, sticky="nsew")

def redirigir_pantalla_asistencia(origen):
    '''Esta función construye la ventana para gestionar a los funcionarios'''

    ventana = modulo_asistencia.ModuloAsistencia(origen)
    origen.contenido.destroy()
    origen.contenido = ventana
    origen.contenido.grid(row=1, column=0, sticky="nsew")