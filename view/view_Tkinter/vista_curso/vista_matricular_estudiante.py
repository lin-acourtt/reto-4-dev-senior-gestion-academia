import tkinter as tk
from tkinter import ttk, messagebox

class VistaMatricularEstudiante:
    def __init__(self, root):
        self.root = root
        self.root.title("Matricular Estudiante")
        self.root.geometry("600x400")
        
        # Frame principal
        self.frame_principal = ttk.Frame(self.root, padding="20")
        self.frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        ttk.Label(
            self.frame_principal,
            text="Matricular Estudiante en Curso",
            font=("Helvetica", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Campos del formulario
        self.crear_campos_formulario()
        
        # Botones
        self.crear_botones()
        
    def crear_campos_formulario(self):
        # Selección de estudiante
        ttk.Label(self.frame_principal, text="Estudiante:").grid(row=1, column=0, pady=5, sticky=tk.W)
        self.estudiante = ttk.Combobox(self.frame_principal, width=40)
        self.estudiante.grid(row=1, column=1, pady=5, padx=5)
        
        # Selección de curso
        ttk.Label(self.frame_principal, text="Curso:").grid(row=2, column=0, pady=5, sticky=tk.W)
        self.curso = ttk.Combobox(self.frame_principal, width=40)
        self.curso.grid(row=2, column=1, pady=5, padx=5)
        
        # Fecha de matrícula
        ttk.Label(self.frame_principal, text="Fecha de Matrícula:").grid(row=3, column=0, pady=5, sticky=tk.W)
        self.fecha_matricula = ttk.Entry(self.frame_principal, width=40)
        self.fecha_matricula.grid(row=3, column=1, pady=5, padx=5)
        
    def crear_botones(self):
        frame_botones = ttk.Frame(self.frame_principal)
        frame_botones.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            frame_botones,
            text="Matricular",
            command=self.realizar_matricula,
            style="Accent.TButton"
        ).grid(row=0, column=0, padx=5)
        
        ttk.Button(
            frame_botones,
            text="Cancelar",
            command=self.root.destroy,
            style="Danger.TButton"
        ).grid(row=0, column=1, padx=5)
        
    def realizar_matricula(self):
        # Aquí irá la lógica para realizar la matrícula
        messagebox.showinfo("Éxito", "Estudiante matriculado exitosamente")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VistaMatricularEstudiante(root)
    root.mainloop() 