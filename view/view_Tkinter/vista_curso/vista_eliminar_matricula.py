import tkinter as tk
from tkinter import ttk, messagebox

class VistaEliminarMatricula:
    def __init__(self, root):
        self.root = root
        self.root.title("Eliminar Matrícula")
        self.root.geometry("600x400")
        
        # Frame principal
        self.frame_principal = ttk.Frame(self.root, padding="20")
        self.frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        ttk.Label(
            self.frame_principal,
            text="Eliminar Matrícula",
            font=("Helvetica", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Campos de búsqueda
        self.crear_campos_busqueda()
        
        # Tabla de matrículas
        self.crear_tabla_matriculas()
        
        # Botones
        self.crear_botones()
        
    def crear_campos_busqueda(self):
        frame_busqueda = ttk.LabelFrame(self.frame_principal, text="Buscar Matrícula", padding="10")
        frame_busqueda.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Búsqueda por estudiante
        ttk.Label(frame_busqueda, text="Estudiante:").grid(row=0, column=0, padx=5)
        self.busqueda_estudiante = ttk.Combobox(frame_busqueda, width=30)
        self.busqueda_estudiante.grid(row=0, column=1, padx=5)
        
        # Búsqueda por curso
        ttk.Label(frame_busqueda, text="Curso:").grid(row=0, column=2, padx=5)
        self.busqueda_curso = ttk.Combobox(frame_busqueda, width=30)
        self.busqueda_curso.grid(row=0, column=3, padx=5)
        
        # Botón de búsqueda
        ttk.Button(
            frame_busqueda,
            text="Buscar",
            command=self.buscar_matricula,
            style="Accent.TButton"
        ).grid(row=0, column=4, padx=5)
        
    def crear_tabla_matriculas(self):
        # Frame para la tabla
        frame_tabla = ttk.Frame(self.frame_principal)
        frame_tabla.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear Treeview
        columnas = ("id", "estudiante", "curso", "fecha_matricula")
        self.tabla_matriculas = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        # Definir encabezados
        self.tabla_matriculas.heading("id", text="ID")
        self.tabla_matriculas.heading("estudiante", text="Estudiante")
        self.tabla_matriculas.heading("curso", text="Curso")
        self.tabla_matriculas.heading("fecha_matricula", text="Fecha de Matrícula")
        
        # Configurar columnas
        self.tabla_matriculas.column("id", width=50)
        self.tabla_matriculas.column("estudiante", width=200)
        self.tabla_matriculas.column("curso", width=200)
        self.tabla_matriculas.column("fecha_matricula", width=150)
        
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
            text="Eliminar Seleccionado",
            command=self.eliminar_matricula,
            style="Danger.TButton"
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            frame_botones,
            text="Cancelar",
            command=self.root.destroy,
            style="Accent.TButton"
        ).grid(row=0, column=1, padx=5)
        
    def buscar_matricula(self):
        # Aquí irá la lógica para buscar matrículas
        messagebox.showinfo("Búsqueda", "Buscando matrículas...")
        
    def eliminar_matricula(self):
        # Aquí irá la lógica para eliminar la matrícula seleccionada
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta matrícula?"):
            messagebox.showinfo("Éxito", "Matrícula eliminada exitosamente")
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VistaEliminarMatricula(root)
    root.mainloop() 