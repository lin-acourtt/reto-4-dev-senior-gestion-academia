import customtkinter as ctk
from tkinter import ttk
from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
# from CTkTable import * 

class FrameTablaEstudiantes(CTkFrame):
    def __init__(self, master):
        """
            Al crear este frame, se debe especificar el parent como la ventana del menú principal 
        """
        super().__init__(master)

        # Creación de la tabla de estudiantes
        self.crear_tabla_estudiantes() # -> Resultado, creación de self.tabla_estudiantes
        #self.tabla_estudiantes.pack(fill="x", padx=10, pady=10)
        #self.tabla_estudiantes.pack(expand=True, fill="both", padx=10, pady=10)
        self.tabla_estudiantes.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nswe")

        # Construir un scrollbar vertical
        self.verscrlbar = ttk.Scrollbar(self, orient ="vertical", command = self.tabla_estudiantes.yview)
        self.verscrlbar.grid(row=0,column=1, padx=10, pady=(10, 10),sticky="nesw") #nesw
        
        # Configurar el treeview para el comando yscroll
        self.tabla_estudiantes.configure(yscrollcommand = self.verscrlbar.set)

        self.grid_columnconfigure(0,weight=20)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)

        # Cambiar el estado de los botones inactivos al seleccionar una fila
        self.tabla_estudiantes.bind("<<TreeviewSelect>>", lambda event:self.master.frame_footer.actualizar_estado_de_botones())
        

    def crear_tabla_estudiantes(self):
        """
            Método para generar un componente TreeView para la impresión de la información de los estudiantes.
        """
        # Crear el Treeviw, las columnas y escoger mostrar los headers
        self.tabla_estudiantes = ttk.Treeview(
            self,
            columns=("ID","Nombre","Apellido","Correo","Teléfono"),
            show="headings"
        )
        ttk.Style(self)
        # Asignar nombre a los headers
        self.tabla_estudiantes.heading("ID", text="ID")
        self.tabla_estudiantes.heading("Nombre", text="Nombre")
        self.tabla_estudiantes.heading("Apellido", text="Apellido")
        self.tabla_estudiantes.heading("Correo", text="Correo")
        self.tabla_estudiantes.heading("Teléfono", text="Teléfono")

        # Asignar ancho de columna
        self.tabla_estudiantes.column("ID",width=50)
        # Obtener la información que se pondrá en la tabla
        estudiantes = self.master.obtener_lista_estudiantes()

        self.imprimir_informacion_en_tabla(estudiantes)
    
    def imprimir_informacion_en_tabla(self, estudiantes):
        """
            Método que recibe una lista de estudiantes (objetos), e imprime sus atributos en el TreeView
            - estudiantes: list[Estudiante]
        """
        # Llenar el Treeview con esta información
        for est in estudiantes:
            try:
                self.tabla_estudiantes.insert(
                    "","end",
                    iid=est.id_estudiante,
                    values = (
                        est.id_estudiante,
                        est.nombre,
                        est.apellido,
                        est.correo,
                        est.telefono
                    )
                )
            except:
                # se usa para reimprimir la tabla, si un ID ya existe, se sigue con el próximo item
                continue

        """for i in range(20):
            self.tabla_estudiantes.insert(
                "","end",
                iid = i+30,
                values = (
                    f'test{i+30}',
                    f'test{i+30}',
                    f'test{i+30}',
                    f'test{i+30}'
                )
            )"""