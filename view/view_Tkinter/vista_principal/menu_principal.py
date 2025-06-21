import sys
import customtkinter as ctk
#from PIL import Image, ImageTk

from config.database import Database
from config.appearance import centrar_ventana

from .frame_principal import FramePrincipal

from view.view_Tkinter.vista_estudiante.menu_estudiante import VentanaMenuEstudiante
from view.view_Tkinter.vista_profesor.menu_profesor import VentanaMenuProfesor
from view.view_Tkinter.vista_curso.menu_curso import VentanaMenuCurso
from view.view_Tkinter.vista_horario.menu_horario import VentanaMenuHorario
from view.view_Tkinter.vista_matricula.menu_matricula import VentanaMenuMatricula
#from view.view_Tkinter.vista_matricula.vista_menu_matricula import VistaMenuMatricula
from view.view_Tkinter.vista_msgbox.msgbox_library import CTkMessagebox

# Crear la clase de la ventana principial
# desde la cual se podrá hacer la gestión académica 

class VentanaMenuPrincipal(ctk.CTk):
    """
        Ventana CTk con el menú principal para acceder a los submenús. 
    """

    def __init__(self, db: Database = None):
        """
            Constructor, requiere de:
            - db: Base de datos, objeto tipo Database
        """
        super().__init__()
        # El método constructor asegura que el atributo "db" sea de tipo "Database""
        self.db = db

    def iniciar_ventana(self, tema_actual="System"):   
        """
            Inicializa la ventana del menú principal
        """ 
        self.title("Sistema de Gestión Académica - Dev Senior - Reto 4 - 'Lindsey - Santiago' ")
        
        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)
        self.tema_actual = tema_actual
        centrar_ventana(self)
        
        # Configuración de restricciones de la ventana
        self.resizable(True, True)

        # Crear el frame principal - Contiene FrameSuperior y FrameContenido
        self.frame_principal = FramePrincipal(self)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        # Ejecuta la función "salir_programa", para cerrar la aplicación de modo seguro
        self.protocol("WM_DELETE_WINDOW",self.salir_programa)

        self.mainloop()


    def abrir_ventana_estudiantes(self):
        """
            Abre la ventana para operaciones con estudiantes.
            Para esto, se cierra el menú principal.
        """
        self.destroy()
        self.ventana_menu_estudiantes = VentanaMenuEstudiante(self.db)
        self.ventana_menu_estudiantes.iniciar_ventana(self.tema_actual)
        

    def abrir_ventana_profesores(self):
        """
            Abre la ventana para operaciones con docentes.
            Para esto, se cierra el menú principal.
        """
        self.destroy()
        ventana_menu_profesores = VentanaMenuProfesor(db=self.db)
        ventana_menu_profesores.iniciar_ventana(self.tema_actual)

    def abrir_ventana_cursos(self):
        """Abre la ventana para operaciones con cursos"""
        self.destroy()
        ventana_cursos = VentanaMenuCurso(db=self.db)
        ventana_cursos.iniciar_ventana(self.tema_actual)
        
        
    def abrir_ventana_horarios(self):
        """Abre la ventana para operaciones con horarios"""
        self.destroy()
        ventana_horarios = VentanaMenuHorario(db=self.db)
        ventana_horarios.iniciar_ventana(self.tema_actual)
  

    def abrir_ventana_matriculas(self):
        """Abre la ventana para operaciones con matrículas"""
        self.destroy()
        ventana_matriculas = VentanaMenuMatricula(db=self.db)
        ventana_matriculas.iniciar_ventana(self.tema_actual)

        #VistaMenuMatricula(self, self.db, self.tema_actual)
        
    def cambiar_tema(self):
        """
            Método para cambiar el estilo de la ventana
        """
        if self.tema_actual == "Light":
            ctk.set_appearance_mode("Dark")
            self.tema_actual = "Dark"
            self.frame_principal.frame_superior.frame_botones.btn_cambiar_tema.configure(text="☀️ Cambiar Tema")
        else:
            ctk.set_appearance_mode("Light")
            self.tema_actual = "Light"
            self.frame_principal.frame_superior.frame_botones.btn_cambiar_tema.configure(text="🌙 Cambiar Tema")

    def salir_programa(self):
        """
            Método para cerrar el programa de manera segura
        """
        try:
            # Mensaje de confirmación antes de cerrar
            msg = CTkMessagebox(title="¿Salir?", message="¿Está seguro que desea cerrar la aplicación?", icon="question", option_1="Cancelar", option_2="No", option_3="Sí")
            response = msg.get()
            if response != "Sí":
                return
            print("cerrando")
            self.quit()
            self.destroy()
            if self.db:
                self.db.close()
            # Destruir la ventana principal
            sys.exit(0)
        except Exception as e:
            #print(f"Error al cerrar el programa: {e}")
            # Forzar el cierre si hay algún error
            self.quit()
            sys.exit(1)

