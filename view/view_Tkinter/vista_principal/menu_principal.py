import customtkinter as ctk
from PIL import Image, ImageTk
import os
# from view.view_Tkinter.viewEstudiante.menuEstudiante import MenuEstudiante
# from view.view_Tkinter.viewDocenteFull.menuDocenteFull import MenuDocenteFull
from controllers.estudiante_controller import EstudianteController
from controllers.profesor_controller import ProfesorController
from controllers.curso_controller import CursoController
from controllers.horario_controller import HorarioController
from controllers.matricula_controller import MatriculaController

from config.database import Database
from config.appearance import centrar_ventana

from .frame_principal import FramePrincipal

from view.view_Tkinter.vista_estudiante.menu_estudiante import VentanaMenuEstudiante

# Crear la clase de la ventana principial
# desde la cual se podrá hacer la gestión académica 

class VentanaMenuPrincipal(ctk.CTk):

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

        self.mainloop()

        # Cargar estadísticas iniciales
        # self.cargar_estadisticas()

    # def cargar_estadisticas(self):
    #     try:
    #         # Crear controladores
    #         estudiante_controller = EstudianteController(self.db)
    #         docente_controller = ProfesorController(self.db)
    #         curso_controller = CursoController(self.db)

    #         # Obtener estadísticas
    #         total_estudiantes = len(estudiante_controller.listar_estudiantes())
    #         total_docentes = len(docente_controller.listar_docentes())
    #         total_cursos = len(curso_controller.listar_cursos())

    #         # Actualizar etiquetas de estadísticas si existen
    #         if hasattr(self, 'label_estadisticas'):
    #             self.label_estadisticas.configure(
    #                 text=f"Estadísticas:\n"
    #                      f"Estudiantes: {total_estudiantes}\n"
    #                      f"Docentes: {total_docentes}\n"
    #                      f"Cursos: {total_cursos}"
    #             )
    #     except Exception as e:
    #         print(f"Error al cargar estadísticas: {e}")

    # def mostrar_estadisticas(self):
    #     # Crear ventana de estadísticas
    #     ventana_stats = ctk.CTkToplevel(self.root)
    #     ventana_stats.title("Estadísticas del Sistema")
    #     ventana_stats.geometry("400x300")
    #     ventana_stats.resizable(False, False)
        
    #     # Configurar el tema
    #     ctk.set_appearance_mode(self.tema_actual)
        
    #     # Frame para las estadísticas
    #     frame_stats = ctk.CTkFrame(ventana_stats)
    #     frame_stats.pack(fill="both", expand=True, padx=20, pady=20)
        
    #     # Título
    #     titulo = ctk.CTkLabel(
    #         frame_stats,
    #         text="Estadísticas del Sistema",
    #         font=("Helvetica", 20, "bold")
    #     )
    #     titulo.pack(pady=10)
        
    #     # Cargar y mostrar estadísticas
    #     try:
    #         estudiante_controller = EstudianteController(self.db)
    #         docente_controller = ProfesorController(self.db)
    #         curso_controller = CursoController(self.db)
            
    #         total_estudiantes = len(estudiante_controller.listar_estudiantes())
    #         total_docentes = len(docente_controller.listar_docentes())
    #         total_cursos = len(curso_controller.listar_cursos())
            
    #         # Mostrar estadísticas con iconos
    #         stats_text = f"""
    #         👥 Total de Estudiantes: {total_estudiantes}
    #         👨‍🏫 Total de Docentes: {total_docentes}
    #         📚 Total de Cursos: {total_cursos}
    #         """
            
    #         label_stats = ctk.CTkLabel(
    #             frame_stats,
    #             text=stats_text,
    #             font=("Helvetica", 16),
    #             justify="left"
    #         )
    #         label_stats.pack(pady=20)
            
    #     except Exception as e:
    #         label_error = ctk.CTkLabel(
    #             frame_stats,
    #             text=f"Error al cargar estadísticas: {str(e)}",
    #             text_color="red"
    #         )
    #         label_error.pack(pady=20)
        
    #     # Botón para cerrar
    #     btn_cerrar = ctk.CTkButton(
    #         frame_stats,
    #         text="Cerrar",
    #         command=ventana_stats.destroy
    #     )
    #     btn_cerrar.pack(pady=10)

    def abrir_ventana_estudiantes(self):
        """
            Abre la ventana para operaciones con estudiantes.
            Para esto, se cierra el menú principal.
        """
        self.destroy()
        self.ventana_menu_estudiantes = VentanaMenuEstudiante(self.db)
        self.ventana_menu_estudiantes.iniciar_ventana(self.tema_actual)
        

    def abrir_ventana_docentes(self):
        # self.root.destroy()
        # menu_docente = MenuDocenteFull(db=self.db, tema_actual=self.tema_actual)
        # menu_docente.root.mainloop()
        print("Ventana docentes")
        

    def abrir_ventana_cursos(self):
        print("Ventana cursos")

    def abrir_ventana_horarios(self):
        print("Ventana horarios")

    def abrir_ventana_matriculas(self):
        print("Ventana matrículas")
    
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
            # Cerrar la conexión a la base de datos si existe
            self.destroy()
            if self.db:
                self.db.close()
            # Destruir la ventana principal
            
        except Exception as e:
            print(f"Error al cerrar el programa: {e}")
            # Forzar el cierre si hay algún error
            self.quit()

