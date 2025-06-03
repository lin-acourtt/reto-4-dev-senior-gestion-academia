import customtkinter as ctk
from view.view_Tkinter.vista_msgbox.msgbox_library import msg_sin_cambios, msg_registro_exitoso, msg_error_campos_vacios, msg_entrada_duplicada, msg_error_integrity, msg_error_inesperado, msg_error_cargar_datos
from mysql.connector import IntegrityError
from config.appearance import centrar_ventana

class VentanaCrearCurso(ctk.CTk):
    """
        Inicializa la ventana para crear nuevos cursos.
    """
    def __init__(self, parent=None, tipo: int=1):
        """
            Se debe definir el parent, que sería la ventana de "MenuCurso" y el tipo, que tiene 2 opciones
            1: Crear Curso
            2: Modificar curso
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
        self.label_nombre = ctk.CTkLabel(self, text="Nombre:")
        self.label_nombre.grid(row = row_number, column= 0, padx=(10,10), pady=(5,5))
        self.entry_nombre = ctk.CTkEntry(self)
        self.entry_nombre.grid(row = row_number, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        
        # Descripción del curso
        row_number += 1
        self.label_descripcion = ctk.CTkLabel(self, text="Descripción:")
        self.label_descripcion.grid(row = row_number, column= 0, padx=(10,10), pady=(5,5))
        self.entry_descripcion = ctk.CTkEntry(self)
        self.entry_descripcion.grid(row = row_number, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        
        # Duración del curso
        row_number += 1
        self.label_duracion = ctk.CTkLabel(self, text="Duración (horas):")
        self.label_duracion.grid(row = row_number, column= 0, padx=(10,10), pady=(5,5))
        self.entry_duracion = ctk.CTkEntry(self)
        self.entry_duracion.grid(row = row_number, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        
        # Profesor
        row_number += 1
        self.label_profesor = ctk.CTkLabel(self, text="Profesor:")
        self.label_profesor.grid(row = row_number, column= 0, padx=(10,10), pady=(5,5))
        self.cobox_profesor = ctk.CTkComboBox(self)
        self.cobox_profesor.grid(row = row_number, column= 1, padx=(10,30), pady=(5,5), sticky='ew')
        self.cobox_profesor.configure(state='readonly')
        
        row_number += 1
        # Botón de guardado    
        self.btn_guardar = ctk.CTkButton(self)
        self.btn_guardar.grid(row = row_number, column = 0, padx=(0,20), pady=15)
        # Botón de cancelar    
        self.btn_cancelar = ctk.CTkButton(self, text="Cancelar", command=self.cancelar_registro)
        self.btn_cancelar.grid(row = row_number, column = 1, padx=(0,20),pady=15)

        # self.detalles_profesor
        # contiene los items por separado
        # self.lista_profesores
        # contiene los items concatenados
        self.obtener_lista_id_nombres_profesor() # Obtiene 3 listas de profesores, ver doc.
        

        if self.tipo == 1:
            # Si es una ventana de creación de nuevo curso, se configuran los siguientes parámetros
            self.title("Crear nuevo curso")
            self.label_titulo.configure(text="Crear nuevo curso")
            self.entry_nombre.configure(placeholder_text="Nombre")
            self.entry_descripcion.configure(placeholder_text="Descripción")
            self.entry_duracion.configure(placeholder_text="Duración")
            self.cargar_profesores_en_cobox()
            # Botón de guardado    
            self.btn_guardar.configure(text="Guardar", command=self.guardar_registro)
        elif self.tipo == 2:
            # Si es una ventana de actualización de nuevo curso, se configuran los siguientes parámetros
            self.title("Editar curso")
            self.label_titulo.configure(text="Actualización de curso")

            self.strvar_nombre = ctk.StringVar(self,"")
            self.strvar_descripcion = ctk.StringVar(self,"")
            self.strvar_duracion = ctk.StringVar(self,"")
            #self.strvar_profesor = ctk.StringVar(self,"")

            # Actualizar los campos de las entries, con la información del estudiante seleccionado
            self.actualizar_informacion_campos()

            self.entry_nombre.configure(textvariable=self.strvar_nombre)
            self.entry_descripcion.configure(textvariable=self.strvar_descripcion)
            self.entry_duracion.configure(textvariable=self.strvar_duracion)

            self.cargar_profesores_en_cobox()
            # Botón de guardado    
            self.btn_guardar.configure(text="Actualizar", command=self.actualizar_registro)
            self.btn_guardar.grid(row = row_number, column = 0, padx=(0,20), pady=15)
        
        self.protocol("WM_DELETE_WINDOW", self.cancelar_registro)

    def guardar_registro(self):
        """
            Se usa para: Crear curso
            Actualiza la base de datos (tabla cursos), con la información del curso que se escribió en el formulario.
        """
        
        try: 
            # Obtener los datos en los elementos de "Entry"
            nombre = self.entry_nombre.get().strip()
            descripcion = self.entry_descripcion.get().strip()
            duracion = self.entry_duracion.get().strip()
            profesor = self.cobox_profesor.get().strip()

            index_profesor = 0
            for string_profesor in self.lista_profesores:
                if profesor == string_profesor:
                    break
                index_profesor +=1

            profesor_id = self.detalles_profesor[index_profesor][0]

            #print(profesor_id)
            # Validar campos
            if not all([nombre, descripcion, duracion, profesor_id]):
                msg_error_campos_vacios()
                return
            
            # Utilizar el controlador de curso para registrar un nuevo curso
            self.parent.controlador_curso.registrar_curso(nombre=nombre, descripcion=descripcion, duracion_horas=duracion, id_profesor=profesor_id)
            
            # Inserta el nuevo curso en la lista de cursos
            # (Se re-imprime toda la lista)
            cursos = self.parent.obtener_lista_cursos()
            self.parent.frame_tabla_cursos.imprimir_informacion_en_tabla(cursos)
            
            # Mostrar un mensaje de registro exitoso
            msg_registro_exitoso("curso")

            # Cierra la ventana y cambia el estado de esta ventana a cerrado
            self.actualizar_estado_ventana_al_cerrar()
        
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                msg_entrada_duplicada("curso")
            else:
                msg_error_integrity("curso",str(e))
        except Exception as e:
            msg_error_inesperado(str(e))

    def obtener_lista_id_nombres_profesor(self):
        """
            Obtiene 3 listas de profesores y los guarda como atributos:
            - self.profesores: lista de objetos
            - self.detalles_profesor: lista con IDs y nombres [[id1,nombre1,apellido1],[id2,nombre2,apellido2],etc]
            - self.lista_profesores: lista con IDs y nombres concatenados ['ID: 1 - Nombre1 Apellido1','ID: 2 - Nombre2 Apellido2',etc]
        """
        try:
            self.profesores, self.detalles_profesor, self.lista_profesores = self.parent.obtener_listas_profesores()
            
            if not self.profesores:
                raise Exception
        except Exception as e:
            msg_error_cargar_datos("profesor",str(e))

    def cargar_profesores_en_cobox(self):
        """
            Se usa con ambas ventanas, guardar y actualizar
            Carga la lista de profesores en el combobox que se le proporcione
        """
        self.cobox_profesor.configure(values=self.lista_profesores)
        if self.tipo == 1:
            # Ventana de creación de curso
            self.cobox_profesor.set("test")
            self.cobox_profesor.set(self.lista_profesores[0])
        if self.tipo == 2:
            # Ventana de actualización de curso

            # El detalle del profesor seleccionado, ya viene de la función self.actualizar_informacion_campos()
            self.cobox_profesor.set(self.profesor_concat_sel)

    
    def actualizar_informacion_campos(self):
        """
            Se usa con ventana: editar curso
            Actualizar los campos de las entries, con la información del curso seleccionado
        """
        self.obtener_valores_de_seleccion()
        # Resultado, actualización de los atributos
        # - self.iid_sel
        # - self.nombre_sel
        # - self.apellido_sel
        # - self.correo_sel
        # - self.telefono_sel

        self.actualizar_strvars()
        # Resultado, actualización de los atributos
        # - self.strvar_nombre
        # - self.strvar_apellido
        # - self.strvar_correo
        # - self.strvar_tel

    def obtener_valores_de_seleccion(self):
        """
            Se usa con ventana: editar curso
            Obtiene los valores de la tabla según la selección que se haga
        """
        self.iid_sel = self.parent.frame_tabla_cursos.tabla_cursos.selection()[0]
        self.nombre_sel = self.parent.frame_tabla_cursos.tabla_cursos.item(self.iid_sel)['values'][1]
        self.descripcion_sel = self.parent.frame_tabla_cursos.tabla_cursos.item(self.iid_sel)['values'][5]
        self.duracion_sel = self.parent.frame_tabla_cursos.tabla_cursos.item(self.iid_sel)['values'][6]
        self.profesor_concat_sel = self.parent.frame_tabla_cursos.tabla_cursos.item(self.iid_sel)['values'][2]
    
    def actualizar_strvars(self):
        """
            Se usa con ventana: editar curso
            Actualiza los valores de los StringVars que llenan los campos de texto con la información del estudiante.
        """
        self.strvar_nombre.set(self.nombre_sel)
        self.strvar_descripcion.set(self.descripcion_sel)
        self.strvar_duracion.set(self.duracion_sel)        
        self.cobox_profesor.set(self.profesor_concat_sel)
    
    def actualizar_registro(self):
        """
            Se usa con la ventana: editar
        """
        try:
            # Obtener los datos en los elementos de "Entry"
            nombre = self.entry_nombre.get().strip()
            descripcion = self.entry_descripcion.get().strip()
            duracion = self.entry_duracion.get().strip()
            profesor_concat = self.cobox_profesor.get().strip()

            # Validar campos
            if not all([nombre, descripcion, duracion, profesor_concat]):
                msg_error_campos_vacios()
                return
            
            if (str(nombre)==str(self.nombre_sel)) and (str(descripcion) == str(self.descripcion_sel)) and (str(duracion) == str(self.duracion_sel)) and (str(profesor_concat) == str(self.profesor_concat_sel)):
                # Se regresa y no se hace ningún cambio
                self.cancelar_registro()
                return

            # Antes de proceder a guardar, se busca el ID del profesor, ya que se obtuvo fue la concatenación de sus datos
            index_profesor = 0
            for string_profesor in self.lista_profesores:
                if profesor_concat == string_profesor:
                    break
                index_profesor +=1

            profesor_id = self.detalles_profesor[index_profesor][0]

            # Utilizar el controlador de curso para actualizar los datos de dicho curso
            self.parent.controlador_curso.actualizar_curso(self.iid_sel,nombre,profesor_id,descripcion,duracion)

            nuevo_curso = self.parent.controlador_curso.obtener_curso_por_id(self.iid_sel)
            
            # Actualizar los valores del estudiante en la tabla
            self.parent.frame_tabla_cursos.tabla_cursos.item(
                self.iid_sel,
                values=(
                    nuevo_curso.id_curso,
                    nuevo_curso.nombre,
                    nuevo_curso.profesor,
                    nuevo_curso.num_estudiantes,
                    nuevo_curso.horarios,
                    nuevo_curso.descripcion,
                    nuevo_curso.duracion_horas
                )
            )

            # Mostrar un mensaje de confirmación
            msg_registro_exitoso("Curso")
            self.actualizar_estado_ventana_al_cerrar()
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                msg_entrada_duplicada("estudiante")
            else:
                msg_error_integrity("estudiante",str(e))
        except Exception as e:
            msg_error_inesperado(str(e))

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
            # Ventana de crear curso
            self.parent.ventana_nuevo_curso_esta_abierta = False
            self.destroy()
        if self.tipo == 2:
            # Ventana de crear curso
            self.parent.ventana_actualizacion_esta_abierta = False
            self.destroy()
