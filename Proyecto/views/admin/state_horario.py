'''Esta clase representa la ventana emergente para la creacion/edicion de horarios'''
from __future__ import annotations
from abc import ABC, abstractmethod
from customtkinter import CTkToplevel
from .crear_horario import CrearHorario
from .editar_horario import EditarHorario
from .crear_horario_masivo import CrearHorarioMasivo

class StateHorario(CTkToplevel):
    """
    Esta clase genera una venta u otra dependiendo del estado
    """

    _state = None

    def __init__(self, master, state: State, celdas: set = None) -> None:
        super().__init__(master)
        self.celdas = celdas
        self.configurar_ventana()

        self.title("Crear horario")

        self.repartir_espacio()

        self.transition_to(state)

    def configurar_ventana(self):
        '''Configura las dimensiones y posicion de la ventana'''
        self.configure(fg_color="#3d1c57")
        factor = 2 if self.master.winfo_screenwidth() < 2000 else 3
        ancho = self.master.winfo_screenwidth() // factor
        alto = self.master.winfo_screenheight()//factor
        x = (self.winfo_screenwidth() - ancho)//factor
        y = (self.winfo_screenheight() - alto) //factor
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

        self.update()
        self.transient(self.master)
        self.grab_set()
        self.focus()

    def repartir_espacio(self):
        '''Reparte el espacio '''
        self.grid_columnconfigure(0, weight=1)

    def transition_to(self, state: State):
        """
        The Context allows changing the State object at runtime.
        """
        self._state = state
        self._state.context = self

    def renderizar_contenido(self):
        '''Este metodo renderiza el contenido dado un estado'''
        self._state.renderizar()

class State(ABC):
    """
    Clase base del estado
    """

    @property
    def context(self) -> StateHorario:
        '''Contexto actual del estado'''
        return self._context

    @context.setter
    def context(self, contexto: StateHorario) -> None:
        self._context = contexto

    @abstractmethod
    def renderizar(self) -> None:
        '''Este metodo renderiza el contenido dado un estado'''

class Creacion(State):
    '''Esta clase representa el widget del estado de creacion'''
    def renderizar(self) -> None:
        contenido = CrearHorario(self.context)
        contenido.pack(fill="both", expand=True)
class CreacionMasiva(State):
    '''Esta clase representa el widget del estado de creacion de varios horarios'''
    def renderizar(self) -> None:
        contenido = CrearHorarioMasivo(self.context, self.context.celdas)
        contenido.pack(fill="both", expand=True)

class EdicionEliminacion(State):
    '''Esta clase representa el widget del estado de edicion y eliminacion'''
    def renderizar(self) -> None:
        contenido = EditarHorario(self.context)
        contenido.pack(fill="both", expand=True)
