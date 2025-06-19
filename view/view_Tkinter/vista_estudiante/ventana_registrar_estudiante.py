import customtkinter as ctk
from view.view_Tkinter.vista_msgbox.msgbox_library import msg_sin_cambios, msg_registro_exitoso, msg_error_campos_vacios, msg_entrada_duplicada, msg_error_integrity, msg_error_inesperado
from mysql.connector import IntegrityError
from config.appearance import centrar_ventana

class VentanaRegistrarEstudiante(ctk.CTk):
    """
        Inicializa la ventana para registrar estudiantes.
    """
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        
        centrar_ventana(self,0.35,0.3)
        self.resizable(False, False)
        self.title("Registro de estudiantes")

        self.columnconfigure(0,weight=2)
        self.columnconfigure(1,weight=1)

        for i in range(4):
            self.rowconfigure(i,weight=1)

        self.label_titulo = ctk.CTkLabel(self, text="Registro de estudiantes",font=("Helvetica", 14, "bold"))
        self.label_titulo.grid(row = 0, column = 0, columnspan=2,pady=(10,10))

        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre")
        self.entry_nombre.grid(row = 1, column = 0, padx=(30,10), pady=5, sticky='ew')

        self.entry_apellido = ctk.CTkEntry(self, placeholder_text="Apellido")
        self.entry_apellido.grid(row = 2, column = 0, padx=(30,10), pady=5, sticky='ew')

        self.entry_correo = ctk.CTkEntry(self, placeholder_text="Correo")
        self.entry_correo.grid(row = 3, column = 0, padx=(30,10), pady=5, sticky='ew')

        self.entry_telefono = ctk.CTkEntry(self, placeholder_text="Teléfono")
        self.entry_telefono.grid(row = 4, column = 0, padx=(30,10), pady=(5,30), sticky='ew')

        self.btn_guardar = ctk.CTkButton(self, text="Guardar", command=self.guardar_registro)
        self.btn_guardar.grid(row = 2, column = 1, padx=(0,20))
        
        self.btn_cancelar = ctk.CTkButton(self, text="Cancelar", command=self.cancelar_registro)
        self.btn_cancelar.grid(row = 3, column = 1, padx=(0,20))

        self.protocol("WM_DELETE_WINDOW", self.cancelar_registro)

    def guardar_registro(self):
        """
            Actualiza la base de datos (tabla estudiantes), con la información del estudiante que se escribió en el formulario.
        """
        try: 
            # Obtener los datos en los elementos de "Entry"
            nombre = self.entry_nombre.get().strip()
            apellido = self.entry_apellido.get().strip()
            correo = self.entry_correo.get().strip()
            telefono = self.entry_telefono.get().strip()

            # Validar campos
            if not all([nombre, apellido, correo, telefono]):
                msg_error_campos_vacios()
                return
            
            # Utilizar el controlador de estudiante para registrar un nuevo estudiante
            self.parent.controlador_estudiante.registrar_estudiante(nombre, apellido, correo, telefono)
            
            # Inserta el nuevo estudiante en la lista de estudiantes
            # (Se re-imprime toda la lista)
            estudiantes = self.parent.obtener_lista_estudiantes()
            self.parent.frame_tabla_estudiantes.imprimir_informacion_en_tabla(estudiantes)
            
            # Mostrar un mensaje de registro exitoso
            msg_registro_exitoso("Estudiante")

            # Cierra la ventana y cambia el estado de esta ventana a cerrado
            self.actualizar_estado_ventana_al_cerrar()
        
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                msg_entrada_duplicada("estudiante")
            else:
                msg_error_integrity("estudiante",str(e))
        except Exception as e:
            msg_error_inesperado(str(e))

    def cancelar_registro(self):
        """
            Muestra un mensaje de alerta, y se cierra la ventana
        """
        msg_sin_cambios()
        self.actualizar_estado_ventana_al_cerrar()

    def actualizar_estado_ventana_al_cerrar(self):
        self.parent.ventana_registro_esta_abierta = False
        self.destroy()
