import customtkinter as ctk
import tkinter as ttk
from config.appearance import centrar_ventana

class VentanaCursosProfesor(ctk.CTk):
    """
        Inicializa la ventana para ver los cursos de un profesor.
    """
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.obtener_valores_de_seleccion()
        # De esta función se van a obtener:
        # self.iid_sel
        # self.nombre_sel
        # self.apellido_sel
        # self.correo_sel
        # self.telefono_sel
        # self.especialidad_sel

        # Configuración de la ventana
        self.title(f"Cursos del Profesor {self.nombre_sel} {self.apellido_sel}")

        centrar_ventana(self,proporcion=0.7)
        self.resizable(False, False)

        self.label_titulo = ctk.CTkLabel(
            self, 
            text=f"Cursos impartidos por {self.nombre_sel} {self.apellido_sel}",
            font=("Helvetica", 14, "bold")
        )
        self.label_titulo.pack(pady=10)
        
        # Frame para la tabla
        self.frame_tabla = ctk.CTkFrame(self)
        self.frame_tabla.pack(pady=20, padx=20, fill="both", expand=True)

        # Tabla de cursos
        self.tabla_cursos_prof = ttk.Treeview(
            self.frame_tabla,
            columns=("ID", "Nombre", "Descripción", "Duración", "Nivel"),
            show="headings"
        )
        self.tabla_cursos_prof.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Configurar encabezados
        self.tabla_cursos_prof.heading("ID", text="ID Curso")
        self.tabla_cursos_prof.heading("Nombre", text="Nombre del Curso")
        self.tabla_cursos_prof.heading("Descripción", text="Descripción")
        self.tabla_cursos_prof.heading("Duración", text="Duración (horas)")
        self.tabla_cursos_prof.heading("Nivel", text="Nivel")
        
        # Ajustar anchos de columna
        self.tabla_cursos_prof.column("ID", width=100)
        self.tabla_cursos_prof.column("Nombre", width=200)
        self.tabla_cursos_prof.column("Descripción", width=250)
        self.tabla_cursos_prof.column("Duración", width=100)
        self.tabla_cursos_prof.column("Nivel", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla_cursos_prof.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla_cursos_prof.configure(yscrollcommand=scrollbar.set)
        
        # Botón para cerrar
        self.btn_cerrar = ctk.CTkButton(
            self,
            text="Cerrar",
            command=self.destroy,
            width=200
        )
        self.btn_cerrar.pack(pady=10)
        
        # Cargar cursos
        self.cargar_cursos_docente()
        

    def obtener_valores_de_seleccion(self):
        """
            Obtiene los valores de la tabla según la selección que se haga
        """
        self.iid_sel = self.parent.frame_tabla_profesores.tabla_profesores.selection()[0]
        self.nombre_sel = self.parent.frame_tabla_profesores.tabla_profesores.item(self.iid_sel)['values'][1]
        self.apellido_sel = self.parent.frame_tabla_profesores.tabla_profesores.item(self.iid_sel)['values'][2]
        self.correo_sel = self.parent.frame_tabla_profesores.tabla_profesores.item(self.iid_sel)['values'][3]
        self.telefono_sel = self.parent.frame_tabla_profesores.tabla_profesores.item(self.iid_sel)['values'][4]
        self.especialidad_sel = self.parent.frame_tabla_profesores.tabla_profesores.item(self.iid_sel)['values'][5]
    
    def cargar_cursos_docente(self):
        return
    
        try:
            # Obtener cursos del profesor
            cursos = self.parent.controlador_profesor.obtener_cursos_profesor(self.iid_sel)
            
            # Limpiar tabla
            for row in self.tabla.get_children():
                self.tabla.delete(row)
            
            # Insertar cursos
            for curso in cursos:
                self.tabla.insert("", "end", values=(
                    curso.id_curso,
                    curso.nombre,
                    curso.descripcion,
                    curso.duracion,
                    curso.nivel
                ))
                
            if not cursos:
                messagebox.showinfo("Información", "Este profesor no tiene cursos asignados")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los cursos: {str(e)}")
