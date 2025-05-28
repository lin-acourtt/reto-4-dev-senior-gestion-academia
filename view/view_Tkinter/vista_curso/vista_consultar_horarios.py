import customtkinter as ctk
from tkinter import ttk, messagebox
from config.appearance import centrar_ventana
from controllers.curso_controller import CursoController
from controllers.horario_controller import HorarioController

class VistaConsultarHorarios:
    def __init__(self, root, db=None):
        self.root = root
        self.db = db
        self.controlador_curso = CursoController(self.db)
        self.controlador_horario = HorarioController(self.db)
        
        # Configurar la ventana
        self.root.title("Consultar Horarios")
        self.root.geometry("800x600")
        centrar_ventana(self.root)
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            self.frame_principal,
            text="Consultar Horarios de Cursos",
            font=("Helvetica", 24, "bold")
        ).pack(pady=20)
        
        # Filtros de búsqueda
        self.crear_filtros()
        
        # Tabla de horarios
        self.crear_tabla_horarios()
        
        # Botones
        self.crear_botones()
        
        # Cargar datos iniciales
        self.cargar_horarios()
        
    def crear_filtros(self):
        # Frame para los filtros
        frame_filtros = ctk.CTkFrame(self.frame_principal)
        frame_filtros.pack(fill="x", padx=20, pady=10)
        
        # Título de la sección
        ctk.CTkLabel(
            frame_filtros,
            text="Filtros de búsqueda",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
        
        # Frame para los campos de filtro
        frame_campos = ctk.CTkFrame(frame_filtros)
        frame_campos.pack(fill="x", padx=20, pady=10)
        
        # Filtro por curso
        ctk.CTkLabel(frame_campos, text="Curso:").pack(side="left", padx=5)
        self.filtro_curso = ctk.CTkComboBox(frame_campos, width=200)
        self.filtro_curso.pack(side="left", padx=5)
        
        # Filtro por día
        ctk.CTkLabel(frame_campos, text="Día:").pack(side="left", padx=5)
        self.filtro_dia = ctk.CTkComboBox(
            frame_campos,
            width=150,
            values=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        )
        self.filtro_dia.pack(side="left", padx=5)
        
        # Botón de búsqueda
        ctk.CTkButton(
            frame_campos,
            text="Buscar",
            command=self.buscar_horarios,
            width=100,
            height=30,
            corner_radius=10
        ).pack(side="left", padx=5)
        
    def crear_tabla_horarios(self):
        # Frame para la tabla
        frame_tabla = ctk.CTkFrame(self.frame_principal)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear Treeview
        columnas = ("id", "curso", "dia", "hora_inicio", "hora_fin", "profesor", "aula")
        self.tabla_horarios = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
        
        # Definir encabezados
        self.tabla_horarios.heading("id", text="ID")
        self.tabla_horarios.heading("curso", text="Curso")
        self.tabla_horarios.heading("dia", text="Día")
        self.tabla_horarios.heading("hora_inicio", text="Hora Inicio")
        self.tabla_horarios.heading("hora_fin", text="Hora Fin")
        self.tabla_horarios.heading("profesor", text="Profesor")
        self.tabla_horarios.heading("aula", text="Aula")
        
        # Configurar columnas
        self.tabla_horarios.column("id", width=50, anchor="center")
        self.tabla_horarios.column("curso", width=200)
        self.tabla_horarios.column("dia", width=100)
        self.tabla_horarios.column("hora_inicio", width=100)
        self.tabla_horarios.column("hora_fin", width=100)
        self.tabla_horarios.column("profesor", width=150)
        self.tabla_horarios.column("aula", width=100)
        
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
        """Carga todos los horarios en la tabla"""
        try:
            # Limpiar tabla
            for item in self.tabla_horarios.get_children():
                self.tabla_horarios.delete(item)
                
            # Obtener horarios de la base de datos
            horarios = self.controlador_horario.listar_horarios()
            
            # Insertar cada horario en la tabla
            for horario in horarios:
                self.tabla_horarios.insert(
                    "",
                    "end",
                    values=(
                        horario.id_horario,
                        horario.curso.nombre,
                        horario.dia,
                        horario.hora_inicio,
                        horario.hora_fin,
                        horario.curso.profesor,
                        horario.aula
                    )
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar horarios: {str(e)}")
            
    def buscar_horarios(self):
        """Busca horarios según los filtros seleccionados"""
        try:
            # Obtener valores de los filtros
            curso = self.filtro_curso.get()
            dia = self.filtro_dia.get()
            
            # Limpiar tabla
            for item in self.tabla_horarios.get_children():
                self.tabla_horarios.delete(item)
                
            # Buscar horarios según los filtros
            horarios = self.controlador_horario.buscar_horarios(
                nombre_curso=curso if curso else None,
                dia=dia if dia else None
            )
            
            # Insertar resultados en la tabla
            for horario in horarios:
                self.tabla_horarios.insert(
                    "",
                    "end",
                    values=(
                        horario.id_horario,
                        horario.curso.nombre,
                        horario.dia,
                        horario.hora_inicio,
                        horario.hora_fin,
                        horario.curso.profesor,
                        horario.aula
                    )
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar horarios: {str(e)}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = VistaConsultarHorarios(root)
    root.mainloop() 