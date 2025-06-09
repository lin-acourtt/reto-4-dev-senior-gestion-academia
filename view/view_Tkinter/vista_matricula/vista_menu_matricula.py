import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from controllers.matricula_controller import MatriculaController
from controllers.estudiante_controller import EstudianteController
from controllers.curso_controller import CursoController
from config.appearance import centrar_ventana
# from view.view_Tkinter.vista_principal.menu_principal import VentanaMenuPrincipal

class VistaMenuMatricula(ctk.CTk):
    def __init__(self, root, db=None, tema_actual="System"):
        super().__init__()
        self.root = root  # Guardamos referencia al root para poder volver al menú principal
        self.db = db
        self.controlador_matricula = MatriculaController(self.db)
        self.controlador_estudiante = EstudianteController(self.db)
        self.controlador_curso = CursoController(self.db)
        
        # Configurar el tema
        ctk.set_appearance_mode(tema_actual)
        
        # Configurar la ventana
        self.title("Gestión de Matrículas")
        self.geometry("1000x600")
        centrar_ventana(self)
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Frame superior con título y botón de regresar
        self.frame_superior = ctk.CTkFrame(self.frame_principal)
        self.frame_superior.pack(fill="x", padx=20, pady=(0, 20))
        
        # Título
        ctk.CTkLabel(
            self.frame_superior,
            text="Gestión de Matrículas",
            font=("Helvetica", 24, "bold")
        ).pack(side="left", padx=10)
        
        # Botón regresar
        self.btn_regresar = ctk.CTkButton(
            self.frame_superior,
            text="← Regresar al Menú Principal",
            command=self.regresar_menu_principal,
            fg_color="gray"
        )
        self.btn_regresar.pack(side="right", padx=10)
        
        # Frame para búsqueda y filtros
        self.frame_busqueda = ctk.CTkFrame(self.frame_principal)
        self.frame_busqueda.pack(fill="x", padx=20, pady=10)
        
        # Campos de búsqueda
        ctk.CTkLabel(self.frame_busqueda, text="Buscar por:").pack(side="left", padx=5)
        self.busqueda_var = ctk.StringVar()
        self.entry_busqueda = ctk.CTkEntry(
            self.frame_busqueda,
            width=200,
            textvariable=self.busqueda_var
        )
        self.entry_busqueda.pack(side="left", padx=5)
        
        # Botón de búsqueda
        self.btn_buscar = ctk.CTkButton(
            self.frame_busqueda,
            text="Buscar",
            command=self.buscar_matriculas
        )
        self.btn_buscar.pack(side="left", padx=5)
        
        # Botón de nueva matrícula
        self.btn_nueva = ctk.CTkButton(
            self.frame_busqueda,
            text="Nueva Matrícula",
            command=self.abrir_registro_matricula
        )
        self.btn_nueva.pack(side="right", padx=5)
        
        # Tabla de matrículas
        self.crear_tabla()
        
        # Frame para botones de acción
        self.frame_acciones = ctk.CTkFrame(self.frame_principal)
        self.frame_acciones.pack(fill="x", padx=20, pady=10)
        
        # Botones de acción
        self.btn_editar = ctk.CTkButton(
            self.frame_acciones,
            text="Editar",
            command=self.editar_matricula,
            state="disabled"
        )
        self.btn_editar.pack(side="left", padx=5)
        
        self.btn_eliminar = ctk.CTkButton(
            self.frame_acciones,
            text="Eliminar",
            command=self.eliminar_matricula,
            state="disabled"
        )
        self.btn_eliminar.pack(side="left", padx=5)
        
        # Cargar datos iniciales
        self.cargar_matriculas()
        
        # Configurar el protocolo de cierre de ventana
        self.protocol("WM_DELETE_WINDOW", self.regresar_menu_principal)
        
        # Iniciar el bucle principal
        self.mainloop()
        
    def regresar_menu_principal(self):

        """
            Método para cerrar la ventana y regresar el menú principal
        """
        self.quit()
        self.destroy()

        # Abrir de nuevo el menú principal
        from view.view_Tkinter.vista_principal.menu_principal import VentanaMenuPrincipal
        app = VentanaMenuPrincipal(db=self.db)
        # Iniciar el bucle principal de la aplicación
        app.iniciar_ventana()        
        
    def crear_tabla(self):
        # Frame para la tabla
        self.frame_tabla = ctk.CTkFrame(self.frame_principal)
        self.frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear Treeview
        self.tabla = ttk.Treeview(
            self.frame_tabla,
            columns=("id", "estudiante", "curso", "fecha"),
            show="headings"
        )
        
        # Configurar columnas
        self.tabla.heading("id", text="ID")
        self.tabla.heading("estudiante", text="Estudiante")
        self.tabla.heading("curso", text="Curso")
        self.tabla.heading("fecha", text="Fecha de Matrícula")
        
        self.tabla.column("id", width=50)
        self.tabla.column("estudiante", width=200)
        self.tabla.column("curso", width=200)
        self.tabla.column("fecha", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.frame_tabla,
            orient="vertical",
            command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar elementos
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Evento de selección
        self.tabla.bind("<<TreeviewSelect>>", self.on_select_matricula)
        
    def cargar_matriculas(self):
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
            
        try:
            # Obtener matrículas
            matriculas, nombres_estudiantes, nombres_cursos = self.controlador_matricula.listar_matriculas()
            
            # Insertar datos en la tabla
            for matricula, nombre_estudiante, nombre_curso in zip(matriculas, nombres_estudiantes, nombres_cursos):
                fecha = matricula.fecha_matricula.strftime("%d/%m/%Y") if matricula.fecha_matricula else "N/A"
                self.tabla.insert(
                    "",
                    "end",
                    values=(
                        matricula.id_matricula,
                        nombre_estudiante,
                        nombre_curso,
                        fecha
                    )
                )
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar matrículas: {str(e)}")
            
    def buscar_matriculas(self):
        busqueda = self.busqueda_var.get().strip()
        if not busqueda:
            self.cargar_matriculas()
            return
            
        try:
            # Limpiar tabla
            for item in self.tabla.get_children():
                self.tabla.delete(item)
                
            # Buscar matrículas
            matriculas = self.controlador_matricula.buscar_matriculas(
                nombre_estudiante=busqueda
            )
            
            # Insertar resultados
            for matricula in matriculas:
                fecha = matricula.fecha_matricula.strftime("%d/%m/%Y") if matricula.fecha_matricula else "N/A"
                self.tabla.insert(
                    "",
                    "end",
                    values=(
                        matricula.id_matricula,
                        f"{matricula.estudiante.nombre} {matricula.estudiante.apellido}",
                        matricula.curso.nombre,
                        fecha
                    )
                )
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar matrículas: {str(e)}")
            
    def on_select_matricula(self, event):
        # Habilitar botones de acción cuando se selecciona una matrícula
        selection = self.tabla.selection()
        if selection:
            self.btn_editar.configure(state="normal")
            self.btn_eliminar.configure(state="normal")
        else:
            self.btn_editar.configure(state="disabled")
            self.btn_eliminar.configure(state="disabled")
            
    def abrir_registro_matricula(self):
        # Importar aquí para evitar importación circular
        from .vista_registro_matricula import VistaRegistroMatricula
        
        # Crear nueva ventana
        ventana_registro = ctk.CTkToplevel(self)
        VistaRegistroMatricula(ventana_registro, self.db)
        
        # Esperar a que se cierre la ventana
        self.root.wait_window(ventana_registro)
        
        # Recargar matrículas
        self.cargar_matriculas()
        
    def editar_matricula(self):
        selection = self.tabla.selection()
        if not selection:
            return
            
        # Obtener ID de la matrícula seleccionada
        matricula_id = self.tabla.item(selection[0])["values"][0]
        
        # Importar aquí para evitar importación circular
        from .vista_edicion_matricula import VistaEdicionMatricula
        
        # Crear nueva ventana
        ventana_edicion = ctk.CTkToplevel(self)
        VistaEdicionMatricula(ventana_edicion, self.db, matricula_id)
        
        # Esperar a que se cierre la ventana
        self.root.wait_window(ventana_edicion)
        
        # Recargar matrículas
        self.cargar_matriculas()
        
    def eliminar_matricula(self):
        selection = self.tabla.selection()
        if not selection:
            return
            
        # Obtener ID de la matrícula seleccionada
        matricula_id = self.tabla.item(selection[0])["values"][0]
        
        # Confirmar eliminación
        if messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de que desea eliminar esta matrícula?"
        ):
            try:
                self.controlador_matricula.eliminar_matricula_por_id(matricula_id)
                messagebox.showinfo("Éxito", "Matrícula eliminada correctamente")
                self.cargar_matriculas()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar matrícula: {str(e)}")
