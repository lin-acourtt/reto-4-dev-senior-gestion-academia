import customtkinter as ctk
from view.view_Tkinter.vista_msgbox.msgbox_library import msg_sin_cambios, msg_registro_exitoso, msg_error_campos_vacios, msg_entrada_duplicada, msg_error_integrity, msg_error_inesperado, msg_error_cargar_datos, msg_conflicto_horas
from mysql.connector import IntegrityError
from config.appearance import centrar_ventana
from controllers.horario_controller import HorarioController
from controllers.curso_controller import CursoController


class VentanaRegistrarHorarioDesdeMenuCurso(ctk.CTkToplevel):
    """
        Inicializa la ventana para registrar horarios desde la ventana de cursos.
    """
    dias = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado']
    horas = ['06:00','06:30','07:00','07:30','08:00','08:30',
             '09:00','09:30','10:00','10:30','11:00','11:30',
             '12:00','12:30','13:00','13:30','14:00','14:30',
             '15:00','15:30','15:00','15:30','16:00','16:30',
             '17:00','17:30','18:00','18:30','19:00','19:30',
             '20:00','20:30','21:00','21:30','22:00','22:30',]
    
    def __init__(self, parent=None):
        """
            Se debe definir el parent, que sería la ventana de "MenuCurso" y la base de datos
        """
        super().__init__()
        self.parent = parent

        # El parent ya viene con los sgtes controladores, no es necesario volverlos a crear:
        # El método constructor asegura que el atributo "db" sea de tipo "Database""
        # self.parent.controlador_curso 
        # self.parent.controlador_profesor
        # self.parent.controlador_horario 
        # self.parent.controlador_matricula

        # Obtener el curso seleccionado
        seleccion = self.parent.frame_tabla_cursos.tabla_cursos.selection()
        valores = self.parent.frame_tabla_cursos.tabla_cursos.item(seleccion[0])['values']
        self.curso_id = valores[0]
        self.curso_nombre = valores[1]  # El nombre del curso está en la segunda columna
        
        self.title("Registro de un nuevo horario")
        centrar_ventana(self,0.4)
        self.resizable(False, False)
        
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        row_number = 0

        # Título en la ventana
        self.label_titulo = ctk.CTkLabel(self, text="Registrar nuevo horario", font=("Helvetica", 14, "bold"))
        self.label_titulo.grid(row = 0, column = 0, columnspan=2, pady=(10,10))

        # Mostrar curso seleccionado
        row_number += 1
        self.label_curso_seleccionado = ctk.CTkLabel(self, text=f"Curso: {self.curso_nombre}", font=("Helvetica", 12))
        self.label_curso_seleccionado.grid(row = row_number, column = 0, columnspan=2, pady=(10,10))

        # Día de semana
        row_number += 1
        self.label_dia = ctk.CTkLabel(self, text="Día de semana:")
        self.label_dia.grid(row = row_number, column= 0, padx=(10,10), pady=(5,5))
        self.cobox_dia = ctk.CTkComboBox(self)
        self.cobox_dia.grid(row = row_number, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        self.cobox_dia.configure(state='readonly')
        
        # Hora Inicio
        row_number += 1
        self.label_hora_inicio = ctk.CTkLabel(self, text="Hora de inicio:")
        self.label_hora_inicio.grid(row = row_number, column= 0, padx=(10,10), pady=(5,5))
        self.cobox_hora_inicio = ctk.CTkComboBox(self)
        self.cobox_hora_inicio.grid(row = row_number, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        self.cobox_hora_inicio.configure(state='readonly')

        # Hora Fin
        row_number += 1
        self.label_hora_fin = ctk.CTkLabel(self, text="Hora de fin:")
        self.label_hora_fin.grid(row = row_number, column= 0, padx=(10,10), pady=(5,5))
        self.cobox_hora_fin = ctk.CTkComboBox(self)
        self.cobox_hora_fin.grid(row = row_number, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        self.cobox_hora_fin.configure(state='readonly')
        
        row_number += 1
        # Botón de guardado    
        self.btn_guardar = ctk.CTkButton(self, text="Guardar", command=self.guardar_registro)
        self.btn_guardar.grid(row = row_number, column = 0, padx=(0,20), pady=(15,30))
        # Botón de cancelar    
        self.btn_cancelar = ctk.CTkButton(self, text="Cancelar", command=self.cancelar_registro)
        self.btn_cancelar.grid(row = row_number, column = 1, padx=(0,20), pady=(15,30))

        for i in range(row_number):
            self.rowconfigure(i,weight=1)

        # Cargar las opciones en los combobox
        self.cargar_dias_en_cobox()
        self.cargar_horas_en_cobox()
        
        self.protocol("WM_DELETE_WINDOW", self.cancelar_registro)

    def cargar_dias_en_cobox(self):
        """Carga los días de la semana en el combobox de días"""
        self.cobox_dia.configure(values=self.dias)
        self.cobox_dia.set(self.dias[0])

    def cargar_horas_en_cobox(self):
        """Carga las horas en los combobox de hora inicio y fin"""
        self.cobox_hora_inicio.configure(values=self.horas)
        self.cobox_hora_inicio.set(self.horas[0])
        
        self.cobox_hora_fin.configure(values=self.horas)
        self.cobox_hora_fin.set(self.horas[1])

    def obtener_informacion_formulario_registro(self):
        """
            Obtiene la información ingresada en el formulario
            Retorna:
            - dia_semana: Día de la semana seleccionado
            - hora_inicio: Hora de inicio seleccionada
            - hora_fin: Hora de fin seleccionada
        """
        dia_semana = self.cobox_dia.get()
        hora_inicio = self.cobox_hora_inicio.get()
        hora_fin = self.cobox_hora_fin.get()

        idx_hora_inicio = VentanaRegistrarHorarioDesdeMenuCurso.horas.index(hora_inicio)
        idx_hora_fin = VentanaRegistrarHorarioDesdeMenuCurso.horas.index(hora_fin)

        if idx_hora_fin <= idx_hora_inicio:
            msg_conflicto_horas()
            return
        
        return dia_semana, hora_inicio, hora_fin

    def guardar_registro(self):
        """
            Registra un nuevo horario para el curso seleccionado
        """
        # Obtener la información del formulario
        dia_semana, hora_inicio, hora_fin = self.obtener_informacion_formulario_registro()

        try:
            # Utilizar el controlador de horario para registrar un nuevo horario
            self.parent.controlador_horario.registrar_horario(
                curso_id=self.curso_id,
                dia_semana=dia_semana,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin
            )
            
            # Mostrar un mensaje de registro exitoso
            msg_registro_exitoso("horario")
            
            # Actualizar la tabla de cursos
            cursos = self.parent.obtener_lista_cursos()
            if cursos:
                self.parent.frame_tabla_cursos.imprimir_informacion_en_tabla(cursos)
            else:
                msg_error_inesperado("Error al actualizar la tabla de cursos")
            
            # Cerrar la ventana
            self.cerrar_registro()
            
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                msg_entrada_duplicada("horario")
            else:
                msg_error_integrity()
        except Exception as e:
            if "Conflicto de horarios" in str(e):
                msg_conflicto_horas()
            else:
                msg_error_inesperado(str(e))

    def cerrar_registro(self):
        """
            Cierra la ventana y actualiza el estado
        """
        self.parent.ventana_registrar_horario_esta_abierta = False
        self.destroy() 
    
    def cancelar_registro(self):
        """
            Cierra la ventana y actualiza el estado
        """
        msg_sin_cambios()
        self.parent.ventana_registrar_horario_esta_abierta = False
        self.destroy() 
