import customtkinter as ctk
from customtkinter import CTkFrame
from .frame_botones_header import FrameBotonesHeader

# Menú Horarios
class FrameHeader(CTkFrame):
    def __init__(self, master_header):
        """
        Al crear este frame, se debe especificar el parent, que debería ser 'VentanaMenuHorario',
        """
        super().__init__(master_header)
        self.master_header = master_header

        # Título con estilo moderno
        self.titulo = ctk.CTkLabel(
            self, 
            text="Gestión de Horarios", 
            font=("Helvetica", 24, "bold")
        )
        self.titulo.pack(side="left", padx=20)

        # Frame para los botones
        self.frame_botones_header = FrameBotonesHeader(self)
        self.frame_botones_header.pack(side="right", padx=10, pady=10)