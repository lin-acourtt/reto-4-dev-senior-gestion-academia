import customtkinter as ctk
from tkinter import ttk, messagebox
from config.appearance import centrar_ventana
from config.database import Database

from .vista_crear_curso import VistaCrearCurso
from .vista_listar_cursos import VistaListarCursos
from .vista_matricular_estudiante import VistaMatricularEstudiante
from .vista_consultar_matriculas import VistaConsultarMatriculas
from .vista_consultar_horarios import VistaConsultarHorarios
from .vista_eliminar_matricula import VistaEliminarMatricula

class VistaMenuCurso:
    def __init__(self, db: Database = None, tema_actual: str = "System"):
        self.db = db
        self.tema_actual = tema_actual
        self.root = ctk.CTk()
        
    def iniciar_ventana(self):
        """Inicializa la ventana del menú de cursos"""
        self.root.title("Gestión de Cursos - Academia")
        self.root.geometry("800x600")
        
        # Configurar el tema
        ctk.set_appearance_mode(self.tema_actual)
        centrar_ventana(self.root)
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            self.frame_principal,
            text="Gestión de Cursos",
            font=("Helvetica", 24, "bold")
        ).pack(pady=20)
        
        # Frame para los botones
        frame_botones = ctk.CTkFrame(self.frame_principal)
        frame_botones.pack(pady=20)
        
        # Botones del menú
        botones = [
            ("Crear Nuevo Curso", self.abrir_crear_curso),
            ("Listar Cursos", self.abrir_listar_cursos),
            ("Matricular Estudiante", self.abrir_matricular_estudiante),
            ("Consultar Matrículas", self.abrir_consultar_matriculas),
            ("Consultar Horarios", self.abrir_consultar_horarios),
            ("Eliminar Matrícula", self.abrir_eliminar_matricula)
        ]
        
        for texto, comando in botones:
            ctk.CTkButton(
                frame_botones,
                text=texto,
                command=comando,
                width=300,
                height=40,
                corner_radius=10
            ).pack(pady=10, padx=20)
            
        # Botón de salir
        ctk.CTkButton(
            frame_botones,
            text="Volver al Menú Principal",
            command=self.volver_menu_principal,
            width=300,
            height=40,
            corner_radius=10,
            fg_color="#FF5555",
            hover_color="#FF3333"
        ).pack(pady=20, padx=20)
        
        self.root.mainloop()
        
    def abrir_crear_curso(self):
        """Abre la ventana para crear un nuevo curso"""
        ventana_crear = ctk.CTkToplevel(self.root)
        VistaCrearCurso(ventana_crear)
        
    def abrir_listar_cursos(self):
        """Abre la ventana para listar los cursos"""
        ventana_listar = ctk.CTkToplevel(self.root)
        VistaListarCursos(ventana_listar)
        
    def abrir_matricular_estudiante(self):
        """Abre la ventana para matricular un estudiante en un curso"""
        ventana_matricular = ctk.CTkToplevel(self.root)
        VistaMatricularEstudiante(ventana_matricular)
        
    def abrir_consultar_matriculas(self):
        """Abre la ventana para consultar las matrículas"""
        ventana_consultar = ctk.CTkToplevel(self.root)
        VistaConsultarMatriculas(ventana_consultar)
        
    def abrir_consultar_horarios(self):
        """Abre la ventana para consultar los horarios de los cursos"""
        ventana_horarios = ctk.CTkToplevel(self.root)
        VistaConsultarHorarios(ventana_horarios)
        
    def abrir_eliminar_matricula(self):
        """Abre la ventana para eliminar una matrícula"""
        ventana_eliminar = ctk.CTkToplevel(self.root)
        VistaEliminarMatricula(ventana_eliminar)
        
    def volver_menu_principal(self):
        """Cierra la ventana actual y vuelve al menú principal"""
        self.root.destroy()

if __name__ == "__main__":
    app = VistaMenuCurso()
    app.iniciar_ventana()
