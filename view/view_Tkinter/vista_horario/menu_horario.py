import customtkinter as ctk
from tkinter import ttk, messagebox
from config.appearance import centrar_ventana
from config.database import Database

from controllers.horario_controller import HorarioController
from controllers.profesor_controller import ProfesorController
from controllers.curso_controller import CursoController

from .frame_header import FrameHeader
from .frame_tabla_horarios import FrameTablaHorarios
from .frame_footer import FrameFooter

from .ventana_crear_horario import VentanaCrearHorario
from .ventana_borrar_horario import VentanaBorrarHorario
from .ventana_buscar_horario import VentanaBuscarHorario


from view.view_Tkinter.vista_msgbox.msgbox_library import msg_no_hay_seleccion, msg_hay_otra_ventana_abierta

class VentanaMenuHorario(ctk.CTkToplevel):

    def __init__(self, db: Database = None):
        """
            Constructor, requiere de:
            - db: Base de datos, objeto tipo Database
        """
        super().__init__()
        # El método constructor asegura que el atributo "db" sea de tipo "Database""
        self.db = db
        self.controlador_horario = HorarioController(self.db)
        #self.controlador_profesor = ProfesorController(self.db)
        self.controlador_curso = CursoController(self.db)

    def iniciar_ventana(self, tema_actual):    
        """
            Inicia la ventana menú horario, requiere de:
            - tema_actual: tema con el que se abrirá la ventana
        """
        self.title("Gestión de horarios - Academia")
        
        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)
        self.tema_actual = tema_actual
        centrar_ventana(self, proporcion=0.7)
        
        # Configuración de restricciones de la ventana
        self.resizable(True, True)

        # Crear el frame Header - Contiene título y botones de cambiar tema y regresar a la ventana principal
        self.frame_header = FrameHeader(self)
        self.frame_header.pack(fill="x", padx=20, pady=10)

        # Crear el frame de tabla horarios - Contiene la tabla y el scroller vertical
        self.frame_tabla_horarios = FrameTablaHorarios(self)
        self.frame_tabla_horarios.pack(fill="both", expand=True, padx=20, pady=10)

        # Crear el frame para el Footer - Contiene los botones de acción
        self.frame_footer = FrameFooter(self)
        self.frame_footer.pack(fill="x",padx=20, pady=10)
        
        # Ejecuta la función "regresar_menu_principal", para poder regresar en caso de que se cierre la ventana con el botón cerrar
        self.protocol("WM_DELETE_WINDOW",self.regresar_menu_principal)

        # Trackear estado (abiertas o cerradas) de ventanas de operaciones
        # Al inicial menú de horarios, todas las ventanas están cerradas
        # Estas se usan para evitar abrir más de una ventana para cada operación
        self.ventana_nuevo_horario_esta_abierta = False
        self.ventana_actualizacion_esta_abierta = False
        self.ventana_borrar_esta_abierta = False
        self.ventana_buscar_esta_abierta = False

        self.mainloop()

    def obtener_lista_horarios(self):
        """
            Obtiene lista de horarios. "horarios" es una lista de objetos tipo "horario", atributos:
            - id_horario
            - nombre
            - profesor
            - num_estudiantes
            - horarios
            - descripcion
            - duracion_horas
        """
        try: 
            horarios, cursos = self.controlador_horario.listar_horarios()
            if horarios and cursos:
                return horarios, cursos
            else:
                raise ValueError
        except ValueError as e:
            print("Valores inválidos")
        except Exception as e:
            print(f"Error al listar los horarios: {str(e)}")
        
        
        # horarios: es una lista de objetos tipo "horario", atributos:
        # id_horario
        # curso_id
        # dia_semana
        # hora_inicio
        # hora_fin
        
        # cursos: es una lista con los nombres de los cursos correspondientes a los curso_id en horarios

    def obtener_listas_cursos(self):
        # Borrar
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
    

    def abrir_ventana_nuevo_horario(self):
        """
            Abrir la ventana para el registro de un nuevo horario
        """
        if self.ventana_nuevo_horario_esta_abierta == False:
            # Si la ventana de nuevo horario está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_nuevo_horario_esta_abierta = True
            # Abrir la ventana
            self.ventana_nuevo_horario = VentanaCrearHorario(parent=self, tipo=1)
            self.ventana_nuevo_horario.mainloop()
        else:
            # Si la ventana de registro está abierta, hacerle focus
            self.ventana_nuevo_horario.focus_force()

    def abrir_ventana_actualizacion(self):
        """
            Abrir la ventana para la actualización de datos de horario
        """
        # Si no hay nada seleccionado, se indica que se debe seleccionar un item primero
        seleccion = self.frame_tabla_horarios.tabla_horarios.selection()
        if not seleccion:
            msg_no_hay_seleccion("horario","actualizar")
            #messagebox.showwarning("Advertencia", "Por favor, seleccione un profesor para actualizar")
            return
        
        if self.ventana_actualizacion_esta_abierta == False:
            # Si la ventana de actualización está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_actualizacion_esta_abierta = True
            # Abrir la ventana
            self.ventana_actualizacion = VentanaCrearHorario(parent=self, tipo=2)
            self.ventana_actualizacion.mainloop()
        else:
            # Si la ventana de actualización está abierta, hacerle focus y actualizar los campos si se cambió la selección
            self.ventana_actualizacion.actualizar_informacion_campos()
            self.ventana_actualizacion.focus_force()   
          
    def abrir_ventana_borrar(self):
        """
            Abrir la ventana para la eliminación de horarios
        """
        
        # Si no hay nada seleccionado, se indica que se debe seleccionar un item primero
        seleccion = self.frame_tabla_horarios.tabla_horarios.selection()
        if not seleccion:
            msg_no_hay_seleccion("horario","borrar")
            return
        
        if self.ventana_borrar_esta_abierta == False:
            # Si la ventana de borrar está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_borrar_esta_abierta = True
            # Abrir la ventana
            self.ventana_borrar = VentanaBorrarHorario(parent=self)
            self.ventana_borrar.mainloop()
        else:
            # Cerrar la que ya está abierta, y volverla a abrir con los nuevos datos
            self.ventana_borrar.destroy()
            self.ventana_borrar = VentanaBorrarHorario(parent=self)
            self.ventana_borrar.mainloop()
    
    def abrir_ventana_buscar(self):
        """
            Abrir la ventana para buscar curso por iD
        """

        if self.ventana_buscar_esta_abierta == False:
            # Abrir la ventana
            self.ventana_buscar = VentanaBuscarHorario(parent=self)
            #self.ventana_buscar.mainloop()
        else:
            # Si la ventana de búsqueda está abierta, hacerle focus
            msg_hay_otra_ventana_abierta("resultados")

    def abrir_ventana_secundaria(self, titulo, clase_vista):
        # Queda pendiente
        """Abre una ventana secundaria y la configura para que aparezca por encima"""
        ventana = ctk.CTkToplevel(self)
        ventana.title(titulo)
        ventana.geometry("600x500")
        ventana.transient(self)  # Hace que la ventana sea transitoria de la principal
        ventana.grab_set()  # Hace que la ventana sea modal
        centrar_ventana(ventana)
        
        # Crear instancia de la vista pasando la ventana y la conexión a la base de datos
        vista = clase_vista(ventana, self.db)
        
        # Configurar el tema
        ctk.set_appearance_mode(self.tema_actual)
        
        return vista
            
    def abrir_matricular_estudiante(self):
        # Queda pendiente
        return
        """Abre la ventana para matricular un estudiante en un horario"""
        self.abrir_ventana_secundaria("Matricular Estudiante", VistaMatricularEstudiante)
        
    def abrir_consultar_matriculas(self):
        # Queda pendiente
        return
        """Abre la ventana para consultar las matrículas"""
        self.abrir_ventana_secundaria("Consultar Matrículas", VistaConsultarMatriculas)
        
    def abrir_consultar_horarios(self):
        # Queda pendiente
        return
        """Abre la ventana para consultar los horarios de los horarios"""
        self.abrir_ventana_secundaria("Consultar Horarios", VistaConsultarHorarios)
        
    def abrir_eliminar_matricula(self):
        # Queda pendiente
        return
        """Abre la ventana para eliminar una matrícula"""
        self.abrir_ventana_secundaria("Eliminar Matrícula", VistaEliminarMatricula)

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
    app = VentanaMenuHorario(db)
    app.iniciar_ventana()
