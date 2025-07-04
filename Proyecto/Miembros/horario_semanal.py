''' Crea el horario semanal para mostrar los horarios '''
from datetime import time
from customtkinter import CTkFrame, CTkLabel

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

        self.celdas = []  # ← Lista de celdas: [ [(0,0), (0,1), ...], [(1,0), ...] ]

        self.crear_cabecera()
        self.crear_horario()

    def crear_cabecera(self):
        '''Crea la cabecera con los dias de la semana'''
        fuente_dias = ("Segoe UI", max(24,int(self.winfo_screenwidth() * 0.015)))
        dias = ["", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        for col, dia in enumerate(dias):
            label = CTkLabel(self, text=dia, font=fuente_dias,text_color='white')
            label.grid(row=0, column=col, sticky="nsew", padx=10, pady=10)
            self.dias.append(label)

    def crear_horario(self):
        '''Crea el resto del horario inclullendo los bloques horarios'''
        fuente_horas = ("Segoe UI", max(15,int(self.winfo_screenwidth() * 0.01)))
        for fila, hora in enumerate(self.horas, start=1):
            fila_celdas = []

            # Columna 0 (horarios)
            hora_label = CTkLabel(self, text=hora, font=fuente_horas, anchor='w', text_color='white')
            hora_label.grid(row=fila, column=0, sticky="nsew", padx=(4,5), pady=3)

            # Celdas de Lunes a Sábado
            for col in range(1, 7):
                celda = CTkLabel(self, fg_color="#f0f0f0", text='', corner_radius=3)
                celda.grid(row=fila, column=col, sticky="nsew", padx=3, pady=3)
                fila_celdas.append(celda)

            self.celdas.append(fila_celdas)
