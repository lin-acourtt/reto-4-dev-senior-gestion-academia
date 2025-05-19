import customtkinter as ctk
from config.database import Database
from config.appearance import centrar_ventana

class VentanaMenuEstudiante(ctk.CTk):

    def __init__(self, db: Database = None):
        super().__init__()
        # El método constructor asegura que el atributo "db" sea de tipo "Database""
        self.db = db

    def iniciar_ventana(self, tema_actual):    
        
        self.title("Gestión de estudiantes")
        
        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)
        self.tema_actual = tema_actual
        centrar_ventana(self, proporcion=0.7)
        
        # Configuración de restricciones de la ventana
        self.resizable(True, True)

        self.mainloop()
