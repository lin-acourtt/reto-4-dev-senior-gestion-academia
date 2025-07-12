import customtkinter as ctk
from tkinter import ttk
from customtkinter import CTkScrollableFrame
from customtkinter import CTkFrame
# from CTkTable import * 

class FrameTablaResultados(CTkFrame):
    def __init__(self, master):
        """
            Al crear este frame, se debe especificar el parent como la ventana "VentanaTablaResultados" 
        """
        super().__init__(master)

        # Creación de la tabla de resultados
        self.crear_tabla_resultados() # -> Resultado, creación de self.tabla_resultados
        self.tabla_resultados.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nswe")

        # La información que se pondrá en la tabla viene del parent
        resultados = self.master.resultados

        self.imprimir_informacion_en_tabla(resultados) # -> Resultado: LLenar tabla con la información

        # Construir un scrollbar vertical
        self.verscrlbar = ttk.Scrollbar(self, orient ="vertical", command = self.tabla_resultados.yview)
        self.verscrlbar.grid(row=0,column=1, padx=10, pady=(10, 10),sticky="nesw") #nesw
        
        # Construir un scrollbar horizontal
        self.horscrlbar = ttk.Scrollbar(self, orient ="horizontal", command = self.tabla_resultados.xview)
        self.tabla_resultados.configure(xscrollcommand=self.horscrlbar.set)
        self.horscrlbar.grid(row=1,column=0, columnspan=2, padx=10, pady=(10, 10),sticky="nesw") #nesw
        
        # Configurar el treeview para el comando yscroll
        self.tabla_resultados.configure(yscrollcommand = self.verscrlbar.set)

        self.grid_columnconfigure(0,weight=20)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)


    def crear_tabla_resultados(self):
        """
            Método para generar un componente TreeView para la impresión de la información de los estudiantes.
        """
        # Crear el Treeviw, las columnas y escoger mostrar los headers
        self.tabla_resultados = ttk.Treeview(
            self,
            columns=(self.master.columnas),
            show="headings",
            height=15
        )
        ttk.Style(self)
        # Asignar nombre a los headers
        for a,b,c in zip(self.master.columnas, self.master.nombre_columnas, self.master.ancho_columnas):
            self.tabla_resultados.heading(a, text=b)
            self.tabla_resultados.column(a,width=c)
        
        # Asignar ancho de columna
        #self.tabla_estudiantes.column("ID",width=50)
        
        
    def imprimir_informacion_en_tabla(self, resultados):
        """
            Método que recibe una matriz de elementos que se van a imprimri en la tabla.
            - El número de columnas debe ser el mismo de las columnas especificadas para el TreeView
            - El número de filas es variable.
        """

        # Limpiar tabla
        for item in self.tabla_resultados.get_children():
            self.tabla_resultados.delete(item)

        # Llenar el Treeview con esta información
        for r in resultados:
            try:
                self.tabla_resultados.insert(
                    "","end",
                    iid=r[0],
                    values = (r)
                )
            except:
                # se usa para reimprimir la tabla, si un ID ya existe, se sigue con el próximo item
                continue
    
