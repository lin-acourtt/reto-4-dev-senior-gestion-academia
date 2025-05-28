import customtkinter as ctk
from tkinter import ttk, messagebox
from config.appearance import centrar_ventana
from config.database import Database

from controllers.curso_controller import CursoController

from .vista_crear_curso import VistaCrearCurso
from .vista_listar_cursos import VistaListarCursos
from .vista_matricular_estudiante import VistaMatricularEstudiante
from .vista_consultar_matriculas import VistaConsultarMatriculas
from .vista_consultar_horarios import VistaConsultarHorarios
from .vista_eliminar_matricula import VistaEliminarMatricula

class VistaMenuCurso:
    def __init__(self, db: Database = None, tema_actual: str = "System"):
        self.db = db
        self.tema_actual = tema_actual
        self.root = ctk.CTk()
        self.controlador_curso = CursoController(self.db)
        
    def iniciar_ventana(self):
        """Inicializa la ventana del menú de cursos"""
        self.root.title("Gestión de Cursos - Academia")
        self.root.geometry("1300x1500")
        
        # Configurar el tema
        ctk.set_appearance_mode(self.tema_actual)
        centrar_ventana(self.root)
        
        # Frame principal que contendrá la tabla y los botones
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            self.frame_principal,
            text="Gestión de Cursos",
            font=("Helvetica", 24, "bold")
        ).pack(pady=20)
        
        # Frame contenedor para la tabla y los botones
        frame_contenedor = ctk.CTkFrame(self.frame_principal)
        frame_contenedor.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Frame para la tabla (izquierda)
        frame_tabla = ctk.CTkFrame(frame_contenedor)
        frame_tabla.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Título de la tabla
        ctk.CTkLabel(
            frame_tabla,
            text="Cursos y sus caracteristicas.",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
        
        # Crear Treeview para mostrar los cursos
        self.crear_tabla_cursos(frame_tabla)
        
        # Frame para los botones (derecha)
        frame_botones = ctk.CTkFrame(frame_contenedor)
        frame_botones.pack(side="right", fill="y", padx=(10, 0))
        
        # Título de la sección de botones
        ctk.CTkLabel(
            frame_botones,
            text="Acciones",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
        
        # Botones del menú
        botones = [
            ("➕ Crear Nuevo Curso", self.abrir_crear_curso),
            ("📝 Actualizar Curso", self.abrir_actualizar_curso),
            ("🗑️ Eliminar Curso", self.abrir_eliminar_curso),
            ("👨‍🎓 Matricular Estudiante", self.abrir_matricular_estudiante),
            ("📊 Consultar Matrículas", self.abrir_consultar_matriculas),
            ("🕒 Consultar Horarios", self.abrir_consultar_horarios),
            ("❌ Eliminar Matrícula", self.abrir_eliminar_matricula)
        ]
        
        for texto, comando in botones:
            ctk.CTkButton(
                frame_botones,
                text=texto,
                command=comando,
                width=250,
                height=40,
                corner_radius=10
            ).pack(pady=10, padx=20)
            
        # Botón de actualizar
        ctk.CTkButton(
            frame_botones,
            text="🔄 Actualizar Lista",
            command=self.actualizar_tabla,
            width=250,
            height=40,
            corner_radius=10,
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).pack(pady=10, padx=20)
            
        # Botón de salir
        ctk.CTkButton(
            frame_botones,
            text="↩️ Volver al Menú Principal",
            command=self.volver_menu_principal,
            width=220,
            height=40,
            corner_radius=20,
            fg_color="#FF5555",
            hover_color="#FF3333"
        ).pack(pady=20, padx=20)
        
        self.root.mainloop()
        
    def crear_tabla_cursos(self, parent):
        """Crea la tabla de cursos y profesores"""
        # Frame para la tabla y scrollbar
        frame_tabla = ctk.CTkFrame(parent)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear Treeview
        columnas = ("id", "nombre", "profesor", "estudiantes", "horarios", "descripcion", "duracion")
        self.tabla_cursos = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=20)
        
        # Definir encabezados
        self.tabla_cursos.heading("id", text="ID")
        self.tabla_cursos.heading("nombre", text="Nombre del Curso")
        self.tabla_cursos.heading("profesor", text="Profesor")
        self.tabla_cursos.heading("estudiantes", text="Estudiantes")
        self.tabla_cursos.heading("horarios", text="Horarios")
        self.tabla_cursos.heading("descripcion", text="Descripción")
        self.tabla_cursos.heading("duracion", text="Duración (hrs)")
        
        # Configurar columnas
        self.tabla_cursos.column("id", width=50, anchor="center")
        self.tabla_cursos.column("nombre", width=150)
        self.tabla_cursos.column("profesor", width=150)
        self.tabla_cursos.column("estudiantes", width=80, anchor="center")
        self.tabla_cursos.column("horarios", width=120)
        self.tabla_cursos.column("descripcion", width=200)
        self.tabla_cursos.column("duracion", width=100, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_cursos.yview)
        self.tabla_cursos.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar elementos
        self.tabla_cursos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Cargar datos iniciales
        self.cargar_datos_tabla()
        
    def cargar_datos_tabla(self):
        """Carga los datos en la tabla de cursos desde la base de datos"""
        # Limpiar tabla
        for item in self.tabla_cursos.get_children():
            self.tabla_cursos.delete(item)
            
        try:
            # Obtener cursos desde la base de datos
            cursos = self.controlador_curso.listar_cursos()
            
            # Insertar cada curso en la tabla
            for curso in cursos:
                self.tabla_cursos.insert(
                    "",
                    "end",
                    iid=curso.id_curso,
                    values=(
                        curso.id_curso,
                        curso.nombre,
                        curso.profesor,
                        curso.num_estudiantes,
                        curso.horarios,
                        curso.descripcion or "Sin descripción",
                        curso.duracion_horas or "N/A"
                    )
                )
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los cursos: {str(e)}")
            
    def actualizar_tabla(self):
        """Actualiza los datos de la tabla"""
        self.cargar_datos_tabla()
        messagebox.showinfo("Actualización", "Lista de cursos actualizada")
        
    def abrir_ventana_secundaria(self, titulo, clase_vista):
        """Abre una ventana secundaria y la configura para que aparezca por encima"""
        ventana = ctk.CTkToplevel(self.root)
        ventana.title(titulo)
        ventana.geometry("600x500")
        ventana.transient(self.root)  # Hace que la ventana sea transitoria de la principal
        ventana.grab_set()  # Hace que la ventana sea modal
        centrar_ventana(ventana)
        
        # Crear instancia de la vista pasando la ventana y la conexión a la base de datos
        vista = clase_vista(ventana, self.db)
        
        # Configurar el tema
        ctk.set_appearance_mode(self.tema_actual)
        
        return vista
        
    def abrir_crear_curso(self):
        """Abre la ventana para crear un nuevo curso"""
        self.abrir_ventana_secundaria("Crear Nuevo Curso", VistaCrearCurso)
        
    def abrir_actualizar_curso(self):
        """Abre la ventana para actualizar un curso"""
        # Verificar si hay un curso seleccionado
        seleccion = self.tabla_cursos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un curso para actualizar")
            return
            
        curso_id = self.tabla_cursos.item(seleccion[0])['values'][0]
        self.abrir_ventana_secundaria(f"Actualizar Curso {curso_id}", VistaCrearCurso)  # Reutilizamos la vista de crear
        
    def abrir_eliminar_curso(self):
        """Abre la ventana para eliminar un curso"""
        # Verificar si hay un curso seleccionado
        seleccion = self.tabla_cursos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un curso para eliminar")
            return
            
        curso_id = self.tabla_cursos.item(seleccion[0])['values'][0]
        curso_nombre = self.tabla_cursos.item(seleccion[0])['values'][1]
        
        if messagebox.askyesno("Confirmar Eliminación", 
                             f"¿Está seguro de eliminar el curso '{curso_nombre}'?"):
            try:
                if self.controlador_curso.eliminar_curso(curso_id):
                    messagebox.showinfo("Éxito", f"Curso '{curso_nombre}' eliminado exitosamente")
                    self.actualizar_tabla()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el curso")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar el curso: {str(e)}")
        
    def abrir_matricular_estudiante(self):
        """Abre la ventana para matricular un estudiante en un curso"""
        self.abrir_ventana_secundaria("Matricular Estudiante", VistaMatricularEstudiante)
        
    def abrir_consultar_matriculas(self):
        """Abre la ventana para consultar las matrículas"""
        self.abrir_ventana_secundaria("Consultar Matrículas", VistaConsultarMatriculas)
        
    def abrir_consultar_horarios(self):
        """Abre la ventana para consultar los horarios de los cursos"""
        self.abrir_ventana_secundaria("Consultar Horarios", VistaConsultarHorarios)
        
    def abrir_eliminar_matricula(self):
        """Abre la ventana para eliminar una matrícula"""
        self.abrir_ventana_secundaria("Eliminar Matrícula", VistaEliminarMatricula)
        
    def volver_menu_principal(self):
        """Cierra la ventana actual y vuelve al menú principal"""
        self.root.destroy()

        from view.view_Tkinter.vista_principal.menu_principal import VentanaMenuPrincipal
        app = VentanaMenuPrincipal(db=self.db)
        app.iniciar_ventana(self.tema_actual)

if __name__ == "__main__":
    db = Database()
    app = VistaMenuCurso(db)
    app.iniciar_ventana()
