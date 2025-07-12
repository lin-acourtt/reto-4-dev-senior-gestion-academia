import customtkinter as ctk
from customtkinter import CTkFrame
from tkinter.constants import DISABLED, NORMAL 

# Menú Horarios
class FrameFooter(CTkFrame):
    def __init__(self, master):
        """
        Al crear este frame, se debe especificar el parent, que debería ser 'VentanaMenuHorario',
        """
        super().__init__(master)

        # Se utilizará para cambiar el estado de los botones
        self.botones_activos = False

        self.btn_nuevo_horario = ctk.CTkButton(self, text="➕ Nuevo Horario", command= self.master.abrir_ventana_nuevo_horario)
        self.btn_actualizar_horario = ctk.CTkButton(self, text="✏️ Editar",state=DISABLED, command= self.master.abrir_ventana_actualizacion)
        self.btn_eliminar_horario = ctk.CTkButton(self, text="🗑️ Eliminar",state=DISABLED, command= self.master.abrir_ventana_borrar)
        self.btn_buscar_horario = ctk.CTkButton(self, text="🔍 Buscar",command=self.master.abrir_ventana_buscar)
        #self.btn_ver_matriculas_estudiante = ctk.CTkButton(self, text="🗎 Ver matrículas",state=DISABLED)
        #self.btn_ver_horarios_estudiante = ctk.CTkButton(self, text="⏱️ Ver horarios",state=DISABLED)

        self.btn_nuevo_horario.grid(row=0,column=0, padx=5, pady=5)
        self.btn_actualizar_horario.grid(row=0,column=1, padx=5, pady=5)
        self.btn_eliminar_horario.grid(row=0,column=2, padx=5, pady=5)
        self.btn_buscar_horario.grid(row=0,column=3, padx=(5,10), pady=5)
        #self.btn_ver_matriculas_estudiante.grid(row=0,column=4, padx=5, pady=5)
        #self.btn_ver_horarios_estudiante.grid(row=0,column=5, padx=5, pady=5)
        
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=1)

    def actualizar_estado_de_botones(self):
        """Actualiza el estado de los botones a continuación cuando hay un elemento en la tabla seleccionado"""
        if self.botones_activos == False:
            # Cambiar el estado a activos
            self.botones_activos = True
            self.btn_actualizar_horario.configure(state = NORMAL)
            self.btn_eliminar_horario.configure(state = NORMAL)
            #self.btn_ver_matriculas_estudiante.configure(state = NORMAL)
            #self.btn_ver_horarios_estudiante.configure(state = NORMAL)
        else:
            return
