import tkinter as tk
from tkinter import ttk, messagebox

class VistaCrearCurso:
    def __init__(self, root):
        self.root = root
        self.root.title("Crear Nuevo Curso")
        self.root.geometry("600x400")
        
        # Frame principal
        self.frame_principal = ttk.Frame(self.root, padding="20")
        self.frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        ttk.Label(
            self.frame_principal,
            text="Crear Nuevo Curso",
            font=("Helvetica", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Campos del formulario
        self.crear_campos_formulario()
        
        # Botones
        self.crear_botones()
        
    def crear_campos_formulario(self):
        # Nombre del curso
        ttk.Label(self.frame_principal, text="Nombre del Curso:").grid(row=1, column=0, pady=5, sticky=tk.W)
        self.nombre_curso = ttk.Entry(self.frame_principal, width=40)
        self.nombre_curso.grid(row=1, column=1, pady=5, padx=5)
        
        # Profesor
        ttk.Label(self.frame_principal, text="Profesor:").grid(row=2, column=0, pady=5, sticky=tk.W)
        self.profesor = ttk.Combobox(self.frame_principal, width=37)
        self.profesor.grid(row=2, column=1, pady=5, padx=5)
        
        # Descripción
        ttk.Label(self.frame_principal, text="Descripción:").grid(row=3, column=0, pady=5, sticky=tk.W)
        self.descripcion = tk.Text(self.frame_principal, width=30, height=4)
        self.descripcion.grid(row=3, column=1, pady=5, padx=5)
        
    def crear_botones(self):
        frame_botones = ttk.Frame(self.frame_principal)
        frame_botones.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            frame_botones,
            text="Guardar",
            command=self.guardar_curso,
            style="Accent.TButton"
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            frame_botones,
            text="Cancelar",
            command=self.root.destroy,
            style="Danger.TButton"
        ).grid(row=0, column=1, padx=5)
        
    def guardar_curso(self):
        # Aquí irá la lógica para guardar el curso
        messagebox.showinfo("Éxito", "Curso creado exitosamente")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VistaCrearCurso(root)
    root.mainloop() 