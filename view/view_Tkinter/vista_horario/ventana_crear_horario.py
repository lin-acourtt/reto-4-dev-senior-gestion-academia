import customtkinter as ctk
from view.view_Tkinter.vista_msgbox.msgbox_library import msg_sin_cambios, msg_registro_exitoso, msg_error_campos_vacios, msg_entrada_duplicada, msg_error_integrity, msg_error_inesperado, msg_error_cargar_datos, msg_conflicto_horas
from mysql.connector import IntegrityError
from config.appearance import centrar_ventana

class VentanaCrearHorario(ctk.CTk):
    """
        Inicializa la ventana para crear nuevos horarios.
    """
    dias = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado']
    horas = ['06:00','06:30','07:00','07:30','08:00','08:30',
             '09:00','09:30','10:00','10:30','11:00','11:30',
             '12:00','12:30','13:00','13:30','14:00','14:30',
             '15:00','15:30','15:00','15:30','16:00','16:30',
             '17:00','17:30','18:00','18:30','19:00','19:30',
             '20:00','20:30','21:00','21:30','22:00','22:30',]
    
    def __init__(self, parent=None, tipo: int=1):
        """
            Se debe definir el parent, que sería la ventana de "MenuHorario" y el tipo, que tiene 2 opciones
            1: Crear Horario
            2: Modificar horario
        """
        super().__init__()
        self.parent = parent
        self.tipo = tipo
        
        centrar_ventana(self,0.4)
        self.resizable(False, False)
        
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        row_number = 0

        # Título en la ventana
        self.label_titulo = ctk.CTkLabel(self,font=("Helvetica", 14, "bold"))
        self.label_titulo.grid(row = 0, column = 0, columnspan=2,pady=(10,10))

        # Nombre del curso
        row_number += 1
        self.label_curso = ctk.CTkLabel(self, text="Curso:")
        self.label_curso.grid(row = row_number, column= 0, padx=(10,10), pady=(5,5))
        self.cobox_curso = ctk.CTkComboBox(self)
        self.cobox_curso.grid(row = row_number, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        self.cobox_curso.configure(state='readonly')
        
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

        # Profesor
        row_number += 1
        self.label_hora_fin = ctk.CTkLabel(self, text="Hora de fin:")
        self.label_hora_fin.grid(row = row_number, column= 0, padx=(10,10), pady=(5,5))
        self.cobox_hora_fin = ctk.CTkComboBox(self)
        self.cobox_hora_fin.grid(row = row_number, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        self.cobox_hora_fin.configure(state='readonly')
        
        row_number += 1
        # Botón de guardado    
        self.btn_guardar = ctk.CTkButton(self)
        self.btn_guardar.grid(row = row_number, column = 0, padx=(0,20), pady=15)
        # Botón de cancelar    
        self.btn_cancelar = ctk.CTkButton(self, text="Cancelar", command=self.cancelar_registro)
        self.btn_cancelar.grid(row = row_number, column = 1, padx=(0,20),pady=15)

        # self.detalles_curso
        # contiene los items por separado
        # self.lista_cursos
        # contiene los items concatenados
        self.obtener_lista_id_cursos() # Obtiene 3 listas de cursos, ver doc.
        
        if self.tipo == 1:
            # Si es una ventana de creación de nuevo horario, se configuran los siguientes parámetros
            self.title("Crear nuevo horario")
            self.label_titulo.configure(text="Crear nuevo horario")
            self.cargar_cursos_en_cobox()
            self.cargar_dias_en_cobox()
            self.cargar_horas_en_cobox()
            # Botón de guardado    
            self.btn_guardar.configure(text="Guardar", command=self.guardar_registro)
        elif self.tipo == 2:
            # Si es una ventana de actualización de nuevo horario, se configuran los siguientes parámetros
            self.title("Editar horario")
            self.label_titulo.configure(text="Actualización de horario")

            self.actualizar_informacion_campos()

            # Actualizar los campos de las entries, con la información del horario seleccionado
            self.cargar_cursos_en_cobox()
            self.cargar_dias_en_cobox()
            self.cargar_horas_en_cobox()

            # Botón de guardado    
            self.btn_guardar.configure(text="Actualizar", command=self.actualizar_registro)
            self.btn_guardar.grid(row = row_number, column = 0, padx=(0,20), pady=15)
        
        self.protocol("WM_DELETE_WINDOW", self.cancelar_registro)

    def obtener_lista_id_cursos(self):
        """
            Obtiene 3 listas de cursos y los guarda como atributos:
            - self.cursos: lista de objetos
            - self.detalles_cursos: lista con IDs y nombres [[id1,nombre1,curso1],[id2,curso2],etc]
            - self.lista_cursos: lista con IDs y nombres concatenados ['ID: 1 - Curso1','ID: 2 - Curso2',etc]
        """
        try:
            self.cursos, self.detalles_cursos, self.lista_cursos = self.parent.obtener_listas_cursos()
            
            if not self.cursos:
                raise Exception
        except Exception as e:
            msg_error_cargar_datos("curso",str(e))

    def cargar_cursos_en_cobox(self):
        """
            Se usa con ambas ventanas, guardar y actualizar
            Carga la lista de cursos en el combobox pertinente
        """
        self.cobox_curso.configure(values=self.lista_cursos)
        if self.tipo == 1:
            # Ventana de creación de horario
            self.cobox_curso.set(self.lista_cursos[0])
        if self.tipo == 2:
            # Ventana de actualización de horario

            # El detalle del profesor seleccionado, ya viene de la función self.actualizar_informacion_campos()
            self.cobox_curso.set(self.curso_sel)
    
    def cargar_dias_en_cobox(self):
        """
            Se usa con ambas ventanas, guardar y actualizar
            Carga la lista de días en el combobox pertinente
        """
        self.cobox_dia.configure(values=VentanaCrearHorario.dias)
        if self.tipo == 1:
            # Ventana de creación de horario
            self.cobox_dia.set(VentanaCrearHorario.dias[0])
        if self.tipo == 2:
            # Ventana de actualización de horario

            # El detalle del día seleccionado, ya viene de la función self.actualizar_informacion_campos()
            self.cobox_dia.set(self.dia_sel)
    
    def cargar_horas_en_cobox(self):
        """
            Se usa con ambas ventanas, guardar y actualizar
            Carga la lista de horas en el combobox pertinente
        """
        self.cobox_hora_inicio.configure(values=VentanaCrearHorario.horas)
        self.cobox_hora_fin.configure(values=VentanaCrearHorario.horas)
        if self.tipo == 1:
            # Ventana de creación de horario
            self.cobox_hora_inicio.set(VentanaCrearHorario.horas[0])
            self.cobox_hora_fin.set(VentanaCrearHorario.horas[1])
        if self.tipo == 2:
            # Ventana de actualización de horario

            # El detalle de las horas seleccionadas, ya viene de la función self.actualizar_informacion_campos()
            self.cobox_hora_inicio.set(self.hora_inicio_sel)
            self.cobox_hora_fin.set(self.hora_fin_sel)

    
    def actualizar_informacion_campos(self):
        """
            Se usa con ventana: editar horario
            Actualizar los campos de las entries, con la información del horario seleccionado
        """
        self.obtener_valores_de_seleccion()
        # Resultado, actualización de los atributos
        # - self.iid_sel
        # - self.curso_sel
        # - self.dia_sel
        # - self.hora_inicio_sel
        # - self.hora_fin_sel

        self.actualizar_strvars()
        # Resultado, actualización de los combo boxes

    def obtener_valores_de_seleccion(self):
        """
            Se usa con ventana: editar horario
            Obtiene los valores de la tabla según la selección que se haga
        """
        self.iid_sel = self.parent.frame_tabla_horarios.tabla_horarios.selection()[0]
        self.curso_sel = self.parent.frame_tabla_horarios.tabla_horarios.item(self.iid_sel)['values'][1]
        self.dia_sel = self.parent.frame_tabla_horarios.tabla_horarios.item(self.iid_sel)['values'][2]
        self.hora_inicio_sel = self.parent.frame_tabla_horarios.tabla_horarios.item(self.iid_sel)['values'][3]
        self.hora_fin_sel = self.parent.frame_tabla_horarios.tabla_horarios.item(self.iid_sel)['values'][4]
    
    def actualizar_strvars(self):
        """
            Se usa con ventana: editar horario
            Actualiza los valores de los StringVars que llenan los campos de texto con la información del estudiante.
        """
        self.cobox_curso.set(self.curso_sel)
        self.cobox_dia.set(self.dia_sel)
        self.cobox_hora_inicio.set(self.hora_inicio_sel)
        self.cobox_hora_fin.set(self.hora_fin_sel)

    def obtener_informacion_formulario_registro(self):
        """
            Se usa para obtener la información del formulario ya sea de registro o de actualización
        """
        try: 
            # Obtener los datos en los elementos de "Entry"
            curso_nombre = self.cobox_curso.get().strip()
            dia_semana = self.cobox_dia.get().strip()
            hora_inicio = self.cobox_hora_inicio.get().strip()
            hora_fin = self.cobox_hora_fin.get().strip()

            idx_hora_inicio = VentanaCrearHorario.horas.index(hora_inicio)
            idx_hora_fin = VentanaCrearHorario.horas.index(hora_fin)

            if idx_hora_fin <= idx_hora_inicio:
                msg_conflicto_horas()
                return

            # Se busca cuál es el ID del curso que corresponde al nombre seleccionado
            index_curso = 0
            for string_curso in self.lista_cursos:
                if curso_nombre == string_curso:
                    break
                index_curso +=1

            curso_id = self.detalles_cursos[index_curso][0]

            #print(profesor_id)
            # Validar campos
            if not all([curso_id, dia_semana, hora_inicio, hora_fin]):
                msg_error_campos_vacios()
                return
            
            return curso_id, dia_semana, hora_inicio, hora_fin
        
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                msg_entrada_duplicada("horario")
            else:
                msg_error_integrity("horario",str(e))
        except Exception as e:
            msg_error_inesperado(str(e))
    
    def guardar_registro(self):
        
        """
            Se usa para: Crear horario
            Actualiza la base de datos (tabla horarios), con la información del horario que se escribió en el formulario.
        """
        curso_id, dia_semana, hora_inicio, hora_fin = self.obtener_informacion_formulario_registro()

        # Utilizar el controlador de horario para registrar un nuevo horario
        self.parent.controlador_horario.registrar_horario(curso_id=curso_id, dia_semana=dia_semana, hora_inicio=hora_inicio, hora_fin=hora_fin)
        
        # Inserta el nuevo horario en la lista de horarios
        # (Se re-imprime toda la lista)
        horarios, cursos = self.parent.obtener_lista_horarios()
        self.parent.frame_tabla_horarios.imprimir_informacion_en_tabla(horarios, cursos)
        
        # Mostrar un mensaje de registro exitoso
        msg_registro_exitoso("horario")

        # Cierra la ventana y cambia el estado de esta ventana a cerrado
        self.actualizar_estado_ventana_al_cerrar()
        

    def actualizar_registro(self):
        """
            Se usa con la ventana: editar
        """
        curso_id, dia_semana, hora_inicio, hora_fin = self.obtener_informacion_formulario_registro()

        lista_idx_cursos = [cur[0] for cur in self.detalles_cursos]
        idx_curso = lista_idx_cursos.index(curso_id)
        curso_nombre = self.lista_cursos[idx_curso]

        if (str(curso_nombre)==str(self.curso_sel)) and (str(dia_semana) == str(self.dia_sel)) and (str(hora_inicio) == str(self.hora_inicio_sel)) and (str(hora_fin) == str(self.hora_fin_sel)):
            # Se regresa y no se hace ningún cambio
            self.cancelar_registro()
            return
        
        # Utilizar el controlador de horario para actualizar los datos de dicho horario
        self.parent.controlador_horario.actualizar_horario_por_id(id_horario=self.iid_sel,curso_id=curso_id,dia_semana=dia_semana,hora_inicio=hora_inicio,hora_fin=hora_fin)

        nuevo_horario, nombre_curso = self.parent.controlador_horario.obtener_horario_por_id(self.iid_sel)
        
        # Actualizar los valores del estudiante en la tabla
        self.parent.frame_tabla_horarios.tabla_horarios.item(
            self.iid_sel,
            values=(
                nuevo_horario.id_horario,
                nombre_curso,
                nuevo_horario.dia_semana,
                nuevo_horario.hora_inicio,
                nuevo_horario.hora_fin
            )
        )

        # Mostrar un mensaje de confirmación
        msg_registro_exitoso("Horario")
        self.actualizar_estado_ventana_al_cerrar()


    def cancelar_registro(self):
        """
            Muestra un mensaje de alerta, y se cierra la ventana
        """
        msg_sin_cambios()
        self.actualizar_estado_ventana_al_cerrar()

    def actualizar_estado_ventana_al_cerrar(self):
        """
            Se usa con ambas ventanas, guardar y actualizar
        """
        if self.tipo == 1:
            # Ventana de crear horario
            self.parent.ventana_nuevo_horario_esta_abierta = False
            self.destroy()
        if self.tipo == 2:
            # Ventana de crear horario
            self.parent.ventana_actualizacion_esta_abierta = False
            self.destroy()
