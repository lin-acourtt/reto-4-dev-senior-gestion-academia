import customtkinter as ctk
from customtkinter import CTkFrame
from .frame_botones import FrameBotones

class FrameSuperior(CTkFrame):
    def __init__(self, master_frame_superior):
        """
            Al crear este frame, se debe especificar el parent, que debería ser 'FramePrincipal',
            - master_frame_superior
        """
        super().__init__(master_frame_superior)
        self.master_frame_superior = master_frame_superior

        # Título con estilo moderno
        self.titulo = ctk.CTkLabel(
            self, 
            text="Sistema de Gestión Académica", 
            font=("Helvetica", 24, "bold")
        )
        self.titulo.pack(side="left", padx=20)

        # Frame para los botones
        self.frame_botones = FrameBotones(self)
        self.frame_botones.pack(side="right", padx=10)