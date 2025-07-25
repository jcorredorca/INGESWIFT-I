'''Esta clase representa la ventana emergente para la creacion/edicion de horarios'''
from __future__ import annotations
from abc import ABC, abstractmethod
from customtkinter import CTkToplevel
from . import reservar, eliminar


class StateHorarioMiembros(CTkToplevel):
    """
    Esta clase genera una venta u otra dependiendo del estado
    """

    _state = None

    def __init__(self, master, state: State) -> None:
        super().__init__(master)

        self.configurar_ventana()

        self.title("Reserva")

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
    def context(self) -> StateHorarioMiembros:
        '''Contexto actual del estado'''
        return self._context

    @context.setter
    def context(self, contexto: StateHorarioMiembros) -> None:
        self._context = contexto

    @abstractmethod
    def renderizar(self) -> None:
        '''Este metodo renderiza el contenido dado un estado'''

class Reservar(State):
    '''Esta clase representa el widget del estado de creacion'''
    def renderizar(self) -> None:
        contenido = reservar.Reservar(self.context)
        contenido.pack(fill="both", expand=True)

class Eliminar(State):
    '''Esta clase representa el widget del estado de edicion y eliminacion'''

    def renderizar(self) -> None:
        contenido = eliminar.Eliminar(self.context)
        contenido.pack(fill="both", expand=True)

# class Interes(State):
#     '''Esta clase representa el widget del estado de edicion y eliminacion'''
#     def renderizar(self) -> None:
#         contenido = EditarHorario(self.context)
#         contenido.pack(fill="both", expand=True)
