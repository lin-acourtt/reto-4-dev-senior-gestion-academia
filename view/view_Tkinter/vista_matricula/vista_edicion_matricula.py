import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.matricula_controller import MatriculaController
from controllers.estudiante_controller import EstudianteController
from controllers.curso_controller import CursoController
from config.appearance import centrar_ventana

class VistaEdicionMatricula:
    def __init__(self, root, db=None, matricula_id=None):
        self.root = root
        self.db = db
        self.matricula_id = matricula_id
        self.controlador_matricula = MatriculaController(self.db)
        self.controlador_estudiante = EstudianteController(self.db)
        self.controlador_curso = CursoController(self.db)
        
        # Configurar la ventana
        self.root.title("Editar Matrícula")
        self.root.geometry("600x500")
        centrar_ventana(self.root)
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            self.frame_principal,
            text="Editar Matrícula",
            font=("Helvetica", 24, "bold")
        ).pack(pady=20)
        
        # Frame para el formulario
        self.frame_formulario = ctk.CTkFrame(self.frame_principal)
        self.frame_formulario.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Campos del formulario
        self.crear_campos_formulario()
        
        # Botones
        self.crear_botones()
        
        # Cargar datos de la matrícula
        self.cargar_datos_matricula()
        
    def crear_campos_formulario(self):
        # Frame para los campos
        frame_campos = ctk.CTkFrame(self.frame_formulario)
        frame_campos.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Estudiante
        ctk.CTkLabel(frame_campos, text="Estudiante:").pack(anchor="w", pady=(10,0))
        self.estudiante_var = ctk.StringVar()
        self.combo_estudiante = ctk.CTkComboBox(
            frame_campos,
            variable=self.estudiante_var,
            width=400,
            state="readonly"
        )
        self.combo_estudiante.pack(fill="x", pady=(5,10))
        self.cargar_estudiantes()
        
        # Curso
        ctk.CTkLabel(frame_campos, text="Curso:").pack(anchor="w", pady=(10,0))
        self.curso_var = ctk.StringVar()
        self.combo_curso = ctk.CTkComboBox(
            frame_campos,
            variable=self.curso_var,
            width=400,
            state="readonly"
        )
        self.combo_curso.pack(fill="x", pady=(5,10))
        self.cargar_cursos()
        
        # Fecha de matrícula
        ctk.CTkLabel(frame_campos, text="Fecha de Matrícula:").pack(anchor="w", pady=(10,0))
        self.fecha_var = ctk.StringVar()
        self.entry_fecha = ctk.CTkEntry(
            frame_campos,
            textvariable=self.fecha_var,
            width=400,
            placeholder_text="YYYY-MM-DD"
        )
        self.entry_fecha.pack(fill="x", pady=(5,10))
        
    def crear_botones(self):
        # Frame para botones
        frame_botones = ctk.CTkFrame(self.frame_principal)
        frame_botones.pack(fill="x", padx=20, pady=10)
        
        # Botón cancelar
        self.btn_cancelar = ctk.CTkButton(
            frame_botones,
            text="Cancelar",
            command=self.root.destroy,
            fg_color="gray"
        )
        self.btn_cancelar.pack(side="left", padx=5)
        
        # Botón guardar
        self.btn_guardar = ctk.CTkButton(
            frame_botones,
            text="Guardar Cambios",
            command=self.guardar_cambios
        )
        self.btn_guardar.pack(side="right", padx=5)
        
    def cargar_estudiantes(self):
        try:
            estudiantes = self.controlador_estudiante.listar_estudiantes()
            nombres_estudiantes = [f"{e.nombre} {e.apellido}" for e in estudiantes]
            self.combo_estudiante.configure(values=nombres_estudiantes)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar estudiantes: {str(e)}")
            
    def cargar_cursos(self):
        try:
            cursos = self.controlador_curso.listar_cursos()
            nombres_cursos = [c.nombre for c in cursos]
            self.combo_curso.configure(values=nombres_cursos)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar cursos: {str(e)}")
            
    def cargar_datos_matricula(self):
        try:
            # Obtener datos de la matrícula
            matricula, nombre_estudiante, nombre_curso = self.controlador_matricula.obtener_matricula_por_id(
                self.matricula_id
            )
            
            if not matricula:
                messagebox.showerror("Error", "No se encontró la matrícula")
                self.root.destroy()
                return
                
            # Establecer valores en los campos
            self.estudiante_var.set(nombre_estudiante)
            self.curso_var.set(nombre_curso)
            self.fecha_var.set(matricula.fecha_matricula.strftime("%Y-%m-%d"))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos de la matrícula: {str(e)}")
            self.root.destroy()
            
    def guardar_cambios(self):
        try:
            # Validar campos
            estudiante = self.estudiante_var.get()
            curso = self.curso_var.get()
            fecha = self.fecha_var.get().strip()
            
            if not estudiante:
                messagebox.showwarning("Advertencia", "Debe seleccionar un estudiante")
                return
                
            if not curso:
                messagebox.showwarning("Advertencia", "Debe seleccionar un curso")
                return
                
            if not fecha:
                messagebox.showwarning("Advertencia", "La fecha de matrícula es obligatoria")
                return
                
            # Validar formato de fecha
            try:
                fecha_matricula = datetime.strptime(fecha, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showwarning(
                    "Advertencia",
                    "El formato de fecha debe ser YYYY-MM-DD"
                )
                return
                
            # Obtener IDs
            estudiantes = self.controlador_estudiante.listar_estudiantes()
            cursos = self.controlador_curso.listar_cursos()
            
            # Encontrar ID del estudiante
            estudiante_id = None
            for e in estudiantes:
                if f"{e.nombre} {e.apellido}" == estudiante:
                    estudiante_id = e.id_estudiante
                    break
                    
            # Encontrar ID del curso
            curso_id = None
            for c in cursos:
                if c.nombre == curso:
                    curso_id = c.id_curso
                    break
                    
            if not estudiante_id or not curso_id:
                messagebox.showerror("Error", "No se pudo encontrar el estudiante o curso seleccionado")
                return
                
            # Actualizar matrícula
            self.controlador_matricula.actualizar_matricula_por_id(
                id_matricula=self.matricula_id,
                estudiante_id=estudiante_id,
                curso_id=curso_id,
                fecha_matricula=fecha_matricula
            )
            
            messagebox.showinfo("Éxito", "Matrícula actualizada correctamente")
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar matrícula: {str(e)}") 