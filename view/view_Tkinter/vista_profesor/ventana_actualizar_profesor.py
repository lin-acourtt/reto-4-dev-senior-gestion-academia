import customtkinter as ctk
from view.view_Tkinter.vista_msgbox.msgbox_library import msg_sin_cambios, msg_registro_exitoso, msg_error_campos_vacios, msg_entrada_duplicada, msg_error_integrity, msg_error_inesperado
from mysql.connector import IntegrityError
from config.appearance import centrar_ventana

class VentanaActualizarProfesor(ctk.CTk):
    """
        Inicializa la ventana para actualizar profesores.
    """
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        
        row_number = 0

        centrar_ventana(self,0.25,0.40)
        self.resizable(False, False)
        self.title("Actualizar profesor")
        self.label_titulo = ctk.CTkLabel(self, text="Actualización de profesor",font=("Helvetica", 14, "bold"))
        self.label_titulo.grid(row = row_number, column = 0, columnspan=2,pady=(10,10))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.strvar_nombre = ctk.StringVar(self,"")
        self.strvar_apellido = ctk.StringVar(self,"")
        self.strvar_correo = ctk.StringVar(self,"")
        self.strvar_tel = ctk.StringVar(self,"")
        self.strvar_esp = ctk.StringVar(self,"")

        # Actualizar los campos de las entries, con la información del profesor seleccionado
        self.actualizar_informacion_campos()
        
        row_number +=1
        self.label_nombre = ctk.CTkLabel(self, text="Nombre:")
        self.label_nombre.grid(row = row_number, column = 0, padx=20, pady=(5,5))
        self.entry_nombre = ctk.CTkEntry(self, textvariable=self.strvar_nombre)
        self.entry_nombre.grid(row = row_number, column = 1, padx=(5,20), pady=(5,5), sticky="ew")

        row_number +=1
        self.label_apellido = ctk.CTkLabel(self, text="Apellido:")
        self.label_apellido.grid(row = row_number, column = 0, padx=20, pady=(5,5))
        self.entry_apellido = ctk.CTkEntry(self, textvariable=self.strvar_apellido)
        self.entry_apellido.grid(row = row_number, column = 1, padx=(5,20), pady=(5,5), sticky="ew")

        row_number +=1
        self.label_correo = ctk.CTkLabel(self, text="Correo:")
        self.label_correo.grid(row = row_number, column = 0, padx=20, pady=(5,5))
        self.entry_correo = ctk.CTkEntry(self, textvariable=self.strvar_correo)
        self.entry_correo.grid(row = row_number, column = 1, padx=(5,20), pady=(5,5), sticky="ew")

        row_number +=1
        self.label_telefono = ctk.CTkLabel(self, text="Teléfono:")
        self.label_telefono.grid(row = row_number, column = 0, padx=20, pady=(5,5))
        self.entry_telefono = ctk.CTkEntry(self, textvariable=self.strvar_tel)
        self.entry_telefono.grid(row = row_number, column = 1, padx=(5,20), pady=(5,5), sticky="ew")

        row_number +=1
        self.label_especialidad = ctk.CTkLabel(self, text="Especialidad:")
        self.label_especialidad.grid(row = row_number, column = 0, padx=20, pady=5)
        self.entry_especialidad = ctk.CTkEntry(self, textvariable=self.strvar_esp)
        self.entry_especialidad.grid(row = row_number, column = 1, padx=(5,20), pady=(5,5), sticky="ew")

        row_number +=1
        self.btn_guardar = ctk.CTkButton(self, text="Actualizar", command=lambda: self.guardar_registro(self.iid_sel))
        self.btn_guardar.grid(row = row_number, column = 0, padx=(30,30), pady=(15,15))
        
        self.btn_cancelar = ctk.CTkButton(self, text="Cancelar", command=self.cancelar_actualizacion)
        self.btn_cancelar.grid(row = row_number, column = 1, padx=(30,30), pady=(15,15))

        self.protocol("WM_DELETE_WINDOW", self.cancelar_actualizacion)

    def actualizar_informacion_campos(self):
        """
            Actualizar los campos de las entries, con la información del profesor seleccionado
        """
        self.obtener_valores_de_seleccion()
        # Resultado, actualización de los atributos
        # - self.iid_sel
        # - self.nombre_sel
        # - self.apellido_sel
        # - self.correo_sel
        # - self.telefono_sel
        # - self.especialidad_sel

        self.actualizar_strvars()
        # Resultado, actualización de los atributos
        # - self.strvar_nombre
        # - self.strvar_apellido
        # - self.strvar_correo
        # - self.strvar_tel
        # - self.strvar_esp

    def obtener_valores_de_seleccion(self):
        """
            Obtiene los valores de la tabla según la selección que se haga
        """
        self.iid_sel = self.parent.frame_tabla_profesores.tabla_profesores.selection()[0]
        self.nombre_sel = self.parent.frame_tabla_profesores.tabla_profesores.item(self.iid_sel)['values'][1]
        self.apellido_sel = self.parent.frame_tabla_profesores.tabla_profesores.item(self.iid_sel)['values'][2]
        self.correo_sel = self.parent.frame_tabla_profesores.tabla_profesores.item(self.iid_sel)['values'][3]
        self.telefono_sel = self.parent.frame_tabla_profesores.tabla_profesores.item(self.iid_sel)['values'][4]
        self.especialidad_sel = self.parent.frame_tabla_profesores.tabla_profesores.item(self.iid_sel)['values'][5]
    
    def actualizar_strvars(self):
        """
            Actualiza los valores de los StringVars que llenan los campos de texto con la información del profesor.
        """
        self.strvar_nombre.set(self.nombre_sel)
        self.strvar_apellido.set(self.apellido_sel)
        self.strvar_correo.set(self.correo_sel)
        self.strvar_tel.set(self.telefono_sel)
        self.strvar_esp.set(self.especialidad_sel)
        

    def guardar_registro(self,id_sel):
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
            
            if (str(nombre)==str(self.nombre_sel)) and (str(apellido) == str(self.apellido_sel)) and (str(correo) == str(self.correo_sel)) and (str(telefono) == str(self.telefono_sel)) and (str(especialidad) == str(self.especialidad_sel)):
                # Se regresa y no se hace ningún cambio
                self.cancelar_actualizacion()
                return

            # Utilizar el controlador de profesor para actualizar los datos de dicho profesor
            self.parent.controlador_profesor.actualizar_profesor_por_id(id_sel,nombre,apellido,correo,telefono,especialidad)
            
            # Actualizar los valores del profesor en la tabla
            self.parent.frame_tabla_profesores.tabla_profesores.item(
                id_sel,
                values=(
                    id_sel,
                    nombre,
                    apellido,
                    correo,
                    telefono,
                    especialidad
                )
            )

            # Mostrar un mensaje de confirmación
            msg_registro_exitoso("Profesor")
            self.actualizar_estado_ventana_al_cerrar()
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                msg_entrada_duplicada("profesor")
            else:
                msg_error_integrity("profesor",str(e))
        except Exception as e:
            msg_error_inesperado(str(e))

    def cancelar_actualizacion(self):
        msg_sin_cambios()
        self.actualizar_estado_ventana_al_cerrar()

    def actualizar_estado_ventana_al_cerrar(self):
        self.parent.ventana_actualizacion_esta_abierta = False
        self.destroy()
