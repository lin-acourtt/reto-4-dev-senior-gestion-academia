import customtkinter as ctk
from customtkinter import CTkFrame
from tkinter.constants import DISABLED, NORMAL 

# Menú Cursos
class FrameFooter(CTkFrame):
    def __init__(self, master):
        """
        Al crear este frame, se debe especificar el parent, que debería ser 'VentanaMenuEstudiante',
        """
        super().__init__(master)

        # Se utilizará para cambiar el estado de los botones
        self.botones_activos = False

        self.btn_nuevo_curso = ctk.CTkButton(self, text="➕ Nuevo Curso", command=self.master.abrir_ventana_nuevo_curso)
        self.btn_actualizar_curso = ctk.CTkButton(self, text="✏️ Editar", state=DISABLED, command=self.master.abrir_ventana_actualizacion)
        self.btn_eliminar_curso = ctk.CTkButton(self, text="🗑️ Eliminar", state=DISABLED, command=self.master.abrir_ventana_borrar)
        self.btn_buscar_curso = ctk.CTkButton(self, text="🔍 Buscar", command=self.master.abrir_ventana_buscar)
        self.btn_registrar_horario = ctk.CTkButton(self, text="⏰ Registrar Horario", state=DISABLED, command=self.master.abrir_ventana_registrar_horario)
        self.btn_consultar_horarios = ctk.CTkButton(self, text="📅 Consultar Horarios", state=DISABLED, command=self.master.abrir_consultar_horarios2)
        self.btn_estudiantes_inscritos = ctk.CTkButton(self, text="👥 Estudiantes inscritos", state=DISABLED, command=self.master.abrir_consultar_estudiantes_curso2)
        
        #self.btn_ver_matriculas_estudiante = ctk.CTkButton(self, text="🗎 Ver matrículas",state=DISABLED)
        #self.btn_ver_horarios_estudiante = ctk.CTkButton(self, text="⏱️ Ver horarios",state=DISABLED)

        self.btn_nuevo_curso.grid(row=0, column=0, padx=5, pady=5)
        self.btn_actualizar_curso.grid(row=0, column=1, padx=5, pady=5)
        self.btn_eliminar_curso.grid(row=0, column=2, padx=5, pady=5)
        self.btn_buscar_curso.grid(row=0, column=3, padx=5, pady=5)
        self.btn_registrar_horario.grid(row=1, column=0, padx=5, pady=5)
        self.btn_consultar_horarios.grid(row=1, column=1, padx=5, pady=5)
        self.btn_estudiantes_inscritos.grid(row=1, column=2, padx=5, pady=5)
        #self.btn_ver_matriculas_estudiante.grid(row=0,column=4, padx=5, pady=5)
        #self.btn_ver_horarios_estudiante.grid(row=0,column=5, padx=5, pady=5)
        for i in range(5):
            self.columnconfigure(i,weight=1)
        
        for i in range(1):
            self.rowconfigure(i,weight=1)
        # Configurar el evento de selección en la tabla
        self.master.frame_tabla_cursos.tabla_cursos.bind('<<TreeviewSelect>>', lambda e: self.actualizar_estado_de_botones())

    def actualizar_estado_de_botones(self):
        """Actualiza el estado de los botones según si hay un elemento seleccionado en la tabla"""
        # Verificar si hay una selección en la tabla
        seleccion = self.master.frame_tabla_cursos.tabla_cursos.selection()
        
        if seleccion:
            # Si hay selección, activar los botones
            self.btn_actualizar_curso.configure(state=NORMAL)
            self.btn_eliminar_curso.configure(state=NORMAL)
            self.btn_registrar_horario.configure(state=NORMAL)
            self.btn_estudiantes_inscritos.configure(state=NORMAL)
            self.btn_consultar_horarios.configure(state=NORMAL)
        else:
            # Si no hay selección, desactivar los botones
            self.btn_actualizar_curso.configure(state=DISABLED)
            self.btn_eliminar_curso.configure(state=DISABLED)
            self.btn_registrar_horario.configure(state=DISABLED)
            self.btn_estudiantes_inscritos.configure(state=DISABLED)
            self.btn_consultar_horarios.configure(state=DISABLED)
