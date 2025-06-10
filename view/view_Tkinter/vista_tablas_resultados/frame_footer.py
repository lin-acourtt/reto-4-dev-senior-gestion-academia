import customtkinter as ctk
from customtkinter import CTkFrame
from tkinter.constants import DISABLED, NORMAL 

# Menú Estudiantes
class FrameFooter(CTkFrame):
    def __init__(self, master):
        """
        Al crear este frame, se debe especificar el parent, que debería ser 'VentanaTablaResultados',
        """
        super().__init__(master)

        ctk.CTkButton(
            self,
            text="Ok",
            command=self.master.destroy,
            width=200,
            height=40,
            corner_radius=10
        ).pack(padx=10, expand=True)
        #).grid(row=0,column=0, padx=5, pady=5)
