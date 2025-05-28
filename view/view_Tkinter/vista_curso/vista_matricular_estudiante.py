import customtkinter as ctk
from tkinter import messagebox
from config.appearance import centrar_ventana
from controllers.curso_controller import CursoController
from controllers.estudiante_controller import EstudianteController
from controllers.matricula_controller import MatriculaController

class VistaMatricularEstudiante:
    def __init__(self, root, db=None):
        self.root = root
        self.db = db
        self.controlador_curso = CursoController(self.db)
        self.controlador_estudiante = EstudianteController(self.db)
        self.controlador_matricula = MatriculaController(self.db)
        
        # Configurar la ventana
        self.root.title("Matricular Estudiante")
        self.root.geometry("600x500")
        centrar_ventana(self.root)
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            self.frame_principal,
            text="Matricular Estudiante en Curso",
            font=("Helvetica", 24, "bold")
        ).pack(pady=20)
        
        # Campos del formulario
        self.crear_campos_formulario()
        
        # Botones
        self.crear_botones()
        
    def crear_campos_formulario(self):
        # Frame para los campos
        frame_campos = ctk.CTkFrame(self.frame_principal)
        frame_campos.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Selección de estudiante
        ctk.CTkLabel(frame_campos, text="Estudiante:").pack(pady=(10,5))
        self.estudiante = ctk.CTkComboBox(frame_campos, width=400)
        self.estudiante.pack(pady=(0,10))
        
        # Selección de curso
        ctk.CTkLabel(frame_campos, text="Curso:").pack(pady=(10,5))
        self.curso = ctk.CTkComboBox(frame_campos, width=400)
        self.curso.pack(pady=(0,10))
        
        # Fecha de matrícula
        ctk.CTkLabel(frame_campos, text="Fecha de Matrícula:").pack(pady=(10,5))
        self.fecha_matricula = ctk.CTkEntry(frame_campos, width=400)
        self.fecha_matricula.pack(pady=(0,10))
        
        # Cargar listas de estudiantes y cursos
        self.cargar_estudiantes()
        self.cargar_cursos()
        
    def crear_botones(self):
        frame_botones = ctk.CTkFrame(self.frame_principal)
        frame_botones.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            frame_botones,
            text="Matricular",
            command=self.realizar_matricula,
            width=200,
            height=40,
            corner_radius=10
        ).pack(side="left", padx=10, expand=True)
        
        ctk.CTkButton(
            frame_botones,
            text="Cancelar",
            command=self.root.destroy,
            width=200,
            height=40,
            corner_radius=10,
            fg_color="#FF5555",
            hover_color="#FF3333"
        ).pack(side="right", padx=10, expand=True)
        
    def cargar_estudiantes(self):
        """Carga la lista de estudiantes en el combobox"""
        try:
            # Obtener estudiantes de la base de datos
            estudiantes = self.controlador_estudiante.listar_estudiantes()
            # Formatear nombres para mostrar
            nombres_estudiantes = [f"{e.nombre} {e.apellido}" for e in estudiantes]
            self.estudiante.configure(values=nombres_estudiantes)
            if nombres_estudiantes:
                self.estudiante.set(nombres_estudiantes[0])
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar estudiantes: {str(e)}")
            
    def cargar_cursos(self):
        """Carga la lista de cursos en el combobox"""
        try:
            # Obtener cursos de la base de datos
            cursos = self.controlador_curso.listar_cursos()
            # Formatear nombres para mostrar
            nombres_cursos = [curso.nombre for curso in cursos]
            self.curso.configure(values=nombres_cursos)
            if nombres_cursos:
                self.curso.set(nombres_cursos[0])
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar cursos: {str(e)}")
        
    def realizar_matricula(self):
        """Realiza la matrícula del estudiante en el curso"""
        try:
            # Obtener valores del formulario
            estudiante = self.estudiante.get()
            curso = self.curso.get()
            fecha = self.fecha_matricula.get().strip()
            
            # Validar campos requeridos
            if not estudiante:
                messagebox.showwarning("Advertencia", "Debe seleccionar un estudiante")
                return
                
            if not curso:
                messagebox.showwarning("Advertencia", "Debe seleccionar un curso")
                return
                
            if not fecha:
                messagebox.showwarning("Advertencia", "La fecha de matrícula es obligatoria")
                return
            
            # Obtener IDs de estudiante y curso
            # Aquí deberías obtener los IDs reales de la base de datos
            # Por ahora usaremos IDs de ejemplo
            id_estudiante = 1
            id_curso = 1
            
            # Registrar la matrícula
            if self.controlador_matricula.registrar_matricula(
                id_estudiante=id_estudiante,
                id_curso=id_curso,
                fecha_matricula=fecha
            ):
                messagebox.showinfo("Éxito", "Estudiante matriculado exitosamente")
                self.root.destroy()
            else:
                messagebox.showerror("Error", "No se pudo realizar la matrícula")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al realizar la matrícula: {str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = VistaMatricularEstudiante(root)
    root.mainloop() 