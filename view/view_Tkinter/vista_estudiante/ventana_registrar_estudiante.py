import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from mysql.connector import IntegrityError
from config.appearance import centrar_ventana

class VentanaRegistrarEstudiante(ctk.CTk):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        
        centrar_ventana(self,proporcion=0.25)
        self.title("Registro de estudiantes")
        self.label_titulo = ctk.CTkLabel(self, text="Registro de estudiantes")
        self.label_titulo.grid(row = 0, column = 0, columnspan=2)

        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre")
        self.entry_nombre.grid(row = 1, column = 0, padx=20, pady=5)

        self.entry_apellido = ctk.CTkEntry(self, placeholder_text="Apellido")
        self.entry_apellido.grid(row = 2, column = 0, padx=20, pady=5)

        self.entry_correo = ctk.CTkEntry(self, placeholder_text="Correo")
        self.entry_correo.grid(row = 3, column = 0, padx=20, pady=5)

        self.entry_telefono = ctk.CTkEntry(self, placeholder_text="Teléfono")
        self.entry_telefono.grid(row = 4, column = 0, padx=20, pady=5)

        self.btn_guardar = ctk.CTkButton(self, text="Guardar", command=self.guardar_registro)
        self.btn_guardar.grid(row = 2, column = 1)
        
        self.btn_cancelar = ctk.CTkButton(self, text="Cancelar", command=self.cancelar_registro)
        self.btn_cancelar.grid(row = 3, column = 1)

        self.protocol("WM_DELETE_WINDOW", self.actualizar_estado_ventana_al_cerrar)

    def guardar_registro(self):
        # Obtener los datos en los elementos de "Entry"
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        correo = self.entry_correo.get()
        telefono = self.entry_telefono.get()

        try:
            # Utilizar el controlador de estudiante para registrar un nuevo estudiante
            self.parent.controlador_estudiante.registrar_estudiante(nombre, apellido, correo, telefono)
            
            # Obtener la nueva lista de estudiantes
            estudiantes = self.parent.obtener_lista_estudiantes()
            self.parent.frame_tabla_estudiantes.imprimir_informacion_en_tabla(estudiantes)
            
            # Mostrar un mensaje de registro exitoso
            CTkMessagebox(
                title= "Guardado",
                message= "Estudiante registrado con éxito",
                icon= "check",
                option_1="OK"
            )
            self.actualizar_estado_ventana_al_cerrar()
        except IntegrityError as e:
            print(f"Error de integridad: {e.msg}")
        except Exception as e: 
            print(f"Error al registrar el estudiante: {str(e)}")


    def cancelar_registro(self):
        CTkMessagebox(
            title= "Sin cambios",
            message= "No se guardarán cambios",
            icon= "warning",
            option_1="OK"
        )
        self.actualizar_estado_ventana_al_cerrar()

    def actualizar_estado_ventana_al_cerrar(self):
        self.parent.ventana_registro_esta_abierta = False
        self.destroy()
