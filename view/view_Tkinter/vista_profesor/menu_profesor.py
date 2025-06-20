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
from view.view_Tkinter.vista_msgbox.msgbox_library import msg_no_hay_seleccion, msg_hay_otra_ventana_abierta, msg_error_inesperado

from view.view_Tkinter.vista_tablas_resultados.ventana_tabla_resultados import VentanaTablaResultados

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
        self.resizable(True, True)

        # Crear el frame Header - Contiene título y botones de cambiar tema y regresar a la ventana principal
        self.frame_header = FrameHeader(self)
        self.frame_header.pack(fill="x", padx=20, pady=10)

        # Crear el frame de tabla profesores - Contiene la tabla y el scroller vertical
        self.frame_tabla_profesores = FrameTablaProfesores(self)
        self.frame_tabla_profesores.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear el frame para el Footer - Contiene los botones de acción
        self.frame_footer = FrameFooter(self)
        self.frame_footer.pack(fill='x', padx=20, pady=10)
        
        # Ejecuta la función "regresar_menu_principal", para poder regresar en caso de que se cierre la ventana con el botón cerrar
        self.protocol("WM_DELETE_WINDOW",self.regresar_menu_principal)

        # Trackear estado (abiertas o cerradas) de ventanas de operaciones
        # Al inicial menú de profesor, todas las ventanas están cerradas
        # Estas se usan para evitar abrir más de una ventana para cada operación
        self.ventana_registro_esta_abierta = False
        self.ventana_actualizacion_esta_abierta = False
        self.ventana_borrar_esta_abierta = False
        self.ventana_buscar_esta_abierta = False
        self.ventana_cursos_esta_abierta = False #v1
        self.ventana_consultar_cursos_esta_abierta = False
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
            # Cerrar la que ya está abierta, y volverla a abrir con los nuevos datos
            self.ventana_borrar.destroy()
            self.ventana_borrar = VentanaBorrarProfesor(parent=self)
            self.ventana_borrar.mainloop()

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

    def obtener_datos_seleccion(self, seleccion):
        """
            Retorna:
            - valores: datos de la fila seleccionada en la tabla
            - profesor_id: ID del profesor
            - nombre_profesor: Nombre del profesor
        """
        # Función de apoyo para abrir_consultar_cursos2

        # Obtener el ID y nombre del profesor seleccionado
        valores = self.frame_tabla_profesores.tabla_profesores.item(seleccion[0])['values']
        profesor_id = valores[0]
        nombre_profesor = f"{valores[1]} {valores[2]}"
        return valores, profesor_id, nombre_profesor
    
    def obtener_datos_de_los_cursos(self, profesor_id):
        """
            Retorna lista de cursos para confirmar si el profesor tiene cursos
            - cursos: es una lista, en donde cada elemento es un objeto de la clase Curso
        """
        # Función de apoyo para abrir_consultar_cursos2

        # Obtener cursos del profesor
        cursos = self.controlador_profesor.obtener_cursos_profesor(profesor_id)
        # - cursos: es una lista, en donde cada elemento es un objeto de la clase Curso
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
            fila = [c.id_curso,
                    c.nombre,
                    c.descripcion,
                    c.duracion_horas,
                    c.horarios
                    ]

            resultados.append(fila)  
        return resultados
            
    def abrir_ventana_cursos_profesor2(self):
        """Abre la ventana para consultar los cursos del profesor seleccionado"""
        
        # Verificar si hay un profesor seleccionado
        seleccion = self.frame_tabla_profesores.tabla_profesores.selection()
        if not seleccion:
            msg_no_hay_seleccion("profesor", "consultar cursos")
            return
        
        # Obtener los datos de la selección
        valores, profesor_id, nombre_profesor = self.obtener_datos_seleccion(seleccion)

        # Confirmar si el profesor tiene cursos
        cursos = self.obtener_datos_de_los_cursos(profesor_id)

        if not cursos:
            msg_error_inesperado("Este profesor no tiene ningún curso asociado")
            if hasattr(self, 'ventana_consultar_cursos_actual'):
                self.ventana_consultar_cursos_actual.destroy()
            return
        
        # Preparar los datos para su impresión en el TreeView
        resultados = self.preparar_datos_para_mostrar_cursos(cursos)
        
        # Verificar si la ventana anterior aún existe
        if hasattr(self, 'ventana_consultar_cursos_actual'):
            try:
                # Intentar hacer focus a la ventana existente e imprimir nuevos datos si un usuario diferente ha sido seleccionado
                self.ventana_consultar_cursos_actual.actualizar_titulos(nombre_profesor)
                self.ventana_consultar_cursos_actual.frame_tabla_resultados.imprimir_informacion_en_tabla(resultados)
                self.ventana_consultar_cursos_actual.focus_force()
                return
            except:
                # Si falla, significa que la ventana ya no existe
                self.ventana_consultar_cursos_esta_abierta = False
                if hasattr(self, 'ventana_consultar_cursos_actual'):
                    delattr(self, 'ventana_consultar_cursos_actual')
        
        # Si no hay ventana abierta o la anterior ya no existe, crear una nueva
        if not self.ventana_consultar_cursos_esta_abierta:
        
            columnas = ("id", "nombre", "descripcion", "duracion", "horarios")
            nombre_columnas = ("ID", "Nombre del Curso", "Descripción","Duración (hrs)","Horarios")
            ancho_columnas = (100, 200, 250, 100, 200)
            # Crear nueva ventana
            self.ventana_consultar_cursos_esta_abierta = True

            self.ventana_consultar_cursos_actual = VentanaTablaResultados(
                self,
                "curso",
                "profesor",
                nombre_profesor,
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
        