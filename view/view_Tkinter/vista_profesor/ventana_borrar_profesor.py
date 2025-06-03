import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from mysql.connector import IntegrityError
from config.appearance import centrar_ventana
from view.view_Tkinter.vista_msgbox.msgbox_library import msg_eliminacion_exitosa, msg_sin_cambios, msg_error_integrity, msg_error_inesperado

class VentanaBorrarProfesor(ctk.CTk):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        
        centrar_ventana(self,0.3,0.2)
        self.resizable(False, False)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)

        self.title("Confirmación")
        self.label_titulo = ctk.CTkLabel(self, text="Borrar profesor",font=("Helvetica", 14, "bold"))
        #self.label_titulo.grid(row = 0, column = 0, columnspan=2)
        self.label_titulo.pack(pady=10)

        # Se obtienen el ID del profesor seleccionado en la tabla
        iid_sel = self.parent.frame_tabla_profesores.tabla_profesores.selection()[0]
        self.label_msj = ctk.CTkLabel(self, text=f"¿Acepta borrar el profesor con ID: {iid_sel}?")
        #self.label_msj.grid(row = 1, column = 0, columnspan=2)
        self.label_msj.pack(pady=10)
        
        self.frame_botones = ctk.CTkFrame(self)

        self.btn_confirmar = ctk.CTkButton(self.frame_botones, text="Sí", command=lambda: self.confirmar_borrado(iid_sel))
        self.btn_confirmar.grid(row = 2, column = 0, padx=20, pady=(5,5))
        #self.btn_confirmar.pack()
        
        self.btn_cancelar = ctk.CTkButton(self.frame_botones, text="Cancelar", command=self.cancelar_borrado)
        self.btn_cancelar.grid(row = 2, column = 1, padx=20, pady=(5,5))
        #self.btn_cancelar.pack()

        self.frame_botones.pack()

        self.protocol("WM_DELETE_WINDOW", self.cancelar_borrado)

    def confirmar_borrado(self,id_sel):

        try:
            # Se utiliza el controlador profesor para eliminar un estudiante por el ID especificado
            self.parent.controlador_profesor.eliminar_profesor_por_id(id_sel)
            
            # Actualizar tabla en el tree view
            self.parent.frame_tabla_profesores.tabla_profesores.delete(id_sel)
            
            # Dar un mensaje de confirmación
            msg_eliminacion_exitosa("Profesor")
            self.actualizar_estado_ventana_al_cerrar()
        except IntegrityError as e:
            msg_error_integrity("profesor",str(e.msg))
        except Exception as e: 
            msg_error_inesperado("profesor",str(e))


    def cancelar_borrado(self):
        msg_sin_cambios()
        self.actualizar_estado_ventana_al_cerrar()

    def actualizar_estado_ventana_al_cerrar(self):
        self.parent.ventana_borrar_esta_abierta = False
        self.destroy()
