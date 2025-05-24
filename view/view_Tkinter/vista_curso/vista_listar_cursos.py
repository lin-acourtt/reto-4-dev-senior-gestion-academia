import tkinter as tk
from tkinter import ttk, messagebox

class VistaListarCursos:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Cursos")
        self.root.geometry("800x600")
        
        # Frame principal
        self.frame_principal = ttk.Frame(self.root, padding="20")
        self.frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        ttk.Label(
            self.frame_principal,
            text="Lista de Cursos",
            font=("Helvetica", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Crear Treeview para mostrar los cursos
        self.crear_tabla_cursos()
        
        # Botones de acción
        self.crear_botones()
        
    def crear_tabla_cursos(self):
        # Frame para la tabla
        frame_tabla = ttk.Frame(self.frame_principal)
        frame_tabla.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear Treeview
        columnas = ("id", "nombre", "profesor", "estudiantes", "horarios")
        self.tabla_cursos = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        # Definir encabezados
        self.tabla_cursos.heading("id", text="ID")
        self.tabla_cursos.heading("nombre", text="Nombre del Curso")
        self.tabla_cursos.heading("profesor", text="Profesor")
        self.tabla_cursos.heading("estudiantes", text="Estudiantes")
        self.tabla_cursos.heading("horarios", text="Horarios")
        
        # Configurar columnas
        self.tabla_cursos.column("id", width=50)
        self.tabla_cursos.column("nombre", width=200)
        self.tabla_cursos.column("profesor", width=150)
        self.tabla_cursos.column("estudiantes", width=100)
        self.tabla_cursos.column("horarios", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tabla_cursos.yview)
        self.tabla_cursos.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar elementos
        self.tabla_cursos.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
    def crear_botones(self):
        frame_botones = ttk.Frame(self.frame_principal)
        frame_botones.grid(row=2, column=0, columnspan=2, pady=20)
        
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
        
    def actualizar_lista(self):
        # Aquí irá la lógica para actualizar la lista de cursos
        # Por ahora solo mostraremos un mensaje
        messagebox.showinfo("Actualización", "Lista de cursos actualizada")

if __name__ == "__main__":
    root = tk.Tk()
    app = VistaListarCursos(root)
    root.mainloop() 