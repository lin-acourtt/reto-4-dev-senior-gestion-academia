import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from mysql.connector import IntegrityError
from config.appearance import centrar_ventana

class VentanaActualizarEstudiante(ctk.CTk):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        
        centrar_ventana(self,proporcion=0.25)
        self.title("Actualizar estudiante")
        self.label_titulo = ctk.CTkLabel(self, text="Actualización de estudiante")
        self.label_titulo.grid(row = 0, column = 0, columnspan=2)

        # Se obtienen los datos del estudiante seleccionado en la tabla
        iid_sel = self.parent.frame_tabla_estudiantes.tabla_estudiantes.selection()[0]
        nombre_sel = self.parent.frame_tabla_estudiantes.tabla_estudiantes.item(iid_sel)['values'][1]
        apellido_sel = self.parent.frame_tabla_estudiantes.tabla_estudiantes.item(iid_sel)['values'][2]
        correo_sel = self.parent.frame_tabla_estudiantes.tabla_estudiantes.item(iid_sel)['values'][3]
        telefono_sel = self.parent.frame_tabla_estudiantes.tabla_estudiantes.item(iid_sel)['values'][4]
        
        strvar_nombre = ctk.StringVar(self,nombre_sel)
        self.entry_nombre = ctk.CTkEntry(self, textvariable=strvar_nombre)
        self.entry_nombre.grid(row = 1, column = 0, padx=20, pady=5)

        strvar_apellido = ctk.StringVar(self,apellido_sel)
        self.entry_apellido = ctk.CTkEntry(self, textvariable=strvar_apellido)
        self.entry_apellido.grid(row = 2, column = 0, padx=20, pady=5)

        strvar_correo = ctk.StringVar(self,correo_sel)
        self.entry_correo = ctk.CTkEntry(self, textvariable=strvar_correo)
        self.entry_correo.grid(row = 3, column = 0, padx=20, pady=5)

        strvar_tel = ctk.StringVar(self,telefono_sel)
        self.entry_telefono = ctk.CTkEntry(self, textvariable=strvar_tel)
        self.entry_telefono.grid(row = 4, column = 0, padx=20, pady=5)

        self.btn_guardar = ctk.CTkButton(self, text="Actualizar", command=lambda: self.guardar_registro(iid_sel))
        self.btn_guardar.grid(row = 2, column = 1)
        
        self.btn_cancelar = ctk.CTkButton(self, text="Cancelar", command=self.cancelar_registro)
        self.btn_cancelar.grid(row = 3, column = 1)

        self.protocol("WM_DELETE_WINDOW", self.actualizar_estado_ventana_al_cerrar)

    def guardar_registro(self,id_sel):
        # Obtener los datos en los elementos de "Entry"
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        correo = self.entry_correo.get()
        telefono = self.entry_telefono.get()

        try:
            # Utilizar el controlador de estudiante para actualizar los datos de dicho estudiante
            self.parent.controlador_estudiante.actualizar_estudiante_por_id(id_sel,nombre,apellido,correo,telefono)
            
            # Actualizar los valores del estudiante en la tabla
            self.parent.frame_tabla_estudiantes.tabla_estudiantes.item(
                id_sel,
                values=(
                    id_sel,
                    nombre,
                    apellido,
                    correo,
                    telefono
                )
            )

            # Mostrar un mensaje de confirmación
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
        self.parent.ventana_actualizacion_esta_abierta = False
        self.destroy()
