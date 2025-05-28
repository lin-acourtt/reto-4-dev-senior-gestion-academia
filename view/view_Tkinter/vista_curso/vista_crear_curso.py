import customtkinter as ctk
from tkinter import messagebox
from config.appearance import centrar_ventana
from controllers.curso_controller import CursoController

class VistaCrearCurso:
    def __init__(self, root, db=None):
        self.root = root
        self.db = db
        self.controlador_curso = CursoController(self.db)
        
        # Configurar la ventana
        self.root.title("Crear Nuevo Curso")
        self.root.geometry("600x500")
        centrar_ventana(self.root)
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            self.frame_principal,
            text="Crear Nuevo Curso",
            font=("Helvetica", 24, "bold")
        ).pack(pady=20)
        
        # Campos del formulario
        self.crear_campos_formulario()
        
        # Botones
        self.crear_botones()
        
    def crear_campos_formulario(self):
        # Frame para los campos
        frame_campos = ctk.CTkFrame(self.frame_principal)
        frame_campos.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Nombre del curso
        ctk.CTkLabel(frame_campos, text="Nombre del Curso:").pack(pady=(10,5))
        self.nombre_curso = ctk.CTkEntry(frame_campos, width=400)
        self.nombre_curso.pack(pady=(0,10))
        
        # Profesor
        ctk.CTkLabel(frame_campos, text="Profesor:").pack(pady=(10,5))
        self.profesor = ctk.CTkComboBox(frame_campos, width=400)
        self.profesor.pack(pady=(0,10))
        
        # Descripción
        ctk.CTkLabel(frame_campos, text="Descripción:").pack(pady=(10,5))
        self.descripcion = ctk.CTkTextbox(frame_campos, width=400, height=100)
        self.descripcion.pack(pady=(0,10))
        
        # Duración en horas
        ctk.CTkLabel(frame_campos, text="Duración (horas):").pack(pady=(10,5))
        self.duracion_horas = ctk.CTkEntry(frame_campos, width=400)
        self.duracion_horas.pack(pady=(0,10))
        
        # Cargar lista de profesores
        self.cargar_profesores()
        
    def crear_botones(self):
        frame_botones = ctk.CTkFrame(self.frame_principal)
        frame_botones.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            frame_botones,
            text="Guardar",
            command=self.guardar_curso,
            width=200,
            height=40,
            corner_radius=10
        ).pack(side="left", padx=10, expand=True)
        
        ctk.CTkButton(
            frame_botones,
            text="Cancelar",
            command=self.root.destroy,
            width=200,
            height=40,
            corner_radius=10,
            fg_color="#FF5555",
            hover_color="#FF3333"
        ).pack(side="right", padx=10, expand=True)
        
    def cargar_profesores(self):
        """Carga la lista de profesores en el combobox"""
        try:
            # Aquí deberías obtener la lista de profesores de la base de datos
            # Por ahora usaremos datos de ejemplo
            profesores = ["Profesor 1", "Profesor 2", "Profesor 3"]
            self.profesor.configure(values=profesores)
            if profesores:
                self.profesor.set(profesores[0])
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar profesores: {str(e)}")
        
    def guardar_curso(self):
        """Guarda el curso en la base de datos"""
        try:
            # Obtener valores del formulario
            nombre = self.nombre_curso.get().strip()
            profesor = self.profesor.get()
            descripcion = self.descripcion.get("1.0", "end-1c").strip()
            duracion = self.duracion_horas.get().strip()
            
            # Validar campos requeridos
            if not nombre:
                messagebox.showwarning("Advertencia", "El nombre del curso es obligatorio")
                return
                
            if not profesor:
                messagebox.showwarning("Advertencia", "Debe seleccionar un profesor")
                return
            
            # Convertir duración a entero si se proporcionó
            duracion_horas = int(duracion) if duracion.isdigit() else None
            
            # Aquí deberías obtener el ID del profesor seleccionado
            # Por ahora usaremos un ID de ejemplo
            id_profesor = 1
            
            # Guardar en la base de datos
            if self.controlador_curso.registrar_curso(
                nombre=nombre,
                id_profesor=id_profesor,
                descripcion=descripcion,
                duracion_horas=duracion_horas
            ):
                messagebox.showinfo("Éxito", "Curso creado exitosamente")
                self.root.destroy()
            else:
                messagebox.showerror("Error", "No se pudo crear el curso")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el curso: {str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = VistaCrearCurso(root)
    root.mainloop() 