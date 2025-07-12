import customtkinter as ctk
from tkinter import ttk
from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
# from CTkTable import * 

class FrameTablaProfesores(CTkFrame):
    def __init__(self, master):
        """
            Al crear este frame, se debe especificar el parent como la ventana del menú principal de profesores
        """
        super().__init__(master)

        # Creación de la tabla de profesores
        self.crear_tabla_profesores() # -> Resultado, creación de self.tabla_profesores
        #self.tabla_profesores.pack(fill="x", padx=10, pady=10)
        #self.tabla_profesores.pack(expand=True, fill="both", padx=10, pady=10)
        self.tabla_profesores.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nswe")

        # Construir un scrollbar vertical
        self.verscrlbar = ttk.Scrollbar(self, orient ="vertical", command = self.tabla_profesores.yview)
        self.verscrlbar.grid(row=0,column=1, padx=10, pady=(10, 10),sticky="nesw") #nesw
        
        # Configurar el treeview para el comando yscroll
        self.tabla_profesores.configure(yscrollcommand = self.verscrlbar.set)

        self.grid_columnconfigure(0,weight=20)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)

        # Cambiar el estado de los botones inactivos al seleccionar una fila
        self.tabla_profesores.bind("<<TreeviewSelect>>", lambda event:self.master.frame_footer.actualizar_estado_de_botones())
        

    def crear_tabla_profesores(self):
        """
            Método para generar un componente TreeView para la impresión de la información de los profesores.
        """
        # Crear el Treeviw, las columnas y escoger mostrar los headers
        self.tabla_profesores = ttk.Treeview(
            self,
            columns=("ID", "Nombre", "Apellido", "Correo", "Telefono", "Especialidad"),
            show="headings"
        )
        ttk.Style(self)
        # Asignar nombre a los headers
        self.tabla_profesores.heading("ID", text="ID Docente")
        self.tabla_profesores.heading("Nombre", text="Nombre")
        self.tabla_profesores.heading("Apellido", text="Apellido")
        self.tabla_profesores.heading("Correo", text="Correo")
        self.tabla_profesores.heading("Telefono", text="Teléfono")
        self.tabla_profesores.heading("Especialidad", text="Especialidad")
        
        # Asignar ancho de columna
        self.tabla_profesores.column("ID",width=50)
        self.tabla_profesores.column("Nombre", width=100)
        self.tabla_profesores.column("Apellido", width=100)
        self.tabla_profesores.column("Correo", width=150)
        self.tabla_profesores.column("Telefono", width=100)
        self.tabla_profesores.column("Especialidad", width=100)
        
        # Obtener la información que se pondrá en la tabla
        profesores = self.master.obtener_lista_profesores()

        self.imprimir_informacion_en_tabla(profesores)
    
    def imprimir_informacion_en_tabla(self, profesores):
        """
            Método que recibe una lista de profesores (objetos), e imprime sus atributos en el TreeView
            - profesores: list[Profesor]
        """
        # Llenar el Treeview con esta información
        for prof in profesores:
            try:
                self.tabla_profesores.insert(
                    "","end",
                    iid=prof.id_profesor,
                    values = (
                        prof.id_profesor,
                        prof.nombre,
                        prof.apellido,
                        prof.correo,
                        prof.telefono,
                        prof.especialidad
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