import customtkinter as ctk
from view.view_Tkinter.vista_msgbox.msgbox_library import msg_sin_cambios, msg_registro_exitoso, msg_error_campos_vacios, msg_entrada_duplicada, msg_error_integrity, msg_error_inesperado, msg_error_cargar_datos, msg_conflicto_horas
from mysql.connector import IntegrityError
from config.appearance import centrar_ventana

from tkcalendar import DateEntry
from datetime import datetime

class VentanaCrearMatricula(ctk.CTk):
    """
        Inicializa la ventana para crear nuevos matriculas.
    """

    def __init__(self, parent=None, tipo: int=1):
        """
            Se debe definir el parent, que sería la ventana de "MenuMatricula" y el tipo, que tiene 2 opciones
            1: Crear Matricula
            2: Modificar matricula
        """
        super().__init__()
        self.parent = parent
        self.tipo = tipo
        
        centrar_ventana(self,0.35,0.3)
        self.resizable(False, False)
        
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        row_number = 0

        # Título en la ventana
        self.label_titulo = ctk.CTkLabel(self,font=("Helvetica", 14, "bold"))
        self.label_titulo.grid(row = 0, column = 0, columnspan=2,pady=(10,10))

        # Nombre del estudiante
        row_number += 1
        self.label_estudiante = ctk.CTkLabel(self, text="Estudiante:")
        self.label_estudiante.grid(row = row_number, column= 0, padx=(10,10), pady=(5,5))
        self.cobox_estudiante = ctk.CTkComboBox(self)
        self.cobox_estudiante.grid(row = row_number, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        self.cobox_estudiante.configure(state='readonly')
        
        # Nombre del curso
        row_number += 1
        self.label_curso = ctk.CTkLabel(self, text="Curso:")
        self.label_curso.grid(row = row_number, column= 0, padx=(10,10), pady=(5,5))
        self.cobox_curso = ctk.CTkComboBox(self)
        self.cobox_curso.grid(row = row_number, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        self.cobox_curso.configure(state='readonly')
        
        # Fecha de matricula
        # Nombre del curso
        row_number += 1
        self.label_fecha = ctk.CTkLabel(self, text="Fecha de matrícula:")
        self.label_fecha.grid(row = row_number, column= 0, padx=(10,10), pady=(5,5))
        self.entry_fecha = DateEntry(self,date_pattern='yyyy-MM-dd')
        self.entry_fecha.grid(row = row_number, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        self.cobox_curso.configure(state='readonly')

        row_number += 1
        # Botón de guardado    
        self.btn_guardar = ctk.CTkButton(self)
        self.btn_guardar.grid(row = row_number, column = 0, padx=(0,20), pady=15)
        # Botón de cancelar    
        self.btn_cancelar = ctk.CTkButton(self, text="Cancelar", command=self.cancelar_registro)
        self.btn_cancelar.grid(row = row_number, column = 1, padx=(0,20),pady=15)

        # self.detalles_estudiantes
        # contiene los items por separado
        # self.lista_estudiantes
        # contiene los items concatenados
        self.obtener_lista_id_estudiantes() # Obtiene 3 listas de estudiantes, ver doc.
        # self.detalles_cursos
        # contiene los items por separado
        # self.lista_cursos
        # contiene los items concatenados
        self.obtener_lista_id_cursos() # Obtiene 3 listas de cursos, ver doc.
        
        if self.tipo == 1:
            # Si es una ventana de creación de nuevo matricula, se configuran los siguientes parámetros
            self.title("Crear nueva matricula")
            self.label_titulo.configure(text="Crear nueva matricula")
            self.cargar_estudiantes_en_cobox()
            self.cargar_cursos_en_cobox()
            # Botón de guardado    
            self.btn_guardar.configure(text="Guardar", command=self.guardar_registro)
        elif self.tipo == 2:
            # Si es una ventana de actualización de nuevo matricula, se configuran los siguientes parámetros
            self.title("Editar matricula")
            self.label_titulo.configure(text="Actualización de matricula")

            self.actualizar_informacion_campos()

            # Actualizar los campos de las entries, con la información del matricula seleccionado
            self.cargar_estudiantes_en_cobox()
            self.cargar_cursos_en_cobox()

            # Botón de guardado    
            self.btn_guardar.configure(text="Actualizar", command=self.actualizar_registro)
            self.btn_guardar.grid(row = row_number, column = 0, padx=(0,20), pady=15)
        
        self.protocol("WM_DELETE_WINDOW", self.cancelar_registro)

    def obtener_lista_id_estudiantes(self):
        """
            Obtiene 3 listas de estudiantes y los guarda como atributos:
            - self.estudiantes: lista de objetos
            - self.detalles_estudiantes: lista con IDs y nombres [[id1,nombre1,apellido1],[id2,nombre2,apellido2],etc]
            - self.lista_estudiantes: lista con IDs y nombres concatenados ['ID: 1 - Nombre1 Apellido1','ID: 2 - Nombre1 Apellido2',etc]
        """
        try:
            self.estudiantes, self.detalles_estudiantes, self.lista_estudiantes = self.parent.obtener_listas_estudiantes()

            if not self.estudiantes:
                raise Exception
        except Exception as e:
            msg_error_cargar_datos("estudiante",str(e))

    def obtener_lista_id_cursos(self):
        """
            Obtiene 3 listas de cursos y los guarda como atributos:
            - self.cursos: lista de objetos
            - self.detalles_cursos: lista con IDs y nombres [[id1,curso1],[id2,curso2],etc]
            - self.lista_cursos: lista con IDs y nombres concatenados ['ID: 1 - Curso1','ID: 2 - Curso2',etc]
        """
        try:
            self.cursos, self.detalles_cursos, self.lista_cursos = self.parent.obtener_listas_cursos()
            
            if not self.cursos:
                raise Exception
        except Exception as e:
            msg_error_cargar_datos("curso",str(e))

    def cargar_estudiantes_en_cobox(self):
        """
            Se usa con ambas ventanas, guardar y actualizar
            Carga la lista de cursos en el combobox pertinente
        """
        self.cobox_estudiante.configure(values=self.lista_estudiantes)
        if self.tipo == 1:
            # Ventana de creación de matricula
            self.cobox_estudiante.set(self.lista_estudiantes[0])
        if self.tipo == 2:
            # Ventana de actualización de matricula

            # El detalle del estudiante seleccionado, ya viene de la función self.actualizar_informacion_campos()
            self.cobox_estudiante.set(self.estudiante_sel)
    

    def cargar_cursos_en_cobox(self):
        """
            Se usa con ambas ventanas, guardar y actualizar
            Carga la lista de cursos en el combobox pertinente
        """
        self.cobox_curso.configure(values=self.lista_cursos)
        if self.tipo == 1:
            # Ventana de creación de matricula
            self.cobox_curso.set(self.lista_cursos[0])
        if self.tipo == 2:
            # Ventana de actualización de matricula

            # El detalle del profesor seleccionado, ya viene de la función self.actualizar_informacion_campos()
            self.cobox_curso.set(self.curso_sel)
    
    def actualizar_informacion_campos(self):
        """
            Se usa con ventana: editar matricula
            Actualizar los campos de las entries, con la información de la matricula seleccionado
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
            Se usa con ventana: editar matricula
            Obtiene los valores de la tabla según la selección que se haga
        """
        self.iid_sel = self.parent.frame_tabla_matriculas.tabla_matriculas.selection()[0]
        self.estudiante_sel = self.parent.frame_tabla_matriculas.tabla_matriculas.item(self.iid_sel)['values'][1]
        self.curso_sel = self.parent.frame_tabla_matriculas.tabla_matriculas.item(self.iid_sel)['values'][2]
        self.fecha_matricula_str_sel = self.parent.frame_tabla_matriculas.tabla_matriculas.item(self.iid_sel)['values'][3]

        # La fecha str se convierte a date(), como ya viene de la tabla se asume que siempre tiene buen formato
        self.fecha_matricula_sel = datetime.strptime(self.fecha_matricula_str_sel, "%Y-%m-%d")
        self.fecha_matricula_sel = datetime.date(self.fecha_matricula_sel)

    def actualizar_strvars(self):
        """
            Se usa con ventana: editar matricula
            Actualiza los valores de los StringVars que llenan los campos de texto con la información del estudiante.
        """
        self.cobox_estudiante.set(self.estudiante_sel)
        self.cobox_curso.set(self.curso_sel)
        self.entry_fecha.set_date(self.fecha_matricula_sel)

    def obtener_informacion_formulario_registro(self):
        """
            Se usa para obtener la información del formulario ya sea de registro o de actualización
        """
        try: 
            # Obtener los datos en los elementos de "Entry"
            estudiante_nombre = self.cobox_estudiante.get().strip()
            curso_nombre = self.cobox_curso.get().strip()
            fecha_matricula = self.entry_fecha.get_date()

            # Se busca cuál es el ID del estudiante que corresponde al nombre seleccionado
            index_est = 0
            if str(estudiante_nombre[0:2])=='ID':# La comparación va a ser con self.lista_estudiantes
                for string_est in self.lista_estudiantes:
                    if estudiante_nombre == string_est:
                        break
                    index_est +=1
            else:
                # La comparación va a ser con self.detalles_estudiantes
                for string_est in self.detalles_estudiantes:
                    if estudiante_nombre == f"{string_est[1]} {string_est[2]}":
                        break
                    index_est +=1
                

            estudiante_id = self.detalles_estudiantes[index_est][0]
            nombre_estudiante = f'{self.detalles_estudiantes[index_est][1]} {self.detalles_estudiantes[index_est][2]}'

            # Se busca cuál es el ID del curso que corresponde al nombre seleccionado
            index_curso = 0
            if str(curso_nombre[0:2])=='ID':
                # La comparación va a ser con self.lista_cursos
                for string_curso in self.lista_cursos:
                    if curso_nombre == string_curso:
                        break
                    index_curso +=1
            else:
                # La comparación va a ser con self.detalles_cursos
                for string_curso in self.detalles_cursos:
                    if curso_nombre == f"{string_curso[1]}":
                        break
                    index_curso +=1

            curso_id = self.detalles_cursos[index_curso][0]
            nombre_curso = self.detalles_cursos[index_curso][1]

            #print(profesor_id)
            # Validar campos
            if not all([estudiante_id, curso_id, fecha_matricula]):
                msg_error_campos_vacios()
                return
            
            return estudiante_id, nombre_estudiante, curso_id, nombre_curso, fecha_matricula
        
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                msg_entrada_duplicada("matricula")
            else:
                msg_error_integrity("matricula",str(e))
        except Exception as e:
            msg_error_inesperado(str(e))
    
    def guardar_registro(self):
        
        """
            Se usa para: Crear matricula
            Actualiza la base de datos (tabla matriculas), con la información del matricula que se escribió en el formulario.
        """
        estudiante_id, nombre_estudiante, curso_id, nombre_curso, fecha_matricula = self.obtener_informacion_formulario_registro()

        # Utilizar el controlador de matricula para registrar un nuevo matricula
        self.parent.controlador_matricula.registrar_matricula(estudiante_id, curso_id, fecha_matricula)
        
        # Inserta el nuevo matricula en la lista de matriculas
        # (Se re-imprime toda la lista)
        matriculas, nombre_estudiantes, nombre_cursos = self.parent.obtener_lista_matriculas()
        self.parent.frame_tabla_matriculas.imprimir_informacion_en_tabla(matriculas, nombre_estudiantes, nombre_cursos)
        
        # Mostrar un mensaje de registro exitoso
        msg_registro_exitoso("matricula")

        # Cierra la ventana y cambia el estado de esta ventana a cerrado
        self.actualizar_estado_ventana_al_cerrar()
        

    def actualizar_registro(self):
        """
            Se usa con la ventana: editar
        """
        estudiante_id, estudiante_nombre, curso_id, curso_nombre, fecha_matricula = self.obtener_informacion_formulario_registro()

        # En este punto se comparan solo los nombres (sin el ID)
        if (str(estudiante_nombre)==str(self.estudiante_sel)) and (str(curso_nombre)==str(self.curso_sel)) and (str(fecha_matricula) == str(self.fecha_matricula_sel)):
            # Se regresa y no se hace ningún cambio
            self.cancelar_registro()
            return
        
        # Utilizar el controlador de matricula para actualizar los datos de dicho matricula
        self.parent.controlador_matricula.actualizar_matricula_por_id(id_matricula=self.iid_sel,estudiante_id=estudiante_id, curso_id=curso_id, fecha_matricula=fecha_matricula)

        nueva_matricula, nombre_estudiante, nombre_curso = self.parent.controlador_matricula.obtener_matricula_por_id(self.iid_sel)
        
        # Actualizar los valores del estudiante en la tabla
        self.parent.frame_tabla_matriculas.tabla_matriculas.item(
            self.iid_sel,
            values=(
                nueva_matricula.id_matricula,
                nombre_estudiante,
                nombre_curso,
                nueva_matricula.fecha_matricula
            )
        )

        # Mostrar un mensaje de confirmación
        msg_registro_exitoso("Matricula")
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
            # Ventana de crear matricula
            self.parent.ventana_nueva_matricula_esta_abierta = False
            self.destroy()
        if self.tipo == 2:
            # Ventana de crear matricula
            self.parent.ventana_actualizacion_esta_abierta = False
            self.destroy()
