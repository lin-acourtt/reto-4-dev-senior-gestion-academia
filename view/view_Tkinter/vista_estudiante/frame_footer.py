import customtkinter as ctk
from customtkinter import CTkFrame
from tkinter.constants import DISABLED, NORMAL 

# Menú Estudiantes
class FrameFooter(CTkFrame):
    def __init__(self, master):
        """
        Al crear este frame, se debe especificar el parent, que debería ser 'VentanaMenuEstudiante',
        """
        super().__init__(master)

        # Se utilizará para cambiar el estado de los botones
        self.botones_activos = False

        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=1)
        self.columnconfigure(4,weight=1)

        self.btn_registrar_estudiante = ctk.CTkButton(self, text="➕ Registrar", command= self.master.abrir_ventana_registro)
        self.btn_actualizar_estudiante = ctk.CTkButton(self, text="✏️ Actualizar",state=DISABLED, command= self.master.abrir_ventana_actualizacion)
        self.btn_eliminar_estudiante = ctk.CTkButton(self, text="🗑️ Eliminar",state=DISABLED, command= self.master.abrir_ventana_borrar)
        self.btn_buscar_estudiante = ctk.CTkButton(self, text="🔍 Buscar",command=self.master.abrir_ventana_buscar)
        self.btn_ver_cursos_estudiante = ctk.CTkButton(self, text="🧑‍🎓 Consultar cursos",state=DISABLED, command=self.master.abrir_consultar_cursos2)

        self.btn_registrar_estudiante.grid(row=0,column=0, padx=5, pady=5)
        self.btn_actualizar_estudiante.grid(row=0,column=1, padx=5, pady=5)
        self.btn_eliminar_estudiante.grid(row=0,column=2, padx=5, pady=5)
        self.btn_buscar_estudiante.grid(row=0,column=3, padx=5, pady=5)
        self.btn_ver_cursos_estudiante.grid(row=0,column=4, padx=5, pady=5)

    def actualizar_estado_de_botones(self):
        """Actualiza el estado de los botones según si hay un elemento seleccionado en la tabla"""
        # Verificar si hay una selección en la tabla
        seleccion = self.master.frame_tabla_estudiantes.tabla_estudiantes.selection()
        
        if seleccion:
            # Si hay selección, activar los botones
            self.btn_actualizar_estudiante.configure(state=NORMAL)
            self.btn_eliminar_estudiante.configure(state=NORMAL)
            self.btn_ver_cursos_estudiante.configure(state=NORMAL)
        else:
            # Si no hay selección, desactivar los botones
            self.btn_actualizar_estudiante.configure(state=DISABLED)
            self.btn_eliminar_estudiante.configure(state=DISABLED)
            self.btn_ver_cursos_estudiante.configure(state=DISABLED)
