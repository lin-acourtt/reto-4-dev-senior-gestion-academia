import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.matricula_controller import MatriculaController
from config.appearance import centrar_ventana

class VistaConsultarEstudiantesCurso:
    def __init__(self, root, db, curso_id=None, nombre_curso=None):
        """
        Inicializa la vista para consultar estudiantes inscritos en un curso
        Args:
            root: Ventana principal
            db: Conexión a la base de datos
            curso_id: ID del curso seleccionado
            nombre_curso: Nombre del curso seleccionado
        """
        self.root = root
        self.db = db
        self.curso_id = curso_id
        self.nombre_curso = nombre_curso
        self.controlador_matricula = MatriculaController(self.db)
        
        # Configurar la ventana
        self.root.title(f"Estudiantes Inscritos - {self.nombre_curso}")
        self.root.geometry("800x600")
        centrar_ventana(self.root)
        
        # Crear widgets
        self.crear_widgets()
        
        # Cargar datos
        self.cargar_estudiantes()
        
    def crear_widgets(self):
        """Crea los widgets de la interfaz"""
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        self.label_titulo = ctk.CTkLabel(
            self.frame_principal,
            text=f"Estudiantes Inscritos en: {self.nombre_curso}",
            font=("Roboto", 16, "bold")
        )
        self.label_titulo.pack(pady=10)
        
        # Frame para la tabla
        self.frame_tabla = ctk.CTkFrame(self.frame_principal)
        self.frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tabla de estudiantes
        self.tabla_estudiantes = ttk.Treeview(
            self.frame_tabla,
            columns=("ID", "Nombre", "Apellido", "Fecha Matrícula"),
            show="headings",
            height=15
        )
        
        # Configurar columnas
        self.tabla_estudiantes.heading("ID", text="ID")
        self.tabla_estudiantes.heading("Nombre", text="Nombre")
        self.tabla_estudiantes.heading("Apellido", text="Apellido")
        self.tabla_estudiantes.heading("Fecha Matrícula", text="Fecha Matrícula")
        
        self.tabla_estudiantes.column("ID", width=50, anchor="center")
        self.tabla_estudiantes.column("Nombre", width=200)
        self.tabla_estudiantes.column("Apellido", width=200)
        self.tabla_estudiantes.column("Fecha Matrícula", width=150, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.frame_tabla,
            orient="vertical",
            command=self.tabla_estudiantes.yview
        )
        self.tabla_estudiantes.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar tabla y scrollbar
        self.tabla_estudiantes.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón cerrar
        self.btn_cerrar = ctk.CTkButton(
            self.frame_principal,
            text="Cerrar",
            command=self.root.destroy
        )
        self.btn_cerrar.pack(pady=10)
        
    def cargar_estudiantes(self):
        """Carga los estudiantes inscritos en el curso"""
        try:
            # Limpiar tabla
            for item in self.tabla_estudiantes.get_children():
                self.tabla_estudiantes.delete(item)
            
            # Obtener estudiantes inscritos usando el ID del curso
            matriculas = self.controlador_matricula.buscar_matriculas(id_curso=self.curso_id)
            
            if not matriculas:
                messagebox.showinfo(
                    "Información",
                    "No hay estudiantes inscritos en este curso"
                )
                return
            
            # Insertar en la tabla
            for matricula in matriculas:
                self.tabla_estudiantes.insert(
                    "",
                    "end",
                    values=(
                        matricula.estudiante.id_estudiante,
                        matricula.estudiante.nombre,
                        matricula.estudiante.apellido,
                        matricula.fecha_matricula.strftime("%d/%m/%Y") if matricula.fecha_matricula else "No especificada"
                    )
                )
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al cargar los estudiantes: {str(e)}"
            )
            print(f"Error detallado: {str(e)}")  # Para depuración 