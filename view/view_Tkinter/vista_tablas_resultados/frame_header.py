import customtkinter as ctk
from customtkinter import CTkFrame

# Ventana Resultados
class FrameHeader(CTkFrame):
    def __init__(self, master_header):
        """
        Al crear este frame, se debe especificar el parent, que debería ser 'VentanaTablaResultados',
        """
        super().__init__(master_header)
        self.master_header = master_header

        # Título dentro de la ventana
        self.label_titulo = ctk.CTkLabel(
            self,
            text=f"{self.master_header.elemento_tabla_pl.capitalize()} de {self.master_header.elemento_owner}: {self.master_header.nombre_elemento_owner}",
            font=("Helvetica", 18, "bold")
        )
        self.label_titulo.pack(pady=5)
