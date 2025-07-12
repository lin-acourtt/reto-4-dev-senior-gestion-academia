import customtkinter as ctk
from tkinter import ttk, messagebox
from config.appearance import centrar_ventana
from config.database import Database

from controllers.matricula_controller import MatriculaController
from controllers.estudiante_controller import EstudianteController
from controllers.curso_controller import CursoController

from .frame_header import FrameHeader
from .frame_tabla_matriculas import FrameTablaMatriculas
from .frame_footer import FrameFooter

from .ventana_crear_matricula import VentanaCrearMatricula
from .ventana_borrar_matricula import VentanaBorrarMatricula
from .ventana_buscar_matricula import VentanaBuscarMatricula

from view.view_Tkinter.vista_msgbox.msgbox_library import msg_no_hay_seleccion, msg_hay_otra_ventana_abierta

class VentanaMenuMatricula(ctk.CTkToplevel):

    def __init__(self, db: Database = None):
        """
            Constructor, requiere de:
            - db: Base de datos, objeto tipo Database
        """
        super().__init__()
        # El método constructor asegura que el atributo "db" sea de tipo "Database""
        self.db = db
        self.controlador_matricula = MatriculaController(self.db)
        #self.controlador_profesor = ProfesorController(self.db)
        self.controlador_estudiante = EstudianteController(self.db)
        self.controlador_curso = CursoController(self.db)

    def iniciar_ventana(self, tema_actual):    
        """
            Inicia la ventana menú matricula, requiere de:
            - tema_actual: tema con el que se abrirá la ventana
        """
        self.title("Gestión de matriculas - Academia")
        
        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)
        self.tema_actual = tema_actual
        centrar_ventana(self, proporcion=0.7)
        
        # Configuración de restricciones de la ventana
        self.resizable(True, True)

        # Crear el frame Header - Contiene título y botones de cambiar tema y regresar a la ventana principal
        self.frame_header = FrameHeader(self)
        self.frame_header.pack(fill="x", padx=20, pady=10)

        # Crear el frame de tabla matriculas - Contiene la tabla y el scroller vertical
        self.frame_tabla_matriculas = FrameTablaMatriculas(self)
        self.frame_tabla_matriculas.pack(fill="both", expand=True, padx=20, pady=10)

        # Crear el frame para el Footer - Contiene los botones de acción
        self.frame_footer = FrameFooter(self)
        self.frame_footer.pack(fill='x',padx=20, pady=10)
        
        # Ejecuta la función "regresar_menu_principal", para poder regresar en caso de que se cierre la ventana con el botón cerrar
        self.protocol("WM_DELETE_WINDOW",self.regresar_menu_principal)

        # Trackear estado (abiertas o cerradas) de ventanas de operaciones
        # Al inicial menú de matriculas, todas las ventanas están cerradas
        # Estas se usan para evitar abrir más de una ventana para cada operación
        self.ventana_nueva_matricula_esta_abierta = False
        self.ventana_actualizacion_esta_abierta = False
        self.ventana_borrar_esta_abierta = False
        self.ventana_buscar_esta_abierta = False

        self.mainloop()

    def obtener_lista_matriculas(self):
        """
            Obtiene lista de matriculas. "matriculas" es una lista de objetos tipo "matricula", atributos:
            - id_matricula
            - nombre
            - profesor
            - num_estudiantes
            - matriculas
            - descripcion
            - duracion_horas
        """
        try: 
            matriculas, nombre_estudiantes, nombre_cursos = self.controlador_matricula.listar_matriculas()
            if matriculas and nombre_estudiantes and nombre_cursos:
                return matriculas, nombre_estudiantes, nombre_cursos
            else:
                raise ValueError
        except ValueError as e:
            print("Valores inválidos")
        except Exception as e:
            print(f"Error al listar los matriculas: {str(e)}")
        
        
        # matriculas: es una lista de objetos tipo "matricula", atributos:
        # id_matricula
        # curso_id
        # dia_semana
        # hora_inicio
        # hora_fin
        
        # cursos: es una lista con los nombres de los cursos correspondientes a los curso_id en matriculas

    def obtener_listas_cursos(self):
        """
            Obtiene lista de cursos. "cursos" es una lista de objetos tipo "Cursos", atributos:
            - id_profesor
            - nombre
            - apellido
            - correo
            - telefono
        """
        try: 
            cursos = self.controlador_curso.listar_cursos()
            
            if cursos:
                
                detalles_cursos = []
                # detalles cursos es una lista con IDs y nombres como:
                # [
                # [id1, curso1]
                # [id2, curso2]
                # ...
                # ]

                for c in cursos:
                    detalles_cursos.append([c.id_curso,c.nombre])

                lista_cursos = [
                    f"ID: {c[0]} - {c[1]}"
                    for c in detalles_cursos
                ]
                    
                return cursos, detalles_cursos, lista_cursos
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
    
    def obtener_listas_estudiantes(self):
        """
            Obtiene lista de estudiantes. "estudiantes" es una lista de objetos tipo "Estudiante", atributos:
            - id_profesor
            - nombre
            - apellido
            - correo
            - telefono
        """
        try: 
            estudiantes = self.controlador_estudiante.listar_estudiantes()
            
            if estudiantes:
                
                detalles_estudiantes = []
                # detalles cursos es una lista con IDs y nombres como:
                # [
                # [id1, nombre1, apellido1]
                # [id2, nombre3, apellido2]
                # ...
                # ]

                for e in estudiantes:
                    detalles_estudiantes.append([e.id_estudiante,e.nombre,e.apellido])

                lista_estudiantes = [
                    f"ID: {e[0]} - {e[1]} {e[2]}"
                    for e in detalles_estudiantes
                ]
                    
                return estudiantes, detalles_estudiantes, lista_estudiantes
            else:
                raise ValueError
        except ValueError as e:
            print("Valores inválidos")
        except Exception as e:
            print(f"Error al listar los profesores: {str(e)}")
        
    def abrir_ventana_nuevo_matricula(self):
        """
            Abrir la ventana para el registro de un nuevo matricula
        """
        if self.ventana_nueva_matricula_esta_abierta == False:
            # Si la ventana de nuevo matricula está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_nueva_matricula_esta_abierta = True
            # Abrir la ventana
            self.ventana_nuevo_matricula = VentanaCrearMatricula(parent=self, tipo=1)
            self.ventana_nuevo_matricula.mainloop()
        else:
            # Si la ventana de registro está abierta, hacerle focus
            self.ventana_nuevo_matricula.focus_force()

    def abrir_ventana_actualizacion(self):
        """
            Abrir la ventana para la actualización de datos de matricula
        """
        # Si no hay nada seleccionado, se indica que se debe seleccionar un item primero
        seleccion = self.frame_tabla_matriculas.tabla_matriculas.selection()
        if not seleccion:
            msg_no_hay_seleccion("matricula","actualizar")
            #messagebox.showwarning("Advertencia", "Por favor, seleccione un profesor para actualizar")
            return
        
        if self.ventana_actualizacion_esta_abierta == False:
            # Si la ventana de actualización está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_actualizacion_esta_abierta = True
            # Abrir la ventana
            self.ventana_actualizacion = VentanaCrearMatricula(parent=self, tipo=2)
            self.ventana_actualizacion.mainloop()
        else:
            # Si la ventana de actualización está abierta, hacerle focus y actualizar los campos si se cambió la selección
            self.ventana_actualizacion.actualizar_informacion_campos()
            self.ventana_actualizacion.focus_force()   
          
    def abrir_ventana_borrar(self):
        """
            Abrir la ventana para la eliminación de matriculas
        """
        
        # Si no hay nada seleccionado, se indica que se debe seleccionar un item primero
        seleccion = self.frame_tabla_matriculas.tabla_matriculas.selection()
        if not seleccion:
            msg_no_hay_seleccion("matricula","borrar")
            return
        
        if self.ventana_borrar_esta_abierta == False:
            # Si la ventana de borrar está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_borrar_esta_abierta = True
            # Abrir la ventana
            self.ventana_borrar = VentanaBorrarMatricula(parent=self)
            self.ventana_borrar.mainloop()
        else:
            # Cerrar la que ya está abierta, y volverla a abrir con los nuevos datos
            self.ventana_borrar.destroy()
            self.ventana_borrar = VentanaBorrarMatricula(parent=self)
            self.ventana_borrar.mainloop()
    
    def abrir_ventana_buscar(self):
        """
            Abrir la ventana para buscar curso por iD
        """

        if self.ventana_buscar_esta_abierta == False:
            # Abrir la ventana
            self.ventana_buscar = VentanaBuscarMatricula(parent=self)
            #self.ventana_buscar.mainloop()
        else:
            # Si la ventana de búsqueda está abierta, hacerle focus
            msg_hay_otra_ventana_abierta("resultados")
        
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

if __name__ == "__main__":
    db = Database()
    app = VentanaMenuMatricula(db)
    app.iniciar_ventana()
