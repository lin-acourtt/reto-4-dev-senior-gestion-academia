import tkinter as tk
from tkinter import ttk, messagebox

class VistaConsultarMatriculas:
    def __init__(self, root):
        self.root = root
        self.root.title("Consultar Matrículas")
        self.root.geometry("800x600")
        
        # Frame principal
        self.frame_principal = ttk.Frame(self.root, padding="20")
        self.frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        ttk.Label(
            self.frame_principal,
            text="Consultar Matrículas",
            font=("Helvetica", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Filtros de búsqueda
        self.crear_filtros()
        
        # Tabla de matrículas
        self.crear_tabla_matriculas()
        
        # Botones
        self.crear_botones()
        
    def crear_filtros(self):
        frame_filtros = ttk.LabelFrame(self.frame_principal, text="Filtros de búsqueda", padding="10")
        frame_filtros.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Filtro por curso
        ttk.Label(frame_filtros, text="Curso:").grid(row=0, column=0, padx=5)
        self.filtro_curso = ttk.Combobox(frame_filtros, width=30)
        self.filtro_curso.grid(row=0, column=1, padx=5)
        
        # Filtro por estudiante
        ttk.Label(frame_filtros, text="Estudiante:").grid(row=0, column=2, padx=5)
        self.filtro_estudiante = ttk.Combobox(frame_filtros, width=30)
        self.filtro_estudiante.grid(row=0, column=3, padx=5)
        
        # Botón de búsqueda
        ttk.Button(
            frame_filtros,
            text="Buscar",
            command=self.buscar_matriculas,
            style="Accent.TButton"
        ).grid(row=0, column=4, padx=5)
        
    def crear_tabla_matriculas(self):
        # Frame para la tabla
        frame_tabla = ttk.Frame(self.frame_principal)
        frame_tabla.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear Treeview
        columnas = ("id", "estudiante", "curso", "fecha_matricula", "profesor")
        self.tabla_matriculas = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        # Definir encabezados
        self.tabla_matriculas.heading("id", text="ID")
        self.tabla_matriculas.heading("estudiante", text="Estudiante")
        self.tabla_matriculas.heading("curso", text="Curso")
        self.tabla_matriculas.heading("fecha_matricula", text="Fecha de Matrícula")
        self.tabla_matriculas.heading("profesor", text="Profesor")
        
        # Configurar columnas
        self.tabla_matriculas.column("id", width=50)
        self.tabla_matriculas.column("estudiante", width=200)
        self.tabla_matriculas.column("curso", width=200)
        self.tabla_matriculas.column("fecha_matricula", width=150)
        self.tabla_matriculas.column("profesor", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tabla_matriculas.yview)
        self.tabla_matriculas.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar elementos
        self.tabla_matriculas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
    def crear_botones(self):
        frame_botones = ttk.Frame(self.frame_principal)
        frame_botones.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            frame_botones,
            text="Actualizar",
            command=self.actualizar_lista,
            style="Accent.TButton"
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            frame_botones,
            text="Cerrar",
            command=self.root.destroy,
            style="Danger.TButton"
        ).grid(row=0, column=1, padx=5)
        
    def buscar_matriculas(self):
        # Aquí irá la lógica para buscar matrículas
        messagebox.showinfo("Búsqueda", "Buscando matrículas...")
        
    def actualizar_lista(self):
        # Aquí irá la lógica para actualizar la lista de matrículas
        messagebox.showinfo("Actualización", "Lista de matrículas actualizada")

if __name__ == "__main__":
    root = tk.Tk()
    app = VistaConsultarMatriculas(root)
    root.mainloop() 