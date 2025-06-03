import customtkinter as ctk
from view.view_Tkinter.vista_msgbox.msgbox_library import msg_id_no_encontrado
from mysql.connector import IntegrityError
from config.appearance import centrar_ventana

class VentanaBuscarMatricula(ctk.CTk):
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
            lista_ids = self.obtener_lista_ids_matricula()

            if self.id_a_buscar in lista_ids:
                
                # Si la ventana de buscar está cerrada, cambiar su atributo a "True" y abrir la ventana
                self.parent.ventana_buscar_esta_abierta = True
                self.mostrar_detalles_matricula()
            else:
                msg_id_no_encontrado(self.id_a_buscar)
    
    def obtener_lista_ids_matricula(self):
        """
            Retorna una lista de los IDs presentes en la tabla
        """
        lista_ids = self.parent.frame_tabla_matriculas.tabla_matriculas.get_children()
        return lista_ids

    def obtener_detalles_matricula_por_id(self):
        try:
            matricula = self.parent.controlador_matricula.obtener_matricula_por_id(self.id_a_buscar)
            if matricula:
                return matricula
            else:
                #print("Estudiante no encontrado")
                return
        except Exception as e:
            pass
            #print(f"Error del estudiante: {str(e)}")
    
    def mostrar_detalles_matricula(self):
        matricula = self.obtener_detalles_matricula_por_id()

        self.ventana_resultados = ctk.CTk()
        centrar_ventana(self.ventana_resultados,0.3)
        self.ventana_resultados.columnconfigure(0,weight=1)
        self.ventana_resultados.columnconfigure(1,weight=1)

        self.ventana_resultados.title("Resultados de matricula")
        row_number = 0
        self.label_titulo = ctk.CTkLabel(self.ventana_resultados, text=f"Detalle de matricula con ID: {self.id_a_buscar}",font=("Helvetica", 14, "bold"))
        self.label_titulo.grid(row = row_number, column = 0, columnspan=2, pady=(10,10))
        
        estudiante = self.parent.frame_tabla_matriculas.tabla_matriculas.item(self.id_a_buscar)['values'][1]
        curso = self.parent.frame_tabla_matriculas.tabla_matriculas.item(self.id_a_buscar)['values'][2]
        fecha = self.parent.frame_tabla_matriculas.tabla_matriculas.item(self.id_a_buscar)['values'][3]

        row_number +=1
        self.label_estudiante = ctk.CTkLabel(self.ventana_resultados, text="Estudiante:")
        self.label_estudiante.grid(row = row_number, column = 0, padx=20, pady=5)
        self.entry_estudiante = ctk.CTkLabel(self.ventana_resultados, text=estudiante)
        self.entry_estudiante.grid(row = row_number, column = 1, padx=20, pady=5)        
        row_number +=1
        self.label_curso = ctk.CTkLabel(self.ventana_resultados, text="Curso:")
        self.label_curso.grid(row = row_number, column = 0, padx=20, pady=5)
        self.entry_curso = ctk.CTkLabel(self.ventana_resultados, text=curso)
        self.entry_curso.grid(row = row_number, column = 1, padx=20, pady=5)

        row_number +=1
        self.label_fecha = ctk.CTkLabel(self.ventana_resultados, text="FEcha:")
        self.label_fecha.grid(row = row_number, column = 0, padx=20, pady=5)
        self.entry_fecha = ctk.CTkLabel(self.ventana_resultados, text=fecha)
        self.entry_fecha.grid(row = row_number, column = 1, padx=20, pady=5)

        row_number +=1
        self.btn_ok = ctk.CTkButton(self.ventana_resultados, text="OK", command=self.cerrar_resultados)
        self.btn_ok.grid(row = row_number, column = 0, columnspan=2, padx=20, pady=10)

        self.ventana_resultados.mainloop()

    def cerrar_resultados(self):
        self.parent.ventana_buscar_esta_abierta = False
        self.ventana_resultados.destroy()
        
        
        


