import customtkinter as ctk
from view.view_Tkinter.vista_msgbox.msgbox_library import msg_id_no_encontrado
from mysql.connector import IntegrityError
from config.appearance import centrar_ventana

class VentanaBuscarEstudiante(ctk.CTk):
    """
        Inicializa la ventana para buscar estudiantes.
    """
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.id_input_dialog = ctk.CTkInputDialog(text="ID:", title="Escriba ID a buscar")
        centrar_ventana(self.id_input_dialog,0.2,0.2)
        self.id_a_buscar = self.id_input_dialog.get_input()

        if self.id_a_buscar:
            
            # obtener la lista de IDs
            lista_ids = self.obtener_lista_ids_estudiante()

            if self.id_a_buscar in lista_ids:
                
                # Si la ventana de buscar está cerrada, cambiar su atributo a "True" y abrir la ventana
                self.parent.ventana_buscar_esta_abierta = True
                self.mostrar_detalles_estudiante()
            else:
                msg_id_no_encontrado(self.id_a_buscar)
    
    def obtener_lista_ids_estudiante(self):
        """
            Retorna una lista de los IDs presentes en la tabla
        """
        lista_ids = self.parent.frame_tabla_estudiantes.tabla_estudiantes.get_children()
        return lista_ids

    def obtener_detalles_estudiante_por_id(self):
        try:
            estudiante = self.parent.controlador_estudiante.obtener_estudiante_por_id(self.id_a_buscar)
            if estudiante:
                return estudiante
            else:
                #print("Estudiante no encontrado")
                return
        except Exception as e:
            pass
            #print(f"Error del estudiante: {str(e)}")
    
    def mostrar_detalles_estudiante(self):
        estudiante = self.obtener_detalles_estudiante_por_id()

        self.ventana_resultados = ctk.CTk()
        centrar_ventana(self.ventana_resultados,0.25,0.35)
        self.ventana_resultados.columnconfigure(0,weight=1)
        self.ventana_resultados.columnconfigure(1,weight=1)

        self.ventana_resultados.title("Resultados de estudiante")
        row_number = 0
        self.label_titulo = ctk.CTkLabel(self.ventana_resultados, text=f"Detalle de estudiante con ID: {self.id_a_buscar}",font=("Helvetica", 14, "bold"))
        self.label_titulo.grid(row = row_number, column = 0, columnspan=2, pady=(10,10))
        
        row_number +=1
        self.label_nombre = ctk.CTkLabel(self.ventana_resultados, text="Nombre:")
        self.label_nombre.grid(row = row_number, column = 0, padx=20, pady=5)
        self.entry_nombre = ctk.CTkLabel(self.ventana_resultados, text=estudiante.nombre)
        self.entry_nombre.grid(row = row_number, column = 1, padx=20, pady=5)

        row_number +=1
        self.label_apellido = ctk.CTkLabel(self.ventana_resultados, text="Apellido:")
        self.label_apellido.grid(row = row_number, column = 0, padx=20, pady=5)
        self.entry_apellido = ctk.CTkLabel(self.ventana_resultados, text=estudiante.apellido)
        self.entry_apellido.grid(row = row_number, column = 1, padx=20, pady=5)

        row_number +=1
        self.label_correo = ctk.CTkLabel(self.ventana_resultados, text="Correo:")
        self.label_correo.grid(row = row_number, column = 0, padx=20, pady=5)
        self.entry_correo = ctk.CTkLabel(self.ventana_resultados, text=estudiante.correo)
        self.entry_correo.grid(row = row_number, column = 1, padx=20, pady=5)

        row_number +=1
        self.label_telefono = ctk.CTkLabel(self.ventana_resultados, text="Teléfono:")
        self.label_telefono.grid(row = row_number, column = 0, padx=20, pady=5)
        self.entry_telefono = ctk.CTkLabel(self.ventana_resultados, text=estudiante.telefono)
        self.entry_telefono.grid(row = row_number, column = 1, padx=20, pady=5)

        row_number +=1
        self.btn_ok = ctk.CTkButton(self.ventana_resultados, text="OK", command=self.cerrar_resultados)
        self.btn_ok.grid(row = row_number, column = 0, columnspan=2, padx=20, pady=(10,30))

        for i in range(row_number):
            self.ventana_resultados.rowconfigure(i,weight=1)
        
        self.ventana_resultados.protocol("WM_DELETE_WINDOW", self.cerrar_resultados)
        self.ventana_resultados.mainloop()

    def cerrar_resultados(self):
        self.parent.ventana_buscar_esta_abierta = False
        self.ventana_resultados.destroy()
        
        
        


