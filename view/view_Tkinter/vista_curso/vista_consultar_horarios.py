import tkinter as tk
from tkinter import ttk, messagebox

class VistaConsultarHorarios:
    def __init__(self, root):
        self.root = root
        self.root.title("Consultar Horarios")
        self.root.geometry("800x600")
        
        # Frame principal
        self.frame_principal = ttk.Frame(self.root, padding="20")
        self.frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        ttk.Label(
            self.frame_principal,
            text="Consultar Horarios de Cursos",
            font=("Helvetica", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Filtros de búsqueda
        self.crear_filtros()
        
        # Tabla de horarios
        self.crear_tabla_horarios()
        
        # Botones
        self.crear_botones()
        
    def crear_filtros(self):
        frame_filtros = ttk.LabelFrame(self.frame_principal, text="Filtros de búsqueda", padding="10")
        frame_filtros.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Filtro por curso
        ttk.Label(frame_filtros, text="Curso:").grid(row=0, column=0, padx=5)
        self.filtro_curso = ttk.Combobox(frame_filtros, width=30)
        self.filtro_curso.grid(row=0, column=1, padx=5)
        
        # Filtro por día
        ttk.Label(frame_filtros, text="Día:").grid(row=0, column=2, padx=5)
        self.filtro_dia = ttk.Combobox(frame_filtros, width=20)
        self.filtro_dia.grid(row=0, column=3, padx=5)
        
        # Botón de búsqueda
        ttk.Button(
            frame_filtros,
            text="Buscar",
            command=self.buscar_horarios,
            style="Accent.TButton"
        ).grid(row=0, column=4, padx=5)
        
    def crear_tabla_horarios(self):
        # Frame para la tabla
        frame_tabla = ttk.Frame(self.frame_principal)
        frame_tabla.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear Treeview
        columnas = ("id", "curso", "dia", "hora_inicio", "hora_fin", "profesor", "aula")
        self.tabla_horarios = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        # Definir encabezados
        self.tabla_horarios.heading("id", text="ID")
        self.tabla_horarios.heading("curso", text="Curso")
        self.tabla_horarios.heading("dia", text="Día")
        self.tabla_horarios.heading("hora_inicio", text="Hora Inicio")
        self.tabla_horarios.heading("hora_fin", text="Hora Fin")
        self.tabla_horarios.heading("profesor", text="Profesor")
        self.tabla_horarios.heading("aula", text="Aula")
        
        # Configurar columnas
        self.tabla_horarios.column("id", width=50)
        self.tabla_horarios.column("curso", width=200)
        self.tabla_horarios.column("dia", width=100)
        self.tabla_horarios.column("hora_inicio", width=100)
        self.tabla_horarios.column("hora_fin", width=100)
        self.tabla_horarios.column("profesor", width=150)
        self.tabla_horarios.column("aula", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tabla_horarios.yview)
        self.tabla_horarios.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar elementos
        self.tabla_horarios.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
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
        
    def buscar_horarios(self):
        # Aquí irá la lógica para buscar horarios
        messagebox.showinfo("Búsqueda", "Buscando horarios...")
        
    def actualizar_lista(self):
        # Aquí irá la lógica para actualizar la lista de horarios
        messagebox.showinfo("Actualización", "Lista de horarios actualizada")

if __name__ == "__main__":
    root = tk.Tk()
    app = VistaConsultarHorarios(root)
    root.mainloop() 