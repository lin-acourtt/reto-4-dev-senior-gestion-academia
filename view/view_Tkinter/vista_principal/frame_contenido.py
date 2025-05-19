import customtkinter as ctk
from customtkinter import CTkFrame
from .frame_botones import FrameBotones

class FrameContenido(CTkFrame):
    def __init__(self, master, botones):
        """
        Al crear este frame, se debe especificar el parent, que debería ser 'FramePrincipal',
        """
        super().__init__(master)

        # Crear grid de botones
        for i, (texto, descripcion, comando) in enumerate(botones):
            frame_boton = ctk.CTkFrame(self)
            frame_boton.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            
            btn = ctk.CTkButton(
                frame_boton,
                text=texto,
                command=comando,
                height=100,
                font=("Helvetica", 16, "bold")
            )
            btn.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Agregar descripción
            label_desc = ctk.CTkLabel(
                frame_boton,
                text=descripcion,
                font=("Helvetica", 12)
            )
            label_desc.pack(pady=(0, 5))

        # Configurar el grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)