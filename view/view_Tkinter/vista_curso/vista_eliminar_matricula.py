import customtkinter as ctk
from tkinter import ttk, messagebox
from config.appearance import centrar_ventana
from controllers.matricula_controller import MatriculaController

class VistaEliminarMatricula:
    def __init__(self, root, db=None):
        self.root = root
        self.db = db
        self.controlador_matricula = MatriculaController(self.db)
        
        # Configurar la ventana
        self.root.title("Eliminar Matrícula")
        self.root.geometry("800x600")
        centrar_ventana(self.root)
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            self.frame_principal,
            text="Eliminar Matrícula",
            font=("Helvetica", 24, "bold")
        ).pack(pady=20)
        
        # Campos de búsqueda
        self.crear_campos_busqueda()
        
        # Tabla de matrículas
        self.crear_tabla_matriculas()
        
        # Botones
        self.crear_botones()
        
        # Cargar datos iniciales
        self.cargar_matriculas()
        
    def crear_campos_busqueda(self):
        # Frame para los campos de búsqueda
        frame_busqueda = ctk.CTkFrame(self.frame_principal)
        frame_busqueda.pack(fill="x", padx=20, pady=10)
        
        # Título de la sección
        ctk.CTkLabel(
            frame_busqueda,
            text="Buscar Matrícula",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
        
        # Frame para los campos
        frame_campos = ctk.CTkFrame(frame_busqueda)
        frame_campos.pack(fill="x", padx=20, pady=10)
        
        # Búsqueda por estudiante
        ctk.CTkLabel(frame_campos, text="Estudiante:").pack(side="left", padx=5)
        self.busqueda_estudiante = ctk.CTkComboBox(frame_campos, width=200)
        self.busqueda_estudiante.pack(side="left", padx=5)
        
        # Búsqueda por curso
        ctk.CTkLabel(frame_campos, text="Curso:").pack(side="left", padx=5)
        self.busqueda_curso = ctk.CTkComboBox(frame_campos, width=200)
        self.busqueda_curso.pack(side="left", padx=5)
        
        # Botón de búsqueda
        ctk.CTkButton(
            frame_campos,
            text="Buscar",
            command=self.buscar_matricula,
            width=100,
            height=30,
            corner_radius=10
        ).pack(side="left", padx=5)
        
    def crear_tabla_matriculas(self):
        # Frame para la tabla
        frame_tabla = ctk.CTkFrame(self.frame_principal)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear Treeview
        columnas = ("id", "estudiante", "curso", "fecha_matricula")
        self.tabla_matriculas = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        
        # Definir encabezados
        self.tabla_matriculas.heading("id", text="ID")
        self.tabla_matriculas.heading("estudiante", text="Estudiante")
        self.tabla_matriculas.heading("curso", text="Curso")
        self.tabla_matriculas.heading("fecha_matricula", text="Fecha de Matrícula")
        
        # Configurar columnas
        self.tabla_matriculas.column("id", width=50, anchor="center")
        self.tabla_matriculas.column("estudiante", width=250)
        self.tabla_matriculas.column("curso", width=250)
        self.tabla_matriculas.column("fecha_matricula", width=150)
        
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
            text="Eliminar Seleccionada",
            command=self.eliminar_matricula_seleccionada,
            width=200,
            height=40,
            corner_radius=10,
            fg_color="#FF5555",
            hover_color="#FF3333"
        ).pack(side="left", padx=10, expand=True)
        
        ctk.CTkButton(
            frame_botones,
            text="Cerrar",
            command=self.root.destroy,
            width=200,
            height=40,
            corner_radius=10
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
                    iid=matricula.id_matricula,
                    values=(
                        matricula.id_matricula,
                        f"{matricula.estudiante.nombre} {matricula.estudiante.apellido}",
                        matricula.curso.nombre,
                        matricula.fecha_matricula
                    )
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar matrículas: {str(e)}")
            
    def buscar_matricula(self):
        """Busca matrículas según los filtros seleccionados"""
        try:
            # Obtener valores de los filtros
            estudiante = self.busqueda_estudiante.get()
            curso = self.busqueda_curso.get()
            
            # Limpiar tabla
            for item in self.tabla_matriculas.get_children():
                self.tabla_matriculas.delete(item)
                
            # Buscar matrículas según los filtros
            matriculas = self.controlador_matricula.buscar_matriculas(
                nombre_estudiante=estudiante if estudiante else None,
                nombre_curso=curso if curso else None
            )
            
            # Insertar resultados en la tabla
            for matricula in matriculas:
                self.tabla_matriculas.insert(
                    "",
                    "end",
                    iid=matricula.id_matricula,
                    values=(
                        matricula.id_matricula,
                        f"{matricula.estudiante.nombre} {matricula.estudiante.apellido}",
                        matricula.curso.nombre,
                        matricula.fecha_matricula
                    )
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar matrículas: {str(e)}")
            
    def eliminar_matricula_seleccionada(self):
        """Elimina la matrícula seleccionada de la tabla"""
        try:
            # Obtener la selección
            seleccion = self.tabla_matriculas.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Por favor, seleccione una matrícula para eliminar")
                return
                
            # Obtener datos de la matrícula seleccionada
            matricula_id = int(seleccion[0])
            estudiante = self.tabla_matriculas.item(seleccion[0])['values'][1]
            curso = self.tabla_matriculas.item(seleccion[0])['values'][2]
            
            # Confirmar eliminación
            if messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar la matrícula del estudiante {estudiante} en el curso {curso}?"
            ):
                # Eliminar la matrícula
                if self.controlador_matricula.eliminar_matricula(matricula_id):
                    messagebox.showinfo("Éxito", "Matrícula eliminada exitosamente")
                    self.cargar_matriculas()  # Recargar la tabla
                else:
                    messagebox.showerror("Error", "No se pudo eliminar la matrícula")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar la matrícula: {str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = VistaEliminarMatricula(root)
    root.mainloop() 