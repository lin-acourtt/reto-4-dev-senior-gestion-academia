import customtkinter as ctk
from tkinter import messagebox
from config.appearance import centrar_ventana
from controllers.horario_controller import HorarioController
from controllers.curso_controller import CursoController

class VentanaRegistrarHorario(ctk.CTkToplevel):
    def __init__(self, parent, db=None):
        super().__init__()
        self.parent = parent
        self.db = db
        self.controlador_horario = HorarioController(self.db)
        self.controlador_curso = CursoController(self.db)
        
        # Obtener el curso seleccionado
        seleccion = self.parent.frame_tabla_cursos.tabla_cursos.selection()
        if not seleccion:
            messagebox.showerror("Error", "Debe seleccionar un curso primero")
            self.parent.ventana_registrar_horario_esta_abierta = False
            self.destroy()
            return
            
        # Obtener el ID del curso seleccionado (está en la primera columna)
        item = self.parent.frame_tabla_cursos.tabla_cursos.item(seleccion[0])
        valores = item['values']
        if not valores:
            messagebox.showerror("Error", "No se pudo obtener la información del curso")
            self.parent.ventana_registrar_horario_esta_abierta = False
            self.destroy()
            return
            
        self.curso_seleccionado_id = valores[0]  # El ID está en la primera columna
        
        # Configurar la ventana
        self.title("Registrar Horario de Curso")
        self.geometry("500x400")
        centrar_ventana(self)
        self.resizable(False, False)
        
        # Frame principal
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            self.frame_principal,
            text="Registrar Horario de Curso",
            font=("Helvetica", 24, "bold")
        ).pack(pady=20)
        
        # Campos del formulario
        self.crear_campos_formulario()
        
        # Botones
        self.crear_botones()
        
        # Cargar información del curso seleccionado
        self.cargar_curso_seleccionado()
        
    def crear_campos_formulario(self):
        # Frame para los campos
        frame_campos = ctk.CTkFrame(self.frame_principal)
        frame_campos.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Mostrar curso seleccionado (solo lectura)
        ctk.CTkLabel(frame_campos, text="Curso seleccionado:").pack(pady=(10,5))
        self.label_curso = ctk.CTkLabel(frame_campos, text="", font=("Helvetica", 14))
        self.label_curso.pack(pady=(0,10))
        
        # Selección de día
        ctk.CTkLabel(frame_campos, text="Día de la semana:").pack(pady=(10,5))
        self.dia = ctk.CTkComboBox(
            frame_campos,
            width=400,
            values=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        )
        self.dia.pack(pady=(0,10))
        
        # Hora de inicio
        ctk.CTkLabel(frame_campos, text="Hora de inicio (HH:MM):").pack(pady=(10,5))
        self.hora_inicio = ctk.CTkEntry(frame_campos, width=400, placeholder_text="Ejemplo: 09:00")
        self.hora_inicio.pack(pady=(0,10))
        
        # Hora de fin
        ctk.CTkLabel(frame_campos, text="Hora de fin (HH:MM):").pack(pady=(10,5))
        self.hora_fin = ctk.CTkEntry(frame_campos, width=400, placeholder_text="Ejemplo: 11:00")
        self.hora_fin.pack(pady=(0,10))

    def crear_botones(self):
        """Crea los botones de la ventana"""
        frame_botones = ctk.CTkFrame(self.frame_principal)
        frame_botones.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(
            frame_botones,
            text="Registrar Horario",
            command=self.registrar_horario,
            width=200,
            height=40,
            corner_radius=10
        ).pack(side="left", padx=10, expand=True)
        
        ctk.CTkButton(
            frame_botones,
            text="Cancelar",
            command=self.cancelar_registro,
            width=200,
            height=40,
            corner_radius=10,
            fg_color="#FF5555",
            hover_color="#FF3333"
        ).pack(side="right", padx=10, expand=True)
        
    def cargar_curso_seleccionado(self):
        """Carga la información del curso seleccionado"""
        try:
            print(f"Intentando cargar curso con ID: {self.curso_seleccionado_id}")
            curso = self.controlador_curso.obtener_curso_por_id(self.curso_seleccionado_id)
            print(f"Resultado de obtener_curso_por_id: {curso}")
            
            if curso:
                texto_curso = f"ID: {curso.id_curso} - {curso.nombre}"
                print(f"Configurando label con texto: {texto_curso}")
                self.label_curso.configure(text=texto_curso)
            else:
                raise ValueError(f"No se encontró el curso con ID {self.curso_seleccionado_id}")
        except Exception as e:
            print(f"Error al cargar el curso: {str(e)}")
            messagebox.showerror("Error", f"Error al cargar el curso: {str(e)}")
            self.parent.ventana_registrar_horario_esta_abierta = False
            self.destroy()
            
    def registrar_horario(self):
        """Registra el horario en la base de datos"""
        try:
            # Obtener y validar datos
            dia = self.dia.get()
            hora_inicio = self.hora_inicio.get().strip()
            hora_fin = self.hora_fin.get().strip()
            
            # Validar campos requeridos
            if not dia:
                messagebox.showwarning("Advertencia", "Debe seleccionar un día")
                return
                
            if not hora_inicio or not hora_fin:
                messagebox.showwarning("Advertencia", "Debe ingresar hora de inicio y fin")
                return
                
            # Validar formato de horas
            if not self.validar_hora(hora_inicio) or not self.validar_hora(hora_fin):
                messagebox.showwarning("Advertencia", "El formato de hora debe ser HH:MM (ejemplo: 09:00)")
                return
                
            # Registrar el horario
            self.controlador_horario.registrar_horario(
                curso_id=self.curso_seleccionado_id,
                dia_semana=dia,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin
            )
            
            messagebox.showinfo("Éxito", "Horario registrado exitosamente")
            
            # Actualizar la tabla de cursos en la ventana principal
            cursos = self.parent.obtener_lista_cursos()
            self.parent.frame_tabla_cursos.imprimir_informacion_en_tabla(cursos)
            
            # Cerrar la ventana
            self.parent.ventana_registrar_horario_esta_abierta = False
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar horario: {str(e)}")
            
    def cancelar_registro(self):
        """Cierra la ventana sin guardar cambios"""
        self.parent.ventana_registrar_horario_esta_abierta = False
        self.destroy()
        
    def validar_hora(self, hora_str):
        """Valida que el formato de hora sea correcto (HH:MM)"""
        try:
            if not hora_str or ":" not in hora_str:
                return False
            horas, minutos = map(int, hora_str.split(":"))
            return 0 <= horas <= 23 and 0 <= minutos <= 59
        except:
            return False 