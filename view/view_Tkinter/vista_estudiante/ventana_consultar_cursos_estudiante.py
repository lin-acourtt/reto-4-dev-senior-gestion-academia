import customtkinter as ctk
from tkinter import ttk, messagebox
from config.appearance import centrar_ventana
from controllers.matricula_controller import MatriculaController

class VistaConsultarCursosEstudiante:
    def __init__(self, root, db=None, estudiante_id=None, nombre_estudiante=None):
        self.root = root
        self.db = db
        self.estudiante_id = estudiante_id
        self.nombre_estudiante = nombre_estudiante
        self.controlador_matricula = MatriculaController(self.db)
        
        # Configurar la ventana
        self.root.title("Cursos del Estudiante")
        self.root.geometry("1000x600")
        centrar_ventana(self.root)
        self.root.resizable(True, True)
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        self.label_titulo = ctk.CTkLabel(
            self.frame_principal,
            text=f"Cursos de {self.nombre_estudiante}",
            font=("Helvetica", 24, "bold")
        )
        self.label_titulo.pack(pady=20)
        
        # Tabla de cursos
        self.crear_tabla_cursos()
        
        # Botones
        self.crear_botones()
        
        # Cargar cursos del estudiante
        self.cargar_cursos()
        
    def crear_tabla_cursos(self):
        # Frame para la tabla
        frame_tabla = ctk.CTkFrame(self.frame_principal)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear Treeview
        columnas = ("id", "curso", "profesor", "descripcion", "duracion", "horarios")
        self.tabla_cursos = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        
        # Definir encabezados
        self.tabla_cursos.heading("id", text="ID")
        self.tabla_cursos.heading("curso", text="Curso")
        self.tabla_cursos.heading("profesor", text="Profesor")
        self.tabla_cursos.heading("descripcion", text="Descripción")
        self.tabla_cursos.heading("duracion", text="Duración (hrs)")
        self.tabla_cursos.heading("horarios", text="Horarios")
        
        # Configurar columnas
        self.tabla_cursos.column("id", width=50, anchor="center")
        self.tabla_cursos.column("curso", width=200)
        self.tabla_cursos.column("profesor", width=200)
        self.tabla_cursos.column("descripcion", width=200)
        self.tabla_cursos.column("duracion", width=100, anchor="center")
        self.tabla_cursos.column("horarios", width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_cursos.yview)
        self.tabla_cursos.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar elementos
        self.tabla_cursos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def crear_botones(self):
        frame_botones = ctk.CTkFrame(self.frame_principal)
        frame_botones.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            frame_botones,
            text="Actualizar",
            command=self.cargar_cursos,
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
        
    def cargar_cursos(self):
        """Carga los cursos del estudiante en la tabla"""
        try:
            if not self.estudiante_id:
                messagebox.showerror("Error", "No se ha seleccionado ningún estudiante")
                self.root.destroy()
                return
                
            # Limpiar tabla
            for item in self.tabla_cursos.get_children():
                self.tabla_cursos.delete(item)
                
            # Obtener cursos del estudiante
            cursos = self.controlador_matricula.obtener_cursos_por_estudiante(self.estudiante_id)
            
            if not cursos:
                messagebox.showinfo("Información", "Este estudiante no está inscrito en ningún curso")
                return
            
            # Insertar cada curso en la tabla
            for curso in cursos:
                self.tabla_cursos.insert(
                    "",
                    "end",
                    values=(
                        curso['id_curso'],
                        curso['nombre'],
                        curso['profesor'],
                        curso['descripcion'],
                        curso['duracion_horas'],
                        curso['horarios']
                    )
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar cursos: {str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = VistaConsultarCursosEstudiante(root)
    root.mainloop() 