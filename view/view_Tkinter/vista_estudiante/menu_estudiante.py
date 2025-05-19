import customtkinter as ctk

# from tkinter import ttk

from config.database import Database
from config.appearance import centrar_ventana

from controllers.estudiante_controller import EstudianteController

from mysql.connector import IntegrityError

from .frame_header import FrameHeader
from .frame_tabla_estudiantes import FrameTablaEstudiantes
from .frame_footer import FrameFooter
from .ventana_registrar_estudiante import VentanaRegistrarEstudiante
from .ventana_actualizar_estudiante import VentanaActualizarEstudiante
from .ventana_borrar_estudiante import VentanaBorrarEstudiante

class VentanaMenuEstudiante(ctk.CTk):

    def __init__(self, db: Database = None):
        super().__init__()
        # El método constructor asegura que el atributo "db" sea de tipo "Database""
        self.db = db
        self.controlador_estudiante = EstudianteController(self.db)

    def iniciar_ventana(self, tema_actual):    
        
        self.title("Gestión de estudiantes")
        
        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)
        self.tema_actual = tema_actual
        centrar_ventana(self, proporcion=0.7)
        
        # Configuración de restricciones de la ventana
        self.resizable(True, True)

        # Crear el frame Header - Contiene título y botones de cambiar tema y regresar
        self.frame_principal = FrameHeader(self)
        self.frame_principal.pack(fill="x", padx=20, pady=10)

        # Crear el frame de tabla estudiantes
        self.frame_tabla_estudiantes = FrameTablaEstudiantes(self)
        self.frame_tabla_estudiantes.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear el frame para el Footer
        self.frame_footer = FrameFooter(self)
        self.frame_footer.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Ejecuta la función "regresar_menu_principal", para poder regresar en caso de que se cierre la ventana con el botón cerrar
        self.protocol("WM_DELETE_WINDOW",self.regresar_menu_principal)

        # Trackear estado de ventanas abiertas
        self.ventana_registro_esta_abierta = False
        self.ventana_actualizacion_esta_abierta = False
        self.ventana_borrar_esta_abierta = False
        self.mainloop()


    def obtener_lista_estudiantes(self):
        
        # estudiantes: es una lista de objetos tipo "Estudiante" con atributos:
        try: 
            estudiantes = self.controlador_estudiante.listar_estudiantes()
            if estudiantes:
                pass
            else:
                raise ValueError
        except ValueError as e:
            print("Valores inválidos")
        except Exception as e:
            print(f"Error al listar los estudiantes: {str(e)}")
        
        return estudiantes
        # estudiantes: es una lista de objetos tipo "Estudiante", atributos:
        # id_estudiante
        # nombre
        # apellido
        # correo
        # telefono
    
    def abrir_ventana_registro(self):
        if self.ventana_registro_esta_abierta == False:
            self.ventana_registro_esta_abierta = True
            # Abrir la ventana
            self.ventana_registro = VentanaRegistrarEstudiante(parent=self)
            self.ventana_registro.mainloop()
        else:
            # No hacer nada
            self.ventana_registro.focus_force()
    
    def abrir_ventana_actualizacion(self):
        #print(self.frame_tabla_estudiantes.tabla_estudiantes.selection()[0])
        if self.ventana_actualizacion_esta_abierta == False:
            self.ventana_actualizacion_esta_abierta = True
            # Abrir la ventana
            self.ventana_actualizacion = VentanaActualizarEstudiante(parent=self)
            self.ventana_actualizacion.mainloop()
        else:
            # No hacer nada
            self.ventana_actualizacion.focus_force()   
    
    def abrir_ventana_borrar(self):
        #print(self.frame_tabla_estudiantes.tabla_estudiantes.selection()[0])
        if self.ventana_borrar_esta_abierta == False:
            self.ventana_borrar_esta_abierta = True
            # Abrir la ventana
            self.ventana_borrar = VentanaBorrarEstudiante(parent=self)
            self.ventana_borrar.mainloop()
        else:
            # No hacer nada
            self.ventana_borrar.focus_force()  


    def cambiar_tema(self):
        """
        Método para cambiar el estilo de la ventana
        """
        if self.tema_actual == "Light":
            ctk.set_appearance_mode("Dark")
            self.tema_actual = "Dark"
            #self.btn_cambiar_tema.configure(text="☀️ Cambiar Tema")
        else:
            ctk.set_appearance_mode("Light")
            self.tema_actual = "Light"
            #self.btn_cambiar_tema.configure(text="🌓 Cambiar Tema")

    def regresar_menu_principal(self):
        '''Método para cerrar el programa de manera segura'''
        self.destroy()

        # Abrir de nuevo el menú principal
        from view.view_Tkinter.vista_principal.menu_principal import VentanaMenuPrincipal
        app = VentanaMenuPrincipal(db=self.db)
        # Iniciar el bucle principal de la aplicación
        app.iniciar_ventana()