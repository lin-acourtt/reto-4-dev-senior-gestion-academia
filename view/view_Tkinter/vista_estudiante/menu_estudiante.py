import customtkinter as ctk

# from tkinter import ttk

from config.database import Database
from config.appearance import centrar_ventana

from controllers.estudiante_controller import EstudianteController
from controllers.matricula_controller import MatriculaController

from mysql.connector import IntegrityError

from .frame_header import FrameHeader
from .frame_tabla_estudiantes import FrameTablaEstudiantes
from .frame_footer import FrameFooter
from .ventana_registrar_estudiante import VentanaRegistrarEstudiante
from .ventana_actualizar_estudiante import VentanaActualizarEstudiante
from .ventana_borrar_estudiante import VentanaBorrarEstudiante
from .ventana_buscar_estudiante import VentanaBuscarEstudiante
from view.view_Tkinter.vista_msgbox.msgbox_library import msg_no_hay_seleccion, msg_hay_otra_ventana_abierta, msg_error_inesperado
from .ventana_consultar_cursos_estudiante import VistaConsultarCursosEstudiante
from view.view_Tkinter.vista_tablas_resultados.ventana_tabla_resultados import VentanaTablaResultados

class VentanaMenuEstudiante(ctk.CTkToplevel):

    def __init__(self, db: Database = None):
        """
            Constructor, requiere de:
            - db: Base de datos, objeto tipo Database
        """
        super().__init__()
        # El método constructor asegura que el atributo "db" sea de tipo "Database""
        self.db = db
        self.controlador_estudiante = EstudianteController(self.db)

    def iniciar_ventana(self, tema_actual):    
        """
            Inicia la ventana menú estudiante, requiere de:
            - tema_actual: tema con el que se abrirá la ventana
        """
        self.title("Gestión de estudiantes")
        
        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)
        self.tema_actual = tema_actual
        centrar_ventana(self, proporcion=0.7)
        
        # Configuración de restricciones de la ventana
        self.resizable(False, False)

        # Crear el frame Header - Contiene título y botones de cambiar tema y regresar a la ventana principal
        self.frame_header = FrameHeader(self)
        self.frame_header.pack(fill="x", padx=20, pady=10)

        # Crear el frame de tabla estudiantes - Contiene la tabla y el scroller vertical
        self.frame_tabla_estudiantes = FrameTablaEstudiantes(self)
        self.frame_tabla_estudiantes.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear el frame para el Footer - Contiene los botones de acción
        self.frame_footer = FrameFooter(self)
        self.frame_footer.pack(padx=20, pady=10)
        #self.frame_footer.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Ejecuta la función "regresar_menu_principal", para poder regresar en caso de que se cierre la ventana con el botón cerrar
        self.protocol("WM_DELETE_WINDOW",self.regresar_menu_principal)

        # Trackear estado (abiertas o cerradas) de ventanas de operaciones
        # Al inicial menú de estudiante, todas las ventanas están cerradas
        # Estas se usan para evitar abrir más de una ventana para cada operación
        self.ventana_registro_esta_abierta = False
        self.ventana_actualizacion_esta_abierta = False
        self.ventana_borrar_esta_abierta = False
        self.ventana_buscar_esta_abierta = False
        self.ventana_consultar_cursos_esta_abierta = False
        self.mainloop()


    def obtener_lista_estudiantes(self):
        """
            Obtiene lista de estudiantes. "estudiantes" es una lista de objetos tipo "Estudiante", atributos:
            - id_estudiante
            - nombre
            - apellido
            - correo
            - telefono
        """
        try: 
            estudiantes = self.controlador_estudiante.listar_estudiantes()
            if estudiantes:
                return estudiantes
            else:
                raise ValueError
        except ValueError as e:
            print("Valores inválidos")
        except Exception as e:
            print(f"Error al listar los estudiantes: {str(e)}")
        
        
        # estudiantes: es una lista de objetos tipo "Estudiante", atributos:
        # id_estudiante
        # nombre
        # apellido
        # correo
        # telefono
    
    def abrir_ventana_registro(self):
        """
            Abrir la ventana para el registro de estudiantes
        """
        if self.ventana_registro_esta_abierta == False:
            # Si la ventana de registro está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_registro_esta_abierta = True
            # Abrir la ventana
            self.ventana_registro = VentanaRegistrarEstudiante(parent=self)
            self.ventana_registro.mainloop()
        else:
            # Si la ventana de registro está abierta, hacerle focus
            self.ventana_registro.focus_force()
    
    def abrir_ventana_actualizacion(self):
        """
            Abrir la ventana para la actualización de datos de estudiantes
        """
        # Si no hay nada seleccionado, se indica que se debe seleccionar un item primero
        seleccion = self.frame_tabla_estudiantes.tabla_estudiantes.selection()
        if not seleccion:
            msg_no_hay_seleccion("estudiante","actualizar")
            #messagebox.showwarning("Advertencia", "Por favor, seleccione un profesor para actualizar")
            return
        
        if self.ventana_actualizacion_esta_abierta == False:
            # Si la ventana de actualización está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_actualizacion_esta_abierta = True
            # Abrir la ventana
            self.ventana_actualizacion = VentanaActualizarEstudiante(parent=self)
            self.ventana_actualizacion.mainloop()
        else:
            # Si la ventana de actualización está abierta, hacerle focus y actualizar los campos si se cambió la selección
            self.ventana_actualizacion.actualizar_informacion_campos()
            self.ventana_actualizacion.focus_force()   
    
    def abrir_ventana_borrar(self):
        """
            Abrir la ventana para la eliminación de estudiantes
        """
        
        # Si no hay nada seleccionado, se indica que se debe seleccionar un item primero
        seleccion = self.frame_tabla_estudiantes.tabla_estudiantes.selection()
        if not seleccion:
            msg_no_hay_seleccion("estudiante","borrar")
            #messagebox.showwarning("Advertencia", "Por favor, seleccione un profesor para actualizar")
            return
        
        if self.ventana_borrar_esta_abierta == False:
            # Si la ventana de borrar está cerrada, cambiar su atributo a "True" y abrir la ventana
            self.ventana_borrar_esta_abierta = True
            # Abrir la ventana
            self.ventana_borrar = VentanaBorrarEstudiante(parent=self)
            self.ventana_borrar.mainloop()
        else:
            # Si la ventana de borrar está abierta, hacerle focus
            self.ventana_borrar.focus_force()  

    def abrir_ventana_buscar(self):
        """
            Abrir la ventana para buscar estudiante por iD
        """

        if self.ventana_buscar_esta_abierta == False:
            # Abrir la ventana
            self.ventana_buscar = VentanaBuscarEstudiante(parent=self)
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

    def abrir_consultar_cursos(self):
        """Abre la ventana para consultar los cursos del estudiante seleccionado"""
        # Verificar si hay un estudiante seleccionado
        seleccion = self.frame_tabla_estudiantes.tabla_estudiantes.selection()
        if not seleccion:
            msg_no_hay_seleccion("estudiante", "consultar cursos")
            return
            
        # Obtener el ID y nombre del estudiante seleccionado
        valores = self.frame_tabla_estudiantes.tabla_estudiantes.item(seleccion[0])['values']
        estudiante_id = valores[0]
        nombre_estudiante = f"{valores[1]} {valores[2]}"
        
        # Verificar si la ventana anterior aún existe
        if hasattr(self, 'ventana_consultar_cursos_actual'):
            try:
                # Intentar hacer focus a la ventana existente
                self.ventana_consultar_cursos_actual.focus_force()
                return
            except:
                # Si falla, significa que la ventana ya no existe
                self.ventana_consultar_cursos_esta_abierta = False
                if hasattr(self, 'ventana_consultar_cursos_actual'):
                    delattr(self, 'ventana_consultar_cursos_actual')
        
        # Si no hay ventana abierta o la anterior ya no existe, crear una nueva
        if not self.ventana_consultar_cursos_esta_abierta:
            # Crear nueva ventana
            self.ventana_consultar_cursos_esta_abierta = True
            ventana = ctk.CTkToplevel(self)
            ventana.title("Consultar Cursos del Estudiante")
            ventana.geometry("1000x600")
            ventana.transient(self)
            ventana.grab_set()
            centrar_ventana(ventana)
            
            # Crear la vista
            vista = VistaConsultarCursosEstudiante(
                root=ventana,
                db=self.db,
                estudiante_id=estudiante_id,
                nombre_estudiante=nombre_estudiante
            )
            
            # Configurar el tema
            ctk.set_appearance_mode(self.tema_actual)
            
            # Configurar el protocolo de cierre
            ventana.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_ventana_consultar_cursos(ventana))
            
            # Mantener referencia a la ventana actual
            self.ventana_consultar_cursos_actual = ventana
            
    def cerrar_ventana_consultar_cursos(self, ventana):
        """Cierra la ventana de consultar cursos y actualiza el estado"""
        try:
            ventana.destroy()
        except:
            pass
        finally:
            self.ventana_consultar_cursos_esta_abierta = False
            if hasattr(self, 'ventana_consultar_cursos_actual'):
                delattr(self, 'ventana_consultar_cursos_actual')

    def obtener_datos_seleccion(self, seleccion):
        """
            Retorna:
            - valores: datos de la fila seleccionada en la tabla
            - estudiante_id: ID del estudiante
            - nombre_estudiante: Nombre del estudiante
        """
        # Función de apoyo para abrir_consultar_cursos2

        # Obtener el ID y nombre del estudiante seleccionado
        valores = self.frame_tabla_estudiantes.tabla_estudiantes.item(seleccion[0])['values']
        estudiante_id = valores[0]
        nombre_estudiante = f"{valores[1]} {valores[2]}"
        return valores, estudiante_id, nombre_estudiante
    
    def obtener_datos_de_los_cursos(self, estudiante_id):
        """
            Retorna lista de cursos para confirmar si el estudiante tiene cursos
            - cursos: es una lista, en donde cada elemento es un diccionario de la forma:
        """
        # Función de apoyo para abrir_consultar_cursos2

        # Obtener cursos del estudiante
        controlador_matricula = MatriculaController(self.db)
        cursos = controlador_matricula.obtener_cursos_por_estudiante(estudiante_id)
        # Cursos es una lista, en donde cada elemento es un diccionario de la forma:
            # {'id_curso': ID, 
            #   'nombre': 'Nombre', 
            #   'profesor': 'Nombre', 
            #   'descripcion': 'Descripción', 
            #   'duracion_horas': Horas, 
            #   'horarios': 'Horarios'} 
        return cursos
    
    def preparar_datos_para_mostrar_cursos(self, cursos):
        """
            Retorna, lista para ser impresa en la ventana de resultados
            - resultados: lista, en donde cada elemento es una lista con los datos a imprimir 
        """
        # Función de apoyo para abrir_consultar_cursos2
        # Se convierte cursos para que quede todo como en filas.
        resultados = []

        for c in cursos:
            fila = []
            elementos = c.values()
            for e in elementos:
                fila.append(e)

            resultados.append(fila)  
        return resultados
            
    def abrir_consultar_cursos2(self):
        """Abre la ventana para consultar los cursos del estudiante seleccionado"""
        
        # Verificar si hay un estudiante seleccionado
        seleccion = self.frame_tabla_estudiantes.tabla_estudiantes.selection()
        if not seleccion:
            msg_no_hay_seleccion("estudiante", "consultar cursos")
            return
        
        # Obtener los datos de la selección
        valores, estudiante_id, nombre_estudiante = self.obtener_datos_seleccion(seleccion)

        # Confirmar si el estudiante tiene cursos
        cursos = self.obtener_datos_de_los_cursos(estudiante_id)

        if not cursos:
            msg_error_inesperado("Este estudiante no está inscrito en ningún curso")
            if hasattr(self, 'ventana_consultar_cursos_actual'):
                self.ventana_consultar_cursos_actual.destroy()
            return
        
        # Preparar los datos para su impresión en el TreeView
        resultados = self.preparar_datos_para_mostrar_cursos(cursos)
        
        # Verificar si la ventana anterior aún existe
        if hasattr(self, 'ventana_consultar_cursos_actual'):
            try:
                # Intentar hacer focus a la ventana existente e imprimir nuevos datos si un usuario diferente ha sido seleccionado
                self.ventana_consultar_cursos_actual.actualizar_titulos(nombre_estudiante)
                self.ventana_consultar_cursos_actual.frame_tabla_resultados.imprimir_informacion_en_tabla(resultados)
                self.ventana_consultar_cursos_actual.focus_force()
                return
            except:
                # Si falla, significa que la ventana ya no existe
                self.ventana_consultar_cursos_esta_abierta = False
                if hasattr(self, 'ventana_consultar_cursos_actual'):
                    delattr(self, 'ventana_consultar_cursos_actual')
        
        # Si no hay ventana abierta o la anterior ya no existe, crear una nueva
        if not self.ventana_consultar_cursos_actual:
        
            columnas = ("id", "curso", "profesor", "descripcion", "duracion", "horarios")
            nombre_columnas = ("ID", "Curso", "Profesor", "Descripción","Duración (hrs)","Horarios")
            ancho_columnas = (50, 200, 200, 200, 100, 200)
            # Crear nueva ventana
            self.ventana_consultar_cursos_esta_abierta = True

            self.ventana_consultar_cursos_actual = VentanaTablaResultados(
                self,
                "curso",
                "estudiante",
                nombre_estudiante,
                columnas,
                nombre_columnas,
                ancho_columnas,
                resultados,
                0.7,
                0.7
            )
    def cerrar_resultados(self):
        """Cierra la ventana de consultar cursos y actualiza el estado"""
        self.ventana_consultar_cursos_esta_abierta = False
        self.ventana_consultar_cursos_actual.destroy()
        