import customtkinter as ctk
from tkinter import ttk
from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
# from CTkTable import * 

class FrameTablaMatriculas(CTkFrame):
    def __init__(self, master):
        """
            Al crear este frame, se debe especificar el parent como la ventana del menú principal 
        """
        super().__init__(master)

        # Creación de la tabla de matriculas
        self.crear_tabla_matriculas() # -> Resultado, creación de self.tabla_matriculas
        self.tabla_matriculas.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nswe")

        # Construir un scrollbar vertical
        self.verscrlbar = ttk.Scrollbar(self, orient ="vertical", command = self.tabla_matriculas.yview)
        self.verscrlbar.grid(row=0,column=1, padx=10, pady=(10, 10),sticky="nesw") #nesw
        
        # Configurar el treeview para el comando yscroll
        self.tabla_matriculas.configure(yscrollcommand = self.verscrlbar.set)

        self.grid_columnconfigure(0,weight=20)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)

        # Cambiar el estado de los botones inactivos al seleccionar una fila
        self.tabla_matriculas.bind("<<TreeviewSelect>>", lambda event:self.master.frame_footer.actualizar_estado_de_botones())
        

    def crear_tabla_matriculas(self):
        """
            Método para generar un componente TreeView para la impresión de la información de las matriculas.
        """
        # Crear el Treeviw, las columnas y escoger mostrar los headers
        self.tabla_matriculas = ttk.Treeview(
            self,
            columns = ("ID", "Estudiante","Curso", "Fecha"),
            show="headings"
        )
        ttk.Style(self)
        # Asignar nombre a los headers
        self.tabla_matriculas.heading("ID", text="ID Matrícula")
        self.tabla_matriculas.heading("Estudiante", text="Estudiante")
        self.tabla_matriculas.heading("Curso", text="Curso")
        self.tabla_matriculas.heading("Fecha", text="Fecha de matrícula")

        # Configurar columnas
        self.tabla_matriculas.column("ID", width=50, anchor="center")
        #self.tabla_matriculas.column("Curso", width=150)
        #self.tabla_matriculas.column("Día", width=80, anchor="center")
        #self.tabla_matriculas.column("Hora de inicio", width=120)
        #self.tabla_matriculas.column("Hora de fin", width=200)

        # Obtener la información que se pondrá en la tabla
        matriculas, nombre_estudiantes, nombre_cursos = self.master.obtener_lista_matriculas()

        self.imprimir_informacion_en_tabla(matriculas, nombre_estudiantes, nombre_cursos)
    
    def imprimir_informacion_en_tabla(self, matriculas, nombre_estudiantes, nombre_cursos):
        """
            Método que recibe una lista de matriculas (objetos), e imprime sus atributos en el TreeView
            - matriculas: list[matricula]
            - nombre_estudiantes: El nombre de los estudiantes
            - nombre_cursos: El nombre de los cursos
        """
        # Limpiar tabla
        for item in self.tabla_matriculas.get_children():
            self.tabla_matriculas.delete(item)

        # Llenar el Treeview con esta información
        for mat,est,cur in zip(matriculas,nombre_estudiantes,nombre_cursos):
            try:
                self.tabla_matriculas.insert(
                    "","end",
                    iid=mat.id_matricula,
                    values = (
                        mat.id_matricula,
                        est,
                        cur,
                        mat.fecha_matricula,
                    )
                )
            except:
                # se usa para reimprimir la tabla, si un ID ya existe, se sigue con el próximo item
                continue

        """for i in range(20):
            self.tabla_matriculas.insert(
                "","end",
                iid = i+30,
                values = (
                    f'test{i+30}',
                    f'test{i+30}',
                    f'test{i+30}',
                    f'test{i+30}'
                )
            )"""