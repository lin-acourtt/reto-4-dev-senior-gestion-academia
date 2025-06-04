import customtkinter as ctk
from tkinter import ttk, messagebox
from config.appearance import centrar_ventana
from controllers.horario_controller import HorarioController
from controllers.curso_controller import CursoController

class VistaConsultarHorarios:
    def __init__(self, root, db=None):
        self.root = root
        self.db = db
        self.controlador_horario = HorarioController(self.db)
        self.controlador_curso = CursoController(self.db)
        
        # Configurar la ventana
        self.root.title("Consultar Horarios")
        self.root.geometry("1000x600")
        centrar_ventana(self.root)
        self.root.resizable(True, True)
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        self.label_titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Horarios de Todos los Cursos",
            font=("Helvetica", 24, "bold")
        )
        self.label_titulo.pack(pady=20)
        
        # Tabla de horarios
        self.crear_tabla_horarios()
        
        # Botones
        self.crear_botones()
        
        # Cargar todos los horarios
        self.cargar_horarios()
        
    def crear_tabla_horarios(self):
        # Frame para la tabla
        frame_tabla = ctk.CTkFrame(self.frame_principal)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear Treeview
        columnas = ("id", "curso", "dia", "hora_inicio", "hora_fin", "profesor")
        self.tabla_horarios = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        
        # Definir encabezados
        self.tabla_horarios.heading("id", text="ID")
        self.tabla_horarios.heading("curso", text="Curso")
        self.tabla_horarios.heading("dia", text="Día")
        self.tabla_horarios.heading("hora_inicio", text="Hora Inicio")
        self.tabla_horarios.heading("hora_fin", text="Hora Fin")
        self.tabla_horarios.heading("profesor", text="Profesor")
        
        # Configurar columnas
        self.tabla_horarios.column("id", width=50, anchor="center")
        self.tabla_horarios.column("curso", width=200)
        self.tabla_horarios.column("dia", width=150)
        self.tabla_horarios.column("hora_inicio", width=150, anchor="center")
        self.tabla_horarios.column("hora_fin", width=150, anchor="center")
        self.tabla_horarios.column("profesor", width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_horarios.yview)
        self.tabla_horarios.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar elementos
        self.tabla_horarios.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def crear_botones(self):
        frame_botones = ctk.CTkFrame(self.frame_principal)
        frame_botones.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            frame_botones,
            text="Actualizar",
            command=self.cargar_horarios,
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
        
    def cargar_horarios(self):
        """Carga todos los horarios de todos los cursos en la tabla"""
        try:
            # Limpiar tabla
            for item in self.tabla_horarios.get_children():
                self.tabla_horarios.delete(item)
                
            # Obtener todos los horarios
            horarios, nombres_cursos = self.controlador_horario.listar_horarios()
            
            if not horarios:
                messagebox.showinfo("Información", "No hay horarios registrados")
                return
            
            # Insertar cada horario en la tabla
            for horario, nombre_curso in zip(horarios, nombres_cursos):
                # Obtener información del curso
                curso = self.controlador_curso.obtener_curso_por_id(horario.curso_id)
                
                self.tabla_horarios.insert(
                    "",
                    "end",
                    values=(
                        horario.id_horario,
                        nombre_curso,
                        horario.dia_semana,
                        horario.hora_inicio,
                        horario.hora_fin,
                        curso.profesor if curso else "No asignado"
                    )
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar horarios: {str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = VistaConsultarHorarios(root)
    root.mainloop() 