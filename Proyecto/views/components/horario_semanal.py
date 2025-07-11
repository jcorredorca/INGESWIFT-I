''' Crea el horario semanal para mostrar los horarios '''
from datetime import time, datetime, timedelta
from customtkinter import CTkFrame, CTkLabel
from .sesion_celda import SesionCelda
from services import administrador

class HorarioSemanal(CTkFrame):
    '''Clase que crea el horario semanal'''
    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="#3d1c57", corner_radius=10)
        self.columnconfigure(tuple(range(7)), weight=1)
        self.rowconfigure(tuple(range(15)), weight=1)

        self.dias = []
        self.horas = self.horas = [
            f"{time(hour=h).strftime('%I:%M')} - {time(hour=h+1).strftime('%I:%M %p')}"
            for h in range(6, 20)]

        # Lista de filas: [ [(0,0), (0,1), ...], [(1,0), ...] ]
        self.celdas: list[list[CTkLabel]] = []

        self.crear_cabecera()
        self.crear_horario()

    def crear_cabecera(self):
        '''Crea la cabecera con los dias de la semana'''
        fuente_dias = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.012)))
        dias = ["", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]

        #Facto de redimencionamiento para el ancho de las columnas
        factor = 0.075 if self.winfo_screenwidth() < 2000 else 0.05

        for col, dia in enumerate(dias):
            label = CTkLabel(self, text=dia, font=fuente_dias, text_color='white',
                             width= self.winfo_screenwidth() * factor)
            label.grid(row=0, column=col, sticky="nsew", padx=10, pady=10)
            self.dias.append(label)

    def crear_horario(self):
        '''Crea el resto del horario incluyendo los bloques horarios'''

        fuente_horas = ("Segoe UI", max(15,int(self.winfo_screenwidth() * 0.01)))

        dias = self.dias_semana()
        horas = self.tiempos_dia()

        plan = self.master.opciones_busqueda.get()
        for fila, hora in enumerate(self.horas, start=1):
            fila_celdas = []

            # Columna 0 (horarios)
            hora_label = CTkLabel(self, text=hora, font=fuente_horas, anchor='w',
                                  text_color='white')
            hora_label.grid(row=fila, column=0, sticky="nsew", padx=(4,5), pady=3)

            # Celdas de Lunes a Sábado
            for col in range(1, 7):
                fecha = datetime.combine(dias[col-1], horas[fila-1])
                fg_color= "#f0f0f0"
                hover_color ="#A8A4A4"
                if administrador.hay_sesiones(plan, fecha):
                    fg_color = '#c3f7c8'
                    hover_color = '#e3fae3'

                celda = SesionCelda(self, fecha, fg_color, hover_color)
                celda.grid(row=fila, column=col, sticky="nsew", padx=3, pady=3)
                fila_celdas.append(celda)

            self.celdas.append(fila_celdas)

    def actualizar_celdas(self, actividad):
        '''Actualiza el estado de las celdas'''
        dias = self.dias_semana()
        horas = self.tiempos_dia()
        for i_fila, fila in enumerate(self.celdas):
            for i_columna, columna in enumerate(fila):
                columna :SesionCelda = columna
                fecha = datetime.combine(dias[i_columna], horas[i_fila])
                fg_color= "#f0f0f0"
                hover_color ="#A8A4A4"
                if administrador.hay_sesiones(actividad, fecha):
                    fg_color = '#c3f7c8'
                    hover_color = '#e3fae3'
                columna.actualizar_colores(fg_color, hover_color)

    def dias_semana(self):
        '''Devuelve una lista con los días de lunes a sábado de la próxima semana'''
        hoy = datetime.now()
        proximo_lunes = hoy - timedelta(days=hoy.weekday()) + timedelta(days=7)

        # Generar días de lunes a sábado
        dias = [(proximo_lunes + timedelta(days=i)).date() for i in range(6)]
        return dias

    def tiempos_dia(self):
        '''Creo el rango de horas tipo time'''
        horas = [time(hour=h) for h in range(6, 20)]

        return horas
