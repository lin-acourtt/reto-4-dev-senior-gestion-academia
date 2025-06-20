import customtkinter as ctk
from view.view_Tkinter.vista_msgbox.msgbox_library import msg_id_no_encontrado
from mysql.connector import IntegrityError
from config.appearance import centrar_ventana

class VentanaBuscarCurso(ctk.CTk):
    """
        Inicializa la ventana para buscar cursos.
    """
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

        self.id_input_dialog = ctk.CTkInputDialog(text="ID:", title="Escriba ID a buscar")
        centrar_ventana(self.id_input_dialog,0.2,0.2)
        self.id_a_buscar = self.id_input_dialog.get_input()

        if self.id_a_buscar:
            
            # obtener la lista de IDs
            lista_ids = self.obtener_lista_ids_curso()

            if self.id_a_buscar in lista_ids:
                
                # Si la ventana de buscar está cerrada, cambiar su atributo a "True" y abrir la ventana
                self.parent.ventana_buscar_esta_abierta = True
                self.mostrar_detalles_curso()
            else:
                msg_id_no_encontrado(self.id_a_buscar)
    
    def obtener_lista_ids_curso(self):
        """
            Retorna una lista de los IDs presentes en la tabla
        """
        lista_ids = self.parent.frame_tabla_cursos.tabla_cursos.get_children()
        return lista_ids

    def obtener_detalles_curso_por_id(self):
        try:
            curso = self.parent.controlador_curso.obtener_curso_por_id(self.id_a_buscar)
            if curso:
                return curso
            else:
                #print("Estudiante no encontrado")
                return
        except Exception as e:
            pass
            #print(f"Error del estudiante: {str(e)}")
    
    def mostrar_detalles_curso(self):
        curso = self.obtener_detalles_curso_por_id()

        self.ventana_resultados = ctk.CTk()
        centrar_ventana(self.ventana_resultados,0.35,0.45)
        

        # Ejecuta la función "cerrar_resultados", para poder regresar en caso de que se cierre la ventana con el botón cerrar
        self.ventana_resultados.protocol("WM_DELETE_WINDOW",self.cerrar_resultados)

        self.ventana_resultados.title("Resultados de curso")
        row_number = 0
        self.label_titulo = ctk.CTkLabel(self.ventana_resultados, text=f"Detalle de curso con ID: {self.id_a_buscar}",font=("Helvetica", 14, "bold"))
        self.label_titulo.grid(row = row_number, column = 0, columnspan=2, pady=(10,10))
        
        row_number +=1
        self.label_nombre = ctk.CTkLabel(self.ventana_resultados, text="Nombre:")
        self.label_nombre.grid(row = row_number, column = 0, padx=20, pady=5)
        self.entry_nombre = ctk.CTkLabel(self.ventana_resultados, text=curso.nombre)
        self.entry_nombre.grid(row = row_number, column = 1, padx=20, pady=5)

        row_number +=1
        self.label_profesor = ctk.CTkLabel(self.ventana_resultados, text="Profesor:")
        self.label_profesor.grid(row = row_number, column = 0, padx=20, pady=5)
        self.entry_profesor = ctk.CTkLabel(self.ventana_resultados, text=curso.profesor)
        self.entry_profesor.grid(row = row_number, column = 1, padx=20, pady=5)

        row_number +=1
        self.label_num_est = ctk.CTkLabel(self.ventana_resultados, text="Número de estudiantes:")
        self.label_num_est.grid(row = row_number, column = 0, padx=20, pady=5)
        self.entry_num_est = ctk.CTkLabel(self.ventana_resultados, text=curso.num_estudiantes)
        self.entry_num_est.grid(row = row_number, column = 1, padx=20, pady=5)

        row_number +=1
        self.label_horarios = ctk.CTkLabel(self.ventana_resultados, text="Horarios:")
        self.label_horarios.grid(row = row_number, column = 0, padx=20, pady=5)
        #self.entry_horarios = ctk.CTkLabel(self.ventana_resultados, text=curso.horarios)
        self.entry_horarios = ctk.CTkEntry(self.ventana_resultados)
        self.entry_horarios.insert(0,curso.horarios)
        self.entry_horarios.grid(row = row_number, column = 1, padx=20, pady=5, sticky='ew')

        row_number +=1
        self.label_descripcion = ctk.CTkLabel(self.ventana_resultados, text="Descripción:")
        self.label_descripcion.grid(row = row_number, column = 0, padx=20, pady=5)
        #self.entry_descripcion = ctk.CTkLabel(self.ventana_resultados, text=curso.descripcion)
        self.entry_descripcion = ctk.CTkEntry(self.ventana_resultados)
        self.entry_descripcion.insert(0,curso.descripcion)
        self.entry_descripcion.grid(row = row_number, column = 1, padx=20, pady=5, sticky="ew")

        row_number +=1
        self.label_duracion = ctk.CTkLabel(self.ventana_resultados, text="Duración (horas):")
        self.label_duracion.grid(row = row_number, column = 0, padx=20, pady=5)
        self.entry_duracion = ctk.CTkLabel(self.ventana_resultados, text=curso.duracion_horas)
        self.entry_duracion.grid(row = row_number, column = 1, padx=20, pady=5)

        invisible_label = ctk.CTkLabel(self.ventana_resultados, text="")
        invisible_label.grid(row=row_number, column=2)
        row_number +=1
        self.btn_ok = ctk.CTkButton(self.ventana_resultados, text="OK", command=self.cerrar_resultados)
        self.btn_ok.grid(row = row_number, column = 0, columnspan=2, padx=20, pady=(10,30))
        
        for i in range(row_number):
            self.ventana_resultados.rowconfigure(i,weight=1)
        
        self.ventana_resultados.columnconfigure(0,weight=1)
        self.ventana_resultados.columnconfigure(1,weight=2)

        self.ventana_resultados.mainloop()

    def cerrar_resultados(self):
        self.parent.ventana_buscar_esta_abierta = False
        self.ventana_resultados.destroy()
        
        
        


