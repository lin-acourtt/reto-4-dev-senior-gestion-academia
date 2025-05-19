import customtkinter as ctk
from customtkinter import CTkFrame

class FrameBotones(CTkFrame):

    def __init__(self, master):
        """
        Al crear este frame, se debe especificar el parent, que debería ser 'FrameTitulo',
        """
        super().__init__(master)

        # Botón de tema con ícono
        self.btn_cambiar_tema = ctk.CTkButton(
            self,
            text="🌓 Cambiar Tema",
            command=master.master.master.cambiar_tema,
            # Master 1: FrameTitulo
            # Master 2: FrameSuperior
            # Master 3: Ventana Principal
            width=120
        )
        self.btn_cambiar_tema.pack(side="left", padx=5)

        # Botón salir del programa
        self.btn_salir = ctk.CTkButton(
            self,
            text="🚪 Salir",
            command=master.master.master.salir_programa,
            width=120,
            fg_color="#FF5555",  # Color rojo para el botón de salir
            hover_color="#FF3333"  # Color rojo más oscuro al pasar el mouse
        )
        self.btn_salir.pack(side="left", padx=5)