import customtkinter as ctk
from customtkinter import CTkFrame
from .frame_superior import FrameSuperior
from .frame_contenido import FrameContenido

class FramePrincipal(CTkFrame):
    def __init__(self, master):
        """
        Al crear este frame, se debe especificar el parent como la ventana principal
        """
        super().__init__(master)

        # Creación del frame superior
        self.frame_superior = FrameSuperior(self)
        self.frame_superior.pack(fill="x", padx=10, pady=10)

        # Creación del frame de contenido
        botones = [
            ("👥 Estudiantes", "Gestionar estudiantes", master.abrir_ventana_estudiantes),
            ("👨‍🏫 Docentes", "Gestionar docentes", master.abrir_ventana_docentes),
            ("📚 Cursos", "Gestionar cursos", master.abrir_ventana_cursos),
            ("⏰ Horarios", "Gestionar horarios", master.abrir_ventana_horarios),
            ("📝 Matrículas", "Gestionar matrículas", master.abrir_ventana_matriculas),
            # ("📊 Estadísticas", "Ver estadísticas", self.mostrar_estadisticas)
        ]
        
        self.frame_contenido = FrameContenido(self, botones)
        self.frame_contenido.pack(fill="both", expand=True, padx=10, pady=10)