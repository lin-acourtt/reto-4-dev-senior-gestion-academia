import customtkinter as ctk
from view.view_Tkinter.vista_msgbox.msgbox_library import msg_sin_cambios, msg_registro_exitoso, msg_error_campos_vacios, msg_entrada_duplicada, msg_error_integrity, msg_error_inesperado
from mysql.connector import IntegrityError
from config.appearance import centrar_ventana

class VentanaRegistrarProfesor(ctk.CTk):
    """
        Inicializa la ventana para registrar profesores.
    """
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        
        centrar_ventana(self,0.35,0.4)
        self.resizable(False, False)
        #self.resizable(False, False)
        self.title("Registro de profesores")
        self.label_titulo = ctk.CTkLabel(self, text="Registro de profesores",font=("Helvetica", 14, "bold"))
        #self.label_titulo.pack()
        self.label_titulo.grid(row = 0, column = 0, columnspan=2, padx=(5,5), pady=(10,10))

        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        # Nombre
        self.label_nombre = ctk.CTkLabel(self, text="Nombre:")
        #self.label_nombre.pack()
        self.label_nombre.grid(row = 1, column= 0, padx=(10,10), pady=(5,5))
        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre")
        #self.entry_nombre.pack()
        self.entry_nombre.grid(row = 1, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        
        # Apellido
        self.label_apellido = ctk.CTkLabel(self, text="Apellido:")
        #self.entry_nombre.pack()
        self.label_apellido.grid(row = 2, column= 0, padx=(10,10), pady=(5,5))
        self.entry_apellido = ctk.CTkEntry(self, placeholder_text="Apellido")
        #self.entry_apellido.pack()
        self.entry_apellido.grid(row = 2, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        
        # Correo
        self.label_correo = ctk.CTkLabel(self, text="Correo:")
        #self.label_correo.pack()
        self.label_correo.grid(row = 3, column= 0, padx=(10,10), pady=(5,5))
        self.entry_correo = ctk.CTkEntry(self, placeholder_text="Correo")
        #self.entry_correo.pack()
        self.entry_correo.grid(row = 3, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        
        # Teléfono
        self.label_telefono = ctk.CTkLabel(self, text="Teléfono:")
        #self.label_telefono.pack()
        self.label_telefono.grid(row = 4, column= 0, padx=(10,10), pady=(5,5))
        self.entry_telefono = ctk.CTkEntry(self, placeholder_text="Teléfono")
        #self.entry_telefono.pack()
        self.entry_telefono.grid(row = 4, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        
        # Especialidad
        self.label_especialidad = ctk.CTkLabel(self, text="Especialidad:")
        #self.label_especialidad.pack()
        self.label_especialidad.grid(row = 5, column= 0, padx=(10,10), pady=(5,5))
        self.entry_especialidad = ctk.CTkEntry(self, placeholder_text="Especialidad")
        #self.entry_especialidad.pack()
        self.entry_especialidad.grid(row = 5, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        
        # Botones
        self.btn_guardar = ctk.CTkButton(
            self,
            text="Guardar",
            command=self.guardar_registro,
            width=200
        )
        #self.btn_guardar.pack()
        self.btn_guardar.grid(row = 6, column = 0, padx=(30,30), pady=(15,15))
        #self.btn_guardar.pack(side="left", padx=10, expand=True)
        
        self.btn_cancelar = ctk.CTkButton(
            self,
            text="Cancelar",
            command=self.cancelar_registro,
            width=200,
            fg_color="gray",
            hover_color="darkgray"
        )
        #self.btn_guardar.pack()
        self.btn_cancelar.grid(row = 6, column = 1, padx=(30,30), pady=(15,15)) 
        #self.btn_cancelar.pack(side="right", padx=10, expand=True)

        self.protocol("WM_DELETE_WINDOW", self.cancelar_registro)

    def guardar_registro(self):
        """
            Actualiza la base de datos (tabla profesores), con la información del profesor que se escribió en el formulario.
        """
        try: 
            # Obtener los datos en los elementos de "Entry"
            nombre = self.entry_nombre.get().strip()
            apellido = self.entry_apellido.get().strip()
            correo = self.entry_correo.get().strip()
            telefono = self.entry_telefono.get().strip()
            especialidad = self.entry_especialidad.get().strip()

            # Validar campos
            if not all([nombre, apellido, correo, telefono, especialidad]):
                msg_error_campos_vacios()
                return
            
            # Utilizar el controlador de profesor para registrar un nuevo profesor
            self.parent.controlador_profesor.registrar_profesor(nombre, apellido, correo, telefono, especialidad)
            
            # Inserta el nuevo profesor en la lista de profesores
            # (Se re-imprime toda la lista)
            profesores = self.parent.obtener_lista_profesores()
            self.parent.frame_tabla_profesores.imprimir_informacion_en_tabla(profesores)
            
            # Mostrar un mensaje de registro exitoso
            msg_registro_exitoso("Profesor")

            # Cierra la ventana y cambia el estado de esta ventana a cerrado
            self.actualizar_estado_ventana_al_cerrar()
        
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                msg_entrada_duplicada("profesor")
            else:
                msg_error_integrity("profesor",str(e))
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
