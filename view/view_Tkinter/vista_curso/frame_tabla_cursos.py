import customtkinter as ctk
from tkinter import ttk
from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
# from CTkTable import * 

class FrameTablaCursos(CTkFrame):
    def __init__(self, master):
        """
            Al crear este frame, se debe especificar el parent como la ventana del menú principal 
        """
        super().__init__(master)

        # Creación de la tabla de cursos
        self.crear_tabla_cursos() # -> Resultado, creación de self.tabla_cursos
        #self.tabla_cursos.pack(fill="x", padx=10, pady=10)
        #self.tabla_cursos.pack(expand=True, fill="both", padx=10, pady=10)
        self.tabla_cursos.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nswe")

        # Construir un scrollbar vertical
        self.verscrlbar = ttk.Scrollbar(self, orient ="vertical", command = self.tabla_cursos.yview)
        self.verscrlbar.grid(row=0,column=1, padx=10, pady=(10, 10),sticky="nesw") #nesw
        
        # Configurar el treeview para el comando yscroll
        self.tabla_cursos.configure(yscrollcommand = self.verscrlbar.set)

        self.grid_columnconfigure(0,weight=20)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)

        # Cambiar el estado de los botones inactivos al seleccionar una fila
        self.tabla_cursos.bind("<<TreeviewSelect>>", lambda event:self.master.frame_footer.actualizar_estado_de_botones())
        

    def crear_tabla_cursos(self):
        """
            Método para generar un componente TreeView para la impresión de la información de los cursos.
        """
        # Crear el Treeviw, las columnas y escoger mostrar los headers
        self.tabla_cursos = ttk.Treeview(
            self,
            columns = ("ID", "Nombre", "Profesor", "Estudiantes", "Horarios", "Descripción", "Duración"),
            show="headings"
        )
        ttk.Style(self)
        # Asignar nombre a los headers
        self.tabla_cursos.heading("ID", text="ID")
        self.tabla_cursos.heading("Nombre", text="Nombre del Curso")
        self.tabla_cursos.heading("Profesor", text="Profesor")
        self.tabla_cursos.heading("Estudiantes", text="Estudiantes")
        self.tabla_cursos.heading("Horarios", text="Horarios")
        self.tabla_cursos.heading("Descripción", text="Descripción")
        self.tabla_cursos.heading("Duración", text="Duración (hrs)")

        # Configurar columnas
        self.tabla_cursos.column("ID", width=50, anchor="center")
        self.tabla_cursos.column("Nombre", width=150)
        self.tabla_cursos.column("Profesor", width=150)
        self.tabla_cursos.column("Estudiantes", width=80, anchor="center")
        self.tabla_cursos.column("Horarios", width=120)
        self.tabla_cursos.column("Descripción", width=200)
        self.tabla_cursos.column("Duración", width=100, anchor="center")

        # Obtener la información que se pondrá en la tabla
        cursos = self.master.obtener_lista_cursos()

        self.imprimir_informacion_en_tabla(cursos)
    
    def imprimir_informacion_en_tabla(self, cursos):
        """
            Método que recibe una lista de cursos (objetos), e imprime sus atributos en el TreeView
            - cursos: list[curso]
        """
        # Limpiar la tabla antes de insertar nuevos datos
        for item in self.tabla_cursos.get_children():
            self.tabla_cursos.delete(item)

        # Llenar el Treeview con esta información
        for cur in cursos:
            try:
                self.tabla_cursos.insert(
                    "","end",
                    iid=cur.id_curso,
                    values = (
                        cur.id_curso,
                        cur.nombre,
                        cur.profesor,
                        cur.num_estudiantes,
                        cur.horarios,
                        cur.descripcion,
                        cur.duracion_horas
                    )
                )
            except:
                # se usa para reimprimir la tabla, si un ID ya existe, se sigue con el próximo item
                continue

        """for i in range(20):
            self.tabla_cursos.insert(
                "","end",
                iid = i+30,
                values = (
                    f'test{i+30}',
                    f'test{i+30}',
                    f'test{i+30}',
                    f'test{i+30}'
                )
            )"""