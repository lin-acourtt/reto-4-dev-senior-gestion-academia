import customtkinter as ctk
from tkinter import ttk, messagebox
from config.appearance import centrar_ventana
from config.database import Database

from controllers.curso_controller import CursoController
from controllers.profesor_controller import ProfesorController
from controllers.horario_controller import HorarioController
from controllers.matricula_controller import MatriculaController

from .frame_header import FrameHeader
from .frame_tabla_cursos import FrameTablaCursos
from .frame_footer import FrameFooter
from .vista_crear_curso import VistaCrearCurso
from .vista_listar_cursos import VistaListarCursos
from .vista_matricular_estudiante import VistaMatricularEstudiante
from .vista_consultar_matriculas import VistaConsultarMatriculas
from .vista_consultar_horarios import VistaConsultarHorarios
from .vista_eliminar_matricula import VistaEliminarMatricula
from .vista_consultar_estudiantes_curso import VistaConsultarEstudiantesCurso

from .ventana_crear_curso import VentanaCrearCurso
from .ventana_borrar_curso import VentanaBorrarCurso
from .ventana_buscar_curso import VentanaBuscarCurso
from .ventana_registrar_horario import VentanaRegistrarHorario
from view.view_Tkinter.vista_tablas_resultados.ventana_tabla_resultados import VentanaTablaResultados

from view.view_Tkinter.vista_msgbox.msgbox_library import msg_no_hay_seleccion, msg_hay_otra_ventana_abierta, msg_error_inesperado

class VentanaMenuCurso(ctk.CTkToplevel):

    def __init__(self, db: Database = None):
        """
            Constructor, requiere de:
            - db: Base de datos, objeto tipo Database
        """
        super().__init__()
        # El método constructor asegura que el atributo "db" sea de tipo "Database""
        self.db = db
        self.controlador_curso = CursoController(self.db)
        self.controlador_profesor = ProfesorController(self.db)
        self.controlador_horario = HorarioController(self.db)
        self.controlador_matricula = MatriculaController(self.db)

    def iniciar_ventana(self, tema_actual):    
        """
            Inicia la ventana menú curso, requiere de:
            - tema_actual: tema con el que se abrirá la ventana
        """
        self.title("Gestión de Cursos - Academia")
        
        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)
        self.tema_actual = tema_actual
        centrar_ventana(self, proporcion=0.7)
        
        # Configuración de restricciones de la ventana
        self.resizable(False, False)

        # Crear el frame Header - Contiene título y botones de cambiar tema y regresar a la ventana principal
        self.frame_header = FrameHeader(self)
        self.frame_header.pack(fill="x", padx=20, pady=10)

        # Crear el frame de tabla cursos - Contiene la tabla y el scroller vertical
        self.frame_tabla_cursos = FrameTablaCursos(self)
        self.frame_tabla_cursos.pack(fill="both", expand=True, padx=20, pady=10)

        # Crear el frame para el Footer - Contiene los botones de acción
        self.frame_footer = FrameFooter(self)
        self.frame_footer.pack(padx=20, pady=10)
        
        # Ejecuta la función "regresar_menu_principal", para poder regresar en caso de que se cierre la ventana con el botón cerrar
        self.protocol("WM_DELETE_WINDOW",self.regresar_menu_principal)

        # Trackear estado (abiertas o cerradas) de ventanas de operaciones
        # Al inicial menú de cursos, todas las ventanas están cerradas
        # Estas se usan para evitar abrir más de una ventana para cada operación
        self.ventana_nuevo_curso_esta_abierta = False
        self.ventana_actualizacion_esta_abierta = False
        self.ventana_borrar_esta_abierta = False
        self.ventana_buscar_esta_abierta = False
        self.ventana_registrar_horario_esta_abierta = False
        self.ventana_consultar_horarios_por_curso_esta_abierta = False
        self.ventana_consultar_estudiantes_por_curso_esta_abierta = False

        self.mainloop()

    def obtener_lista_cursos(self):
        """
            Obtiene lista de cursos. "Cursos" es una lista de objetos tipo "Curso", atributos:
            - id_curso
            - nombre
            - profesor
            - num_estudiantes
            - horarios
            - descripcion
            - duracion_horas
        """
        try: 
            cursos = self.controlador_curso.listar_cursos()
            if cursos:
                return cursos
            else:
                raise ValueError
        except ValueError as e:
            print("Valores inválidos")
        except Exception as e:
            print(f"Error al listar los cursos: {str(e)}")
        
        
        # cursos: es una lista de objetos tipo "Curso", atributos:
        # id_curso
        # nombre
        # profesor
        # num_estudiantes
        # horarios
        # descripcion
        # duracion_horas

    def obtener_listas_profesores(self):
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
                
                detalles_profesor = []
                # detalles profesor es una lista con IDs y nombres como:
                # [
                # [id1, nombre1, apellido1]
                # [id2, nombre2, apellido2]
                # ...
                # ]
                
                for p in profesores:
                    detalles_profesor.append([p.id_profesor,p.nombre,p.apellido])

                lista_profesores = [
                    f"ID: {prof[0]} - {prof[1]} {prof[2]}"
                    for prof in detalles_profesor
                ]
                    
                return profesores, detalles_profesor, lista_profesores
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
    

    def abrir_ventana_nuevo_curso(self):
        """
            Abrir la ventana para el registro de un nuevo curso
        """
        if self.ventana_nuevo_curso_esta_abierta == False:
            # Si la ventana de nuevo curso está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_nuevo_curso_esta_abierta = True
            # Abrir la ventana
            self.ventana_nuevo_curso = VentanaCrearCurso(parent=self, tipo=1)
            self.ventana_nuevo_curso.mainloop()
        else:
            # Si la ventana de registro está abierta, hacerle focus
            self.ventana_nuevo_curso.focus_force()

    def abrir_ventana_actualizacion(self):
        """
            Abrir la ventana para la actualización de datos de curso
        """
        # Si no hay nada seleccionado, se indica que se debe seleccionar un item primero
        seleccion = self.frame_tabla_cursos.tabla_cursos.selection()
        if not seleccion:
            msg_no_hay_seleccion("curso","actualizar")
            #messagebox.showwarning("Advertencia", "Por favor, seleccione un profesor para actualizar")
            return
        
        if self.ventana_actualizacion_esta_abierta == False:
            # Si la ventana de actualización está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_actualizacion_esta_abierta = True
            # Abrir la ventana
            self.ventana_actualizacion = VentanaCrearCurso(parent=self, tipo=2)
            self.ventana_actualizacion.mainloop()
        else:
            # Si la ventana de actualización está abierta, hacerle focus y actualizar los campos si se cambió la selección
            self.ventana_actualizacion.actualizar_informacion_campos()
            self.ventana_actualizacion.focus_force()   
          
    def abrir_ventana_borrar(self):
        """
            Abrir la ventana para la eliminación de cursos
        """
        
        # Si no hay nada seleccionado, se indica que se debe seleccionar un item primero
        seleccion = self.frame_tabla_cursos.tabla_cursos.selection()
        if not seleccion:
            msg_no_hay_seleccion("Curso","borrar")
            return
        
        if self.ventana_borrar_esta_abierta == False:
            # Si la ventana de borrar está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_borrar_esta_abierta = True
            # Abrir la ventana
            self.ventana_borrar = VentanaBorrarCurso(parent=self)
            self.ventana_borrar.mainloop()
        else:
            # Si la ventana de borrar está abierta, hacerle focus
            self.ventana_borrar.focus_force()  

    def abrir_ventana_buscar(self):
        """
            Abrir la ventana para buscar curso por iD
        """

        if self.ventana_buscar_esta_abierta == False:
            # Abrir la ventana
            self.ventana_buscar = VentanaBuscarCurso(parent=self)
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
        """Abre la ventana para matricular un estudiante en un curso"""
        self.abrir_ventana_secundaria("Matricular Estudiante", VistaMatricularEstudiante)
        
    def abrir_consultar_matriculas(self):
        # Queda pendiente
        """Abre la ventana para consultar las matrículas"""
        self.abrir_ventana_secundaria("Consultar Matrículas", VistaConsultarMatriculas)
        
    def abrir_consultar_horarios(self):
        """Abre la ventana para consultar los horarios de todos los cursos"""
        self.abrir_ventana_secundaria("Consultar Horarios", VistaConsultarHorarios)

    def abrir_eliminar_matricula(self):
        # Queda pendiente
        """Abre la ventana para eliminar una matrícula"""
        self.abrir_ventana_secundaria("Eliminar Matrícula", VistaEliminarMatricula)

    def abrir_ventana_registrar_horario(self):
        """
            Abre la ventana para registrar horarios de cursos
        """
        # Verificar si hay un curso seleccionado
        seleccion = self.frame_tabla_cursos.tabla_cursos.selection()
        if not seleccion:
            msg_no_hay_seleccion("curso", "registrar horario")
            return

        if self.ventana_registrar_horario_esta_abierta == False:
            # Si la ventana de registro de horario está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_registrar_horario_esta_abierta = True
            # Abrir la ventana
            self.ventana_registrar_horario = VentanaRegistrarHorario(parent=self, db=self.db)
            self.ventana_registrar_horario.mainloop()
        else:
            # Si la ventana de registro está abierta, hacerle focus
            self.ventana_registrar_horario.focus_force()

    def abrir_consultar_estudiantes_curso(self):
        """Abre la ventana para consultar los estudiantes inscritos en un curso"""
        # Verificar si hay un curso seleccionado
        seleccion = self.frame_tabla_cursos.tabla_cursos.selection()
        if not seleccion:
            msg_no_hay_seleccion("curso", "consultar estudiantes")
            return
            
        # Obtener el ID y nombre del curso seleccionado
        valores = self.frame_tabla_cursos.tabla_cursos.item(seleccion[0])['values']
        curso_id = valores[0]
        nombre_curso = valores[1]
        
        # Debug: Imprimir información del curso seleccionado
        print(f"Curso seleccionado - ID: {curso_id}, Nombre: {nombre_curso}")
        
        # Crear y mostrar la ventana
        ventana = ctk.CTkToplevel(self)
        ventana.transient(self)
        ventana.grab_set()
        
        # Crear la vista
        vista = VistaConsultarEstudiantesCurso(
            root=ventana,
            db=self.db,
            curso_id=curso_id,
            nombre_curso=nombre_curso
        )
        
        # Configurar el tema
        ctk.set_appearance_mode(self.tema_actual)

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

### Funciones basadas en VentanaTablaResultados

    def obtener_datos_seleccion(self, seleccion):
        """
            Retorna:
            - valores: datos de la fila seleccionada en la tabla
            - curso_id: ID del curso
            - nombre_curso: Nombre del curso
        """
        # Función de apoyo para abrir_consultar_horarios2

        # Obtener el ID y nombre del curso seleccionado
        valores = self.frame_tabla_cursos.tabla_cursos.item(seleccion[0])['values']
        curso_id = valores[0]
        nombre_curso = valores[1]
        return valores, curso_id, nombre_curso
    
    def obtener_datos_de_los_horarios(self, curso_id):
        """
            Retorna lista de horarios para confirmar si el curso tiene horarios
            - horarios: es una lista, en donde cada elemento es un diccionario de la forma:
        """
        # Función de apoyo para abrir_consultar_horarios2
        # Obtener cursos del curso
        horarios = self.controlador_horario.obtener_horarios_por_curso(curso_id)
        # horarios es una lista, en donde cada elemento es una tupla de la forma:
            # [0]: horario ID
            # [1]: curso ID
            # [2]: día semana
            # [3]: hora inicio
            # [4]: hora fin
            # [5]: curso nombre
            # [6]: profesor ID
            # [7]: nombre profesor
            # [8]: descripción de curso
            # [9]: duración del curso
        return horarios
    
    def preparar_datos_para_mostrar_horarios(self, horarios):
        """
            Retorna, lista para ser impresa en la ventana de resultados
            - resultados: lista, en donde cada elemento es una lista con los datos a imprimir que son:
            - [0]: Horario ID
            - [1]: Nombre del profesor
            - [2]: Día del horario
            - [3]: Hora de inicio
            - [4]: Hora de fin
        """
        # Función de apoyo para abrir_consultar_cursos2
        # Se convierte cursos para que quede todo como en filas.
        resultados = []

        for c in horarios:
            fila = [c[0], c[7], c[2], c[3], c[4]]
            resultados.append(fila)  

        return resultados
            
    def abrir_consultar_horarios2(self):
        """Abre la ventana para consultar los horarios del curso seleccionado"""
        
        # Verificar si hay un curso seleccionado
        seleccion = self.frame_tabla_cursos.tabla_cursos.selection()
        if not seleccion:
            msg_no_hay_seleccion("curso", "consultar horarios")
            return
        
        # Obtener los datos de la selección
        valores, curso_id, nombre_curso = self.obtener_datos_seleccion(seleccion)

        # Confirmar si el curso tiene horarios
        horarios = self.obtener_datos_de_los_horarios(curso_id)

        if not horarios:
            msg_error_inesperado("Este curso no tienen ningun horario asociado")
            if hasattr(self, 'ventana_consultar_horarios_actual'):
                self.ventana_consultar_horarios_actual.destroy()
            return
        
        # Preparar los datos para su impresión en el TreeView
        resultados = self.preparar_datos_para_mostrar_horarios(horarios)
        
        # Verificar si la ventana anterior aún existe
        if hasattr(self, 'ventana_consultar_horarios_actual'):
            try:
                # Intentar hacer focus a la ventana existente e imprimir nuevos datos si un usuario diferente ha sido seleccionado
                self.ventana_consultar_horarios_actual.actualizar_titulos(nombre_curso)
                self.ventana_consultar_horarios_actual.frame_tabla_resultados.imprimir_informacion_en_tabla(resultados)
                self.ventana_consultar_horarios_actual.focus_force()
                return
            except:
                # Si falla, significa que la ventana ya no existe
                self.ventana_consultar_horarios_por_curso_esta_abierta = False
                if hasattr(self, 'ventana_consultar_horarios_actual'):
                    delattr(self, 'ventana_consultar_horarios_actual')
        
        # Si no hay ventana abierta o la anterior ya no existe, crear una nueva
        #if not self.ventana_consultar_horarios_actual:
        else:
        
            columnas = ("id", "profesor", "dia", "hora_inicio", "hora_fin")
            nombre_columnas = ("ID Horario", "Profesor", "Día", "Profesor","Hora de inicio","Hora de fin")
            ancho_columnas = (100, 200, 150, 150, 150)

            # Crear nueva ventana
            self.ventana_consultar_horarios_por_curso_esta_abierta = True

            self.ventana_consultar_horarios_actual = VentanaTablaResultados(
                self,
                "horario",
                "curso",
                nombre_curso,
                columnas,
                nombre_columnas,
                ancho_columnas,
                resultados,
                0.7,
                0.7
            )

    def obtener_datos_de_los_estudiantes(self, curso_id):
        """
            Retorna lista de estudiantes para confirmar si el curso tiene estudiantes
            - estudiantes: es una lista, en donde cada elemento es un diccionario de la forma:
        """
        # Función de apoyo para abrir_consultar_estudiantes_curso2
        # Obtener estudiantes del curso
        estudiantes = self.controlador_matricula.obtener_estudiantes_por_curso(curso_id)
        # horarios es una lista, en donde cada elemento es una tupla de la forma:
            # [0]: matrícula ID
            # [1]: estudiante ID
            # [2]: nombre de estudiante
            # [3]: fecha de matricula
        return estudiantes
    
    
    def abrir_consultar_estudiantes_curso2(self):
        """Abre la ventana para consultar los estudiantes del curso seleccionado"""
        
        # Verificar si hay un curso seleccionado
        seleccion = self.frame_tabla_cursos.tabla_cursos.selection()
        if not seleccion:
            msg_no_hay_seleccion("curso", "consultar estudiantes")
            return
        
        # Obtener los datos de la selección
        valores, curso_id, nombre_curso = self.obtener_datos_seleccion(seleccion)

        # Confirmar si el curso tiene estudiantes, estos datos ya vienen con el formato para la tabla
        estudiantes = self.obtener_datos_de_los_estudiantes(curso_id)

        if not estudiantes:
            msg_error_inesperado("Este curso no tienen ningun estudiante asociado")
            if hasattr(self, 'ventana_consultar_estudiantes_por_curso'):
                self.ventana_consultar_estudiantes_por_curso.destroy()
            return
        
        # Verificar si la ventana anterior aún existe
        if hasattr(self, 'ventana_consultar_estudiantes_por_curso'):
            try:
                # Intentar hacer focus a la ventana existente e imprimir nuevos datos si un usuario diferente ha sido seleccionado
                self.ventana_consultar_estudiantes_por_curso.actualizar_titulos(nombre_curso)
                self.ventana_consultar_estudiantes_por_curso.frame_tabla_resultados.imprimir_informacion_en_tabla(estudiantes)
                self.ventana_consultar_estudiantes_por_curso.focus_force()
                return
            except:
                # Si falla, significa que la ventana ya no existe
                self.ventana_consultar_estudiantes_por_curso_esta_abierta = False
                if hasattr(self, 'ventana_consultar_estudiantes_por_curso'):
                    delattr(self, 'ventana_consultar_estudiantes_por_curso')
        
        # Si no hay ventana abierta o la anterior ya no existe, crear una nueva
        #if not self.ventana_consultar_horarios_actual:
        else:
        
            columnas = ("id_matricula","id_estudiante", "nombre", "fecha_matricula")
            nombre_columnas = ("ID Matrícula","ID Estudiante", "Nombre", "Fecha de Matrícula")
            ancho_columnas = (200, 200, 200, 200)

            # Crear nueva ventana
            self.ventana_consultar_estudiantes_por_curso_esta_abierta = True

            self.ventana_consultar_estudiantes_por_curso = VentanaTablaResultados(
                self,
                "estudiante",
                "curso",
                nombre_curso,
                columnas,
                nombre_columnas,
                ancho_columnas,
                estudiantes,
                0.7,
                0.7
            )

    def cerrar_resultados(self):
        """Cierra la ventana de consultar horarios y estudiantes y actualiza el estado"""
        try:
            self.ventana_consultar_horarios_por_curso_esta_abierta = False
            self.ventana_consultar_horarios_actual.destroy()
        except:
            pass

        try:
            self.ventana_consultar_estudiantes_por_curso_esta_abierta = False
            self.ventana_consultar_estudiantes_por_curso.destroy()
        except:
            pass


if __name__ == "__main__":
    db = Database()
    app = VentanaMenuCurso(db)
    app.iniciar_ventana()
