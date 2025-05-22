import customtkinter as ctk
from customtkinter import CTkFrame
from .frame_superior import FrameSuperior
from .frame_contenido import FrameContenido

class FramePrincipal(CTkFrame):
    def __init__(self, master_frame_principal):
        """
            Al crear este frame, se debe especificar el parent como la ventana principal
            - master_frame_principal
        """
        super().__init__(master_frame_principal)
        self.master_frame_principal = master_frame_principal

        # Creación del frame superior - Tiene el título y botones de cambiar el tema y cerrar
        self.frame_superior = FrameSuperior(self)
        self.frame_superior.pack(fill="x", padx=10, pady=10)

        # Creación del frame de contenido - Tiene las operaciones disponibles del menú
        botones = [
            ("👥 Estudiantes", "Gestionar estudiantes", master_frame_principal.abrir_ventana_estudiantes),
            ("👨‍🏫 Docentes", "Gestionar docentes", master_frame_principal.abrir_ventana_docentes),
            ("📚 Cursos", "Gestionar cursos", master_frame_principal.abrir_ventana_cursos),
            ("⏰ Horarios", "Gestionar horarios", master_frame_principal.abrir_ventana_horarios),
            ("📝 Matrículas", "Gestionar matrículas", master_frame_principal.abrir_ventana_matriculas),
            # ("📊 Estadísticas", "Ver estadísticas", self.mostrar_estadisticas)
        ]
        
        self.frame_contenido = FrameContenido(self, botones)
        self.frame_contenido.pack(fill="both", expand=True, padx=10, pady=10)