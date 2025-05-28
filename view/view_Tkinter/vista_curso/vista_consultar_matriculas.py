import customtkinter as ctk
from tkinter import ttk, messagebox
from config.appearance import centrar_ventana
from controllers.matricula_controller import MatriculaController

class VistaConsultarMatriculas:
    def __init__(self, root, db=None):
        self.root = root
        self.db = db
        self.controlador_matricula = MatriculaController(self.db)
        
        # Configurar la ventana
        self.root.title("Consultar Matrículas")
        self.root.geometry("800x600")
        centrar_ventana(self.root)
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            self.frame_principal,
            text="Consultar Matrículas",
            font=("Helvetica", 24, "bold")
        ).pack(pady=20)
        
        # Filtros de búsqueda
        self.crear_filtros()
        
        # Tabla de matrículas
        self.crear_tabla_matriculas()
        
        # Botones
        self.crear_botones()
        
        # Cargar datos iniciales
        self.cargar_matriculas()
        
    def crear_filtros(self):
        # Frame para los filtros
        frame_filtros = ctk.CTkFrame(self.frame_principal)
        frame_filtros.pack(fill="x", padx=20, pady=10)
        
        # Título de la sección
        ctk.CTkLabel(
            frame_filtros,
            text="Filtros de búsqueda",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
        
        # Frame para los campos de filtro
        frame_campos = ctk.CTkFrame(frame_filtros)
        frame_campos.pack(fill="x", padx=20, pady=10)
        
        # Filtro por curso
        ctk.CTkLabel(frame_campos, text="Curso:").pack(side="left", padx=5)
        self.filtro_curso = ctk.CTkComboBox(frame_campos, width=200)
        self.filtro_curso.pack(side="left", padx=5)
        
        # Filtro por estudiante
        ctk.CTkLabel(frame_campos, text="Estudiante:").pack(side="left", padx=5)
        self.filtro_estudiante = ctk.CTkComboBox(frame_campos, width=200)
        self.filtro_estudiante.pack(side="left", padx=5)
        
        # Botón de búsqueda
        ctk.CTkButton(
            frame_campos,
            text="Buscar",
            command=self.buscar_matriculas,
            width=100,
            height=30,
            corner_radius=10
        ).pack(side="left", padx=5)
        
    def crear_tabla_matriculas(self):
        # Frame para la tabla
        frame_tabla = ctk.CTkFrame(self.frame_principal)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear Treeview
        columnas = ("id", "estudiante", "curso", "fecha_matricula", "profesor")
        self.tabla_matriculas = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        
        # Definir encabezados
        self.tabla_matriculas.heading("id", text="ID")
        self.tabla_matriculas.heading("estudiante", text="Estudiante")
        self.tabla_matriculas.heading("curso", text="Curso")
        self.tabla_matriculas.heading("fecha_matricula", text="Fecha de Matrícula")
        self.tabla_matriculas.heading("profesor", text="Profesor")
        
        # Configurar columnas
        self.tabla_matriculas.column("id", width=50, anchor="center")
        self.tabla_matriculas.column("estudiante", width=200)
        self.tabla_matriculas.column("curso", width=200)
        self.tabla_matriculas.column("fecha_matricula", width=150)
        self.tabla_matriculas.column("profesor", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_matriculas.yview)
        self.tabla_matriculas.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar elementos
        self.tabla_matriculas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def crear_botones(self):
        frame_botones = ctk.CTkFrame(self.frame_principal)
        frame_botones.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            frame_botones,
            text="Actualizar",
            command=self.cargar_matriculas,
            width=200,
            height=40,
            corner_radius=10
        ).pack(side="left", padx=10, expand=True)
        
        ctk.CTkButton(
            frame_botones,
            text="Cerrar",
            command=self.root.destroy,
            width=200,
            height=40,
            corner_radius=10,
            fg_color="#FF5555",
            hover_color="#FF3333"
        ).pack(side="right", padx=10, expand=True)
        
    def cargar_matriculas(self):
        """Carga todas las matrículas en la tabla"""
        try:
            # Limpiar tabla
            for item in self.tabla_matriculas.get_children():
                self.tabla_matriculas.delete(item)
                
            # Obtener matrículas de la base de datos
            matriculas = self.controlador_matricula.listar_matriculas()
            
            # Insertar cada matrícula en la tabla
            for matricula in matriculas:
                self.tabla_matriculas.insert(
                    "",
                    "end",
                    values=(
                        matricula.id_matricula,
                        f"{matricula.estudiante.nombre} {matricula.estudiante.apellido}",
                        matricula.curso.nombre,
                        matricula.fecha_matricula,
                        matricula.curso.profesor
                    )
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar matrículas: {str(e)}")
            
    def buscar_matriculas(self):
        """Busca matrículas según los filtros seleccionados"""
        try:
            # Obtener valores de los filtros
            curso = self.filtro_curso.get()
            estudiante = self.filtro_estudiante.get()
            
            # Limpiar tabla
            for item in self.tabla_matriculas.get_children():
                self.tabla_matriculas.delete(item)
                
            # Buscar matrículas según los filtros
            matriculas = self.controlador_matricula.buscar_matriculas(
                nombre_curso=curso if curso else None,
                nombre_estudiante=estudiante if estudiante else None
            )
            
            # Insertar resultados en la tabla
            for matricula in matriculas:
                self.tabla_matriculas.insert(
                    "",
                    "end",
                    values=(
                        matricula.id_matricula,
                        f"{matricula.estudiante.nombre} {matricula.estudiante.apellido}",
                        matricula.curso.nombre,
                        matricula.fecha_matricula,
                        matricula.curso.profesor
                    )
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar matrículas: {str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = VistaConsultarMatriculas(root)
    root.mainloop() 