import customtkinter as ctk
from tkinter import ttk
from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
# from CTkTable import * 

class FrameTablaHorarios(CTkFrame):
    def __init__(self, master):
        """
            Al crear este frame, se debe especificar el parent como la ventana del menú principal 
        """
        super().__init__(master)

        # Creación de la tabla de horarios
        self.crear_tabla_horarios() # -> Resultado, creación de self.tabla_horarios
        self.tabla_horarios.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nswe")

        # Construir un scrollbar vertical
        self.verscrlbar = ttk.Scrollbar(self, orient ="vertical", command = self.tabla_horarios.yview)
        self.verscrlbar.grid(row=0,column=1, padx=10, pady=(10, 10),sticky="nesw") #nesw
        
        # Configurar el treeview para el comando yscroll
        self.tabla_horarios.configure(yscrollcommand = self.verscrlbar.set)

        self.grid_columnconfigure(0,weight=20)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)

        # Cambiar el estado de los botones inactivos al seleccionar una fila
        self.tabla_horarios.bind("<<TreeviewSelect>>", lambda event:self.master.frame_footer.actualizar_estado_de_botones())
        

    def crear_tabla_horarios(self):
        """
            Método para generar un componente TreeView para la impresión de la información de los horarios.
        """
        # Crear el Treeviw, las columnas y escoger mostrar los headers
        self.tabla_horarios = ttk.Treeview(
            self,
            columns = ("ID", "Curso", "Día", "Hora de inicio", "Hora de fin"),
            show="headings"
        )
        ttk.Style(self)
        # Asignar nombre a los headers
        self.tabla_horarios.heading("ID", text="ID")
        self.tabla_horarios.heading("Curso", text="Curso")
        self.tabla_horarios.heading("Día", text="Día")
        self.tabla_horarios.heading("Hora de inicio", text="Hora de inicio")
        self.tabla_horarios.heading("Hora de fin", text="Hora de fin")

        # Configurar columnas
        self.tabla_horarios.column("ID", width=50, anchor="center")
        #self.tabla_horarios.column("Curso", width=150)
        #self.tabla_horarios.column("Día", width=80, anchor="center")
        #self.tabla_horarios.column("Hora de inicio", width=120)
        #self.tabla_horarios.column("Hora de fin", width=200)

        # Obtener la información que se pondrá en la tabla
        horarios, cursos = self.master.obtener_lista_horarios()

        self.imprimir_informacion_en_tabla(horarios, cursos)
    
    def imprimir_informacion_en_tabla(self, horarios, cursos):
        """
            Método que recibe una lista de horarios (objetos), e imprime sus atributos en el TreeView
            - horarios: list[horario]
        """
        # Llenar el Treeview con esta información
        for hor,cur in zip(horarios,cursos):
            try:
                self.tabla_horarios.insert(
                    "","end",
                    iid=hor.id_horario,
                    values = (
                        hor.id_horario,
                        cur,
                        hor.dia_semana,
                        hor.hora_inicio,
                        hor.hora_fin,
                    )
                )
            except:
                # se usa para reimprimir la tabla, si un ID ya existe, se sigue con el próximo item
                continue

        """for i in range(20):
            self.tabla_horarios.insert(
                "","end",
                iid = i+30,
                values = (
                    f'test{i+30}',
                    f'test{i+30}',
                    f'test{i+30}',
                    f'test{i+30}'
                )
            )"""