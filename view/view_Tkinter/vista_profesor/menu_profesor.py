import customtkinter as ctk

# from tkinter import ttk

from config.database import Database
from config.appearance import centrar_ventana

from controllers.profesor_controller import ProfesorController

from mysql.connector import IntegrityError

from .frame_header import FrameHeader
from .frame_tabla_profesores import FrameTablaProfesores
from .frame_footer import FrameFooter
from .ventana_registrar_profesor import VentanaRegistrarProfesor
from .ventana_actualizar_profesor import VentanaActualizarProfesor
from .ventana_borrar_profesor import VentanaBorrarProfesor
from .ventana_buscar_profesor import VentanaBuscarProfesor
from .ventana_cursos_profesor import VentanaCursosProfesor
from view.view_Tkinter.vista_msgbox.msgbox_library import msg_no_hay_seleccion, msg_hay_otra_ventana_abierta

class VentanaMenuProfesor(ctk.CTkToplevel):

    def __init__(self, db: Database = None):
        """
            Constructor, requiere de:
            - db: Base de datos, objeto tipo Database
        """
        super().__init__()
        # El método constructor asegura que el atributo "db" sea de tipo "Database""
        self.db = db
        self.controlador_profesor = ProfesorController(self.db)

    def iniciar_ventana(self, tema_actual):    
        """
            Inicia la ventana menú profesor, requiere de:
            - tema_actual: tema con el que se abrirá la ventana
        """
        self.title("Gestión de profesores")
        
        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)
        self.tema_actual = tema_actual
        centrar_ventana(self, proporcion=0.7)
        
        # Configuración de restricciones de la ventana
        self.resizable(False, False)

        # Crear el frame Header - Contiene título y botones de cambiar tema y regresar a la ventana principal
        self.frame_header = FrameHeader(self)
        self.frame_header.pack(fill="x", padx=20, pady=10)

        # Crear el frame de tabla profesores - Contiene la tabla y el scroller vertical
        self.frame_tabla_profesores = FrameTablaProfesores(self)
        self.frame_tabla_profesores.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear el frame para el Footer - Contiene los botones de acción
        self.frame_footer = FrameFooter(self)
        self.frame_footer.pack(padx=20, pady=10)
        
        # Ejecuta la función "regresar_menu_principal", para poder regresar en caso de que se cierre la ventana con el botón cerrar
        self.protocol("WM_DELETE_WINDOW",self.regresar_menu_principal)

        # Trackear estado (abiertas o cerradas) de ventanas de operaciones
        # Al inicial menú de profesor, todas las ventanas están cerradas
        # Estas se usan para evitar abrir más de una ventana para cada operación
        self.ventana_registro_esta_abierta = False
        self.ventana_actualizacion_esta_abierta = False
        self.ventana_borrar_esta_abierta = False
        self.ventana_buscar_esta_abierta = False
        self.ventana_cursos_esta_abierta = False
        #self.mainloop()


    def obtener_lista_profesores(self):
        """
            Obtiene lista de profesores. "profesores" es una lista de objetos tipo "Profesor", atributos:
            - id_profesor
            - nombre
            - apellido
            - correo
            - telefono
        """
        try: 
            profesores = self.controlador_profesor.listar_profesores()
            if profesores:
                return profesores
            else:
                raise ValueError
        except ValueError as e:
            print("Valores inválidos")
        except Exception as e:
            print(f"Error al listar los profesores: {str(e)}")
        
        # profesores: es una lista de objetos tipo "Profesor", atributos:
        # id_profesor
        # nombre
        # apellido
        # correo
        # telefono
    
    def abrir_ventana_registro(self):
        """
            Abrir la ventana para el registro de profesores
        """
        if self.ventana_registro_esta_abierta == False:
            # Si la ventana de registro está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_registro_esta_abierta = True
            # Abrir la ventana
            self.ventana_registro = VentanaRegistrarProfesor(parent=self)
            self.ventana_registro.mainloop()
        else:
            # Si la ventana de registro está abierta, hacerle focus
            self.ventana_registro.focus_force()
    
    def abrir_ventana_actualizacion(self):
        """
            Abrir la ventana para la actualización de datos de profesores
        """
        # Si no hay nada seleccionado, se indica que se debe seleccionar un item primero
        seleccion = self.frame_tabla_profesores.tabla_profesores.selection()
        if not seleccion:
            msg_no_hay_seleccion("profesor","actualizar")
            #messagebox.showwarning("Advertencia", "Por favor, seleccione un profesor para actualizar")
            return
        
        if self.ventana_actualizacion_esta_abierta == False:
            # Si la ventana de actualización está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_actualizacion_esta_abierta = True
            # Abrir la ventana
            self.ventana_actualizacion = VentanaActualizarProfesor(parent=self)
            self.ventana_actualizacion.mainloop()
        else:
            # Si la ventana de actualización está abierta, hacerle focus y actualizar los campos si se cambió la selección
            self.ventana_actualizacion.actualizar_informacion_campos()
            self.ventana_actualizacion.focus_force()   
    
    def abrir_ventana_borrar(self):
        """
            Abrir la ventana para la eliminación de profesores
        """
        
        # Si no hay nada seleccionado, se indica que se debe seleccionar un item primero
        seleccion = self.frame_tabla_profesores.tabla_profesores.selection()
        if not seleccion:
            msg_no_hay_seleccion("profesor","borrar")
            #messagebox.showwarning("Advertencia", "Por favor, seleccione un profesor para actualizar")
            return
        
        if self.ventana_borrar_esta_abierta == False:
            # Si la ventana de borrar está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_borrar_esta_abierta = True
            # Abrir la ventana
            self.ventana_borrar = VentanaBorrarProfesor(parent=self)
            self.ventana_borrar.mainloop()
        else:
            # Si la ventana de borrar está abierta, hacerle focus
            self.ventana_borrar.focus_force()  

    def abrir_ventana_buscar(self):
        """
            Abrir la ventana para buscar profesor por iD
        """
        if self.ventana_buscar_esta_abierta == False:
            # Abrir la ventana
            self.ventana_buscar = VentanaBuscarProfesor(parent=self)
        else:
            # Si la ventana de búsqueda está abierta, hacerle focus
            msg_hay_otra_ventana_abierta("resultados")
    
    def abrir_ventana_cursos_profesor(self):
        """
            Abrir la ventana que muestra los cursos asociados a un profesor
        """

        # Si no hay nada seleccionado, se indica que se debe seleccionar un item primero
        seleccion = self.frame_tabla_profesores.tabla_profesores.selection()
        if not seleccion:
            msg_no_hay_seleccion("profesor","ver sus cursos")
            #messagebox.showwarning("Advertencia", "Por favor, seleccione un profesor para actualizar")
            return
        
        if self.ventana_cursos_esta_abierta == False:
            # Si la ventana de actualización está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_cursos_esta_abierta = True
            # Abrir la ventana
            self.ventana_cursos = VentanaCursosProfesor(parent=self)
            self.ventana_cursos.mainloop()
        else:
            # Si la ventana de cursos está abierta, hacerle focus 
            self.ventana_cursos.focus_force()  

    def cambiar_tema(self):
        """
            Método para cambiar el estilo de la ventana
        """
        if self.tema_actual == "Light":
            ctk.set_appearance_mode("Dark")
            self.tema_actual = "Dark"
            self.frame_header.frame_botones_header.btn_cambiar_tema.configure(text="☀️ Cambiar Tema")
        else:
            ctk.set_appearance_mode("Light")
            self.tema_actual = "Light"
            self.frame_header.frame_botones_header.btn_cambiar_tema.configure(text="🌙 Cambiar Tema")

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