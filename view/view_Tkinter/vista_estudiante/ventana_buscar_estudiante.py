import customtkinter as ctk
from .msgbox_estudiantes import msg_registro_cancelado, msg_registro_exitoso
from mysql.connector import IntegrityError
from config.appearance import centrar_ventana

class VentanaBuscarEstudiante(ctk.CTk):
    """
        Inicializa la ventana para registrar estudiantes.
    """
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.id_buscado = ctk.CTkInputDialog(text="ID:", title="Escriba ID a buscar")
        centrar_ventana(self.id_buscado,0.3,0.2)
        if self.id_buscado.get_input():
            print(type(5))
        else:
            print("Ninguno")
    
    def mostrar_detalles_estudiante(self):
        pass


