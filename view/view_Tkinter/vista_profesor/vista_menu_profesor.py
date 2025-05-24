import customtkinter as ctk
import platform
from tkinter import ttk, messagebox
from controllers.profesor_controller import ProfesorController
from mysql.connector import IntegrityError


class VentanaRegistroDocente(ctk.CTkToplevel):
    def __init__(self, parent, db, callback_actualizar):
        super().__init__(parent)
        self.db = db
        self.callback_actualizar = callback_actualizar
        self.profesor_controller = ProfesorController(db)
        
        # Configuración de la ventana
        self.title("Registrar Nuevo Docente")
        ancho = 500
        alto = 600
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.resizable(False, False)
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Título
        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Registro de Docente",
            font=("Arial", 20, "bold")
        )
        self.titulo.pack(pady=20)
        
        # Campos de entrada
        self.frame_campos = ctk.CTkFrame(self.frame_principal)
        self.frame_campos.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Nombre
        self.label_nombre = ctk.CTkLabel(self.frame_campos, text="Nombre:")
        self.label_nombre.pack(pady=(10,0))
        self.entry_nombre = ctk.CTkEntry(self.frame_campos, width=300)
        self.entry_nombre.pack(pady=(0,10))
        
        # Apellido
        self.label_apellido = ctk.CTkLabel(self.frame_campos, text="Apellido:")
        self.label_apellido.pack(pady=(10,0))
        self.entry_apellido = ctk.CTkEntry(self.frame_campos, width=300)
        self.entry_apellido.pack(pady=(0,10))
        
        # Correo
        self.label_correo = ctk.CTkLabel(self.frame_campos, text="Correo:")
        self.label_correo.pack(pady=(10,0))
        self.entry_correo = ctk.CTkEntry(self.frame_campos, width=300)
        self.entry_correo.pack(pady=(0,10))
        
        # Teléfono
        self.label_telefono = ctk.CTkLabel(self.frame_campos, text="Teléfono:")
        self.label_telefono.pack(pady=(10,0))
        self.entry_telefono = ctk.CTkEntry(self.frame_campos, width=300)
        self.entry_telefono.pack(pady=(0,10))
        
        # Especialidad
        self.label_especialidad = ctk.CTkLabel(self.frame_campos, text="Especialidad:")
        self.label_especialidad.pack(pady=(10,0))
        self.entry_especialidad = ctk.CTkEntry(self.frame_campos, width=300)
        self.entry_especialidad.pack(pady=(0,10))
        
        # Botones
        self.frame_botones = ctk.CTkFrame(self.frame_principal)
        self.frame_botones.pack(pady=20, padx=20, fill="x")
        
        self.btn_guardar = ctk.CTkButton(
            self.frame_botones,
            text="Guardar",
            command=self.guardar_docente,
            width=200
        )
        self.btn_guardar.pack(side="left", padx=10, expand=True)
        
        self.btn_cancelar = ctk.CTkButton(
            self.frame_botones,
            text="Cancelar",
            command=self.destroy,
            width=200,
            fg_color="gray",
            hover_color="darkgray"
        )
        self.btn_cancelar.pack(side="right", padx=10, expand=True)
    
    def guardar_docente(self):
        try:
            # Obtener datos de los campos
            nombre = self.entry_nombre.get().strip()
            apellido = self.entry_apellido.get().strip()
            correo = self.entry_correo.get().strip()
            telefono = self.entry_telefono.get().strip()
            especialidad = self.entry_especialidad.get().strip()
            
            # Validar campos
            if not all([nombre, apellido, correo, telefono, especialidad]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            # Crear profesor
            profesor = self.profesor_controller.registrar_profesor(
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                telefono=telefono,
                especialidad=especialidad
            )
            
            messagebox.showinfo("Éxito", "Docente registrado correctamente")
            self.callback_actualizar()  # Actualizar la tabla principal
            self.destroy()
            
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                messagebox.showerror("Error", "Ya existe un docente con ese correo")
            else:
                messagebox.showerror("Error", f"Error al registrar el docente: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")


class VentanaCursosDocente(ctk.CTkToplevel):
    def __init__(self, parent, db, docente_id, docente_nombre, docente_apellido):
        super().__init__(parent)
        self.db = db
        self.docente_id = docente_id
        self.profesor_controller = ProfesorController(db)
        
        # Configuración de la ventana
        self.title(f"Cursos del Profesor {docente_nombre} {docente_apellido}")
        ancho = 800
        alto = 600
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Título
        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text=f"Cursos impartidos por {docente_nombre} {docente_apellido}",
            font=("Arial", 16, "bold")
        )
        self.titulo.pack(pady=10)
        
        # Tabla de cursos
        self.tabla = ttk.Treeview(
            self.frame_principal,
            columns=("ID", "Nombre", "Descripción", "Duración", "Nivel"),
            show="headings"
        )
        self.tabla.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Configurar encabezados
        self.tabla.heading("ID", text="ID Curso")
        self.tabla.heading("Nombre", text="Nombre del Curso")
        self.tabla.heading("Descripción", text="Descripción")
        self.tabla.heading("Duración", text="Duración (horas)")
        self.tabla.heading("Nivel", text="Nivel")
        
        # Ajustar anchos de columna
        self.tabla.column("ID", width=100)
        self.tabla.column("Nombre", width=200)
        self.tabla.column("Descripción", width=250)
        self.tabla.column("Duración", width=100)
        self.tabla.column("Nivel", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_principal, orient="vertical", command=self.tabla.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        # Botón para cerrar
        self.btn_cerrar = ctk.CTkButton(
            self.frame_principal,
            text="Cerrar",
            command=self.destroy,
            width=200
        )
        self.btn_cerrar.pack(pady=10)
        
        # Cargar cursos
        self.cargar_cursos_docente()
    
    def cargar_cursos_docente(self):
        try:
            # Obtener cursos del profesor
            cursos = self.profesor_controller.obtener_cursos_profesor(self.docente_id)
            
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


class VentanaActualizarProfesor(ctk.CTkToplevel):
    def __init__(self, parent, db, profesor_id, callback_actualizar):
        super().__init__(parent)
        self.db = db
        self.profesor_id = profesor_id
        self.callback_actualizar = callback_actualizar
        self.profesor_controller = ProfesorController(db)
        
        # Configuración de la ventana
        self.title("Actualizar Profesor")
        ancho = 500
        alto = 600
        x = (self.winfo_screenwidth() - ancho) // 2
        y = (self.winfo_screenheight() - alto) // 2
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.resizable(False, False)
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Título
        self.titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Actualizar Profesor",
            font=("Arial", 20, "bold")
        )
        self.titulo.pack(pady=20)
        
        # Campos de entrada
        self.frame_campos = ctk.CTkFrame(self.frame_principal)
        self.frame_campos.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Nombre
        self.label_nombre = ctk.CTkLabel(self.frame_campos, text="Nombre:")
        self.label_nombre.pack(pady=(10,0))
        self.entry_nombre = ctk.CTkEntry(self.frame_campos, width=300)
        self.entry_nombre.pack(pady=(0,10))
        
        # Apellido
        self.label_apellido = ctk.CTkLabel(self.frame_campos, text="Apellido:")
        self.label_apellido.pack(pady=(10,0))
        self.entry_apellido = ctk.CTkEntry(self.frame_campos, width=300)
        self.entry_apellido.pack(pady=(0,10))
        
        # Correo
        self.label_correo = ctk.CTkLabel(self.frame_campos, text="Correo:")
        self.label_correo.pack(pady=(10,0))
        self.entry_correo = ctk.CTkEntry(self.frame_campos, width=300)
        self.entry_correo.pack(pady=(0,10))
        
        # Teléfono
        self.label_telefono = ctk.CTkLabel(self.frame_campos, text="Teléfono:")
        self.label_telefono.pack(pady=(10,0))
        self.entry_telefono = ctk.CTkEntry(self.frame_campos, width=300)
        self.entry_telefono.pack(pady=(0,10))
        
        # Especialidad
        self.label_especialidad = ctk.CTkLabel(self.frame_campos, text="Especialidad:")
        self.label_especialidad.pack(pady=(10,0))
        self.entry_especialidad = ctk.CTkEntry(self.frame_campos, width=300)
        self.entry_especialidad.pack(pady=(0,10))
        
        # Botones
        self.frame_botones = ctk.CTkFrame(self.frame_principal)
        self.frame_botones.pack(pady=20, padx=20, fill="x")
        
        self.btn_guardar = ctk.CTkButton(
            self.frame_botones,
            text="Guardar Cambios",
            command=self.actualizar_profesor,
            width=200
        )
        self.btn_guardar.pack(side="left", padx=10, expand=True)
        
        self.btn_cancelar = ctk.CTkButton(
            self.frame_botones,
            text="Cancelar",
            command=self.destroy,
            width=200,
            fg_color="gray",
            hover_color="darkgray"
        )
        self.btn_cancelar.pack(side="right", padx=10, expand=True)
        
        # Cargar datos del profesor
        self.cargar_datos_profesor()
    
    def cargar_datos_profesor(self):
        try:
            profesor = self.profesor_controller.obtener_profesor_por_id(self.profesor_id)
            if profesor:
                self.entry_nombre.insert(0, profesor.nombre)
                self.entry_apellido.insert(0, profesor.apellido)
                self.entry_correo.insert(0, profesor.correo)
                self.entry_telefono.insert(0, profesor.telefono)
                self.entry_especialidad.insert(0, profesor.especialidad)
            else:
                messagebox.showerror("Error", "No se pudo cargar los datos del profesor")
                self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {str(e)}")
            self.destroy()
    
    def actualizar_profesor(self):
        try:
            # Obtener datos de los campos
            nombre = self.entry_nombre.get().strip()
            apellido = self.entry_apellido.get().strip()
            correo = self.entry_correo.get().strip()
            telefono = self.entry_telefono.get().strip()
            especialidad = self.entry_especialidad.get().strip()
            
            # Validar campos
            if not all([nombre, apellido, correo, telefono, especialidad]):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            # Actualizar profesor
            self.profesor_controller.actualizar_profesor_por_id(
                id_profesor=self.profesor_id,
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                telefono=telefono,
                especialidad=especialidad
            )
            
            messagebox.showinfo("Éxito", "Profesor actualizado correctamente")
            self.callback_actualizar()  # Actualizar la tabla principal
            self.destroy()
            
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                messagebox.showerror("Error", "Ya existe un profesor con ese correo")
            else:
                messagebox.showerror("Error", f"Error al actualizar el profesor: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")


class MenuDocenteFull():
    def __init__(self, db=None, tema_actual="System"):
        self.db = db
        self.profesor_controller = ProfesorController(db)
        self.root = ctk.CTk()
        self.root.title("Gestión de Profesores")
        
        # Configurar el tema
        ctk.set_appearance_mode(tema_actual)
        self.tema_actual = tema_actual
        
        # Configuración de cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.regresar_menu_principal)
        
        # Configurar tamaño de ventana
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        self.root.geometry(f"{ancho_pantalla}x{alto_pantalla}")
        self.root.state("zoomed")
        
        # Título
        self.titulo = ctk.CTkLabel(
            self.root,
            text="Gestión de Profesores",
            font=("Arial", 20, "bold")
        )
        self.titulo.pack(pady=20)
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Frame para la tabla
        self.frame_tabla = ctk.CTkFrame(self.frame_principal)
        self.frame_tabla.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        # Tabla de profesores
        self.tabla = ttk.Treeview(
            self.frame_tabla,
            columns=("ID", "Nombre", "Apellido", "Correo", "Telefono", "Especialidad"),
            show="headings"
        )
        self.tabla.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla.yview)
        scrollbar.pack(side="right", fill="y")
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        # Configurar encabezados
        self.tabla.heading("ID", text="ID Docente")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Apellido", text="Apellido")
        self.tabla.heading("Correo", text="Correo")
        self.tabla.heading("Telefono", text="Teléfono")
        self.tabla.heading("Especialidad", text="Especialidad")
        
        # Ajustar anchos de columna
        self.tabla.column("ID", width=100)
        self.tabla.column("Nombre", width=200)
        self.tabla.column("Apellido", width=200)
        self.tabla.column("Correo", width=250)
        self.tabla.column("Telefono", width=150)
        self.tabla.column("Especialidad", width=200)
        
        # Frame para botones
        self.frame_botones = ctk.CTkFrame(self.frame_principal, width=250)
        self.frame_botones.pack(side="right", fill="y", padx=(0, 20))
        self.frame_botones.pack_propagate(False)
        
        # Botones
        self.btn_registrar = ctk.CTkButton(
            self.frame_botones,
            text="Registrar Profesor",
            command=self.registrar_docente,
            width=200
        )
        self.btn_registrar.pack(pady=10, padx=10, fill="x")
        
        self.btn_actualizar = ctk.CTkButton(
            self.frame_botones,
            text="Actualizar Profesor",
            command=self.actualizar_docente,
            width=200
        )
        self.btn_actualizar.pack(pady=10, padx=10, fill="x")
        
        self.btn_eliminar = ctk.CTkButton(
            self.frame_botones,
            text="Eliminar Profesor",
            command=self.eliminar_docente,
            width=200
        )
        self.btn_eliminar.pack(pady=10, padx=10, fill="x")
        
        self.btn_ver_cursos = ctk.CTkButton(
            self.frame_botones,
            text="Ver Cursos del Profesor",
            command=self.ver_cursos_docente,
            width=200
        )
        self.btn_ver_cursos.pack(pady=10, padx=10, fill="x")
        
        self.btn_cambiar_tema = ctk.CTkButton(
            self.frame_botones,
            text="Cambiar Tema",
            command=self.cambiar_tema,
            width=200
        )
        self.btn_cambiar_tema.pack(pady=10, padx=10, fill="x")
        
        # Botón regresar
        self.btn_regresar = ctk.CTkButton(
            self.frame_botones,
            text="Regresar al Menú Principal",
            command=self.regresar_menu_principal,
            width=200,
            fg_color="#FF5555",  
            hover_color="#FF3333"
        )
        self.btn_regresar.pack(pady=20)
        
        # Cargar datos iniciales
        self.cargar_datos_tabla()
    
    def cargar_datos_tabla(self):
        try:
            # Obtener lista de profesores
            profesores = self.profesor_controller.listar_profesores()
            
            # Limpiar tabla
            for row in self.tabla.get_children():
                self.tabla.delete(row)
            
            # Insertar profesores
            for profesor in profesores:
                self.tabla.insert("", "end", values=(
                    profesor.id_profesor,
                    profesor.nombre,
                    profesor.apellido,
                    profesor.correo,
                    profesor.telefono,
                    profesor.especialidad
                ))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {str(e)}")
    
    def registrar_docente(self):
        ventana_registro = VentanaRegistroDocente(
            self.root,
            self.db,
            self.cargar_datos_tabla
        )
        ventana_registro.grab_set()
    
    def actualizar_docente(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un profesor para actualizar")
            return
        
        # Obtener datos del profesor seleccionado
        profesor_id = self.tabla.item(seleccion[0])['values'][0]
        
        # Abrir ventana de actualización
        ventana_actualizar = VentanaActualizarProfesor(
            self.root,
            self.db,
            profesor_id,
            self.cargar_datos_tabla
        )
        ventana_actualizar.grab_set()
    
    def eliminar_docente(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un profesor para eliminar")
            return
        
        profesor_id = self.tabla.item(seleccion[0])['values'][0]
        profesor_nombre = self.tabla.item(seleccion[0])['values'][1]
        profesor_apellido = self.tabla.item(seleccion[0])['values'][2]
        
        # Confirmar eliminación
        if messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de eliminar al profesor {profesor_nombre} {profesor_apellido}?"
        ):
            try:
                self.profesor_controller.eliminar_profesor_por_id(profesor_id)
                messagebox.showinfo("Éxito", "Profesor eliminado correctamente")
                self.cargar_datos_tabla()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar el profesor: {str(e)}")
    
    def ver_cursos_docente(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un profesor para ver sus cursos")
            return
        
        # Obtener datos del profesor seleccionado
        profesor_id = self.tabla.item(seleccion[0])['values'][0]
        profesor_nombre = self.tabla.item(seleccion[0])['values'][1]
        profesor_apellido = self.tabla.item(seleccion[0])['values'][2]
        
        # Abrir ventana de cursos
        ventana_cursos = VentanaCursosDocente(
            self.root,
            self.db,
            profesor_id,
            profesor_nombre,
            profesor_apellido
        )
        ventana_cursos.grab_set()
    
    def cambiar_tema(self):
        if self.tema_actual == "Light":
            ctk.set_appearance_mode("Dark")
            self.tema_actual = "Dark"
            self.btn_cambiar_tema.configure(text="☀️ Cambiar Tema")
        else:
            ctk.set_appearance_mode("Light")
            self.tema_actual = "Light"
            self.btn_cambiar_tema.configure(text="🌙 Cambiar Tema")
    
    def regresar_menu_principal(self):
        self.root.destroy()
        from view.view_Tkinter.vista_principal.menu_principal import VentanaMenuPrincipal
        app = VentanaMenuPrincipal(db=self.db)
        app.iniciar_ventana(self.tema_actual)