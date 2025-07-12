import customtkinter as ctk

# from tkinter import ttk

from config.database import Database
from config.appearance import centrar_ventana

from .frame_header import FrameHeader
from .frame_tabla_resultados import FrameTablaResultados
from .frame_footer import FrameFooter

class VentanaTablaResultados(ctk.CTkToplevel):
    """
        Este es un molde de ventana exclusivamente usado para mostrar resultados que necesiten imprimirse en una tabla. 
        Input:
        - parent: Ventana desde donde se genera la búsqueda
        - elemento_tabla: Elementos que se van a mostrar en la tabla, todo en minúscula. (todo en minúscula)
        - elemento_owner: Elemento que es el owner de lo que se va a mostrar en la tabla. (todo en minúscula)
        - nombre_elemento_owner: Nombre del elemento owner. (Viene con su propia capitalización)
        - columnas: Lista con las columnas que debe tener el TreeView
        - nombre_columnas: Lista con el nombre de las columnas del TreeView
        - ancho_columnas: Lista con el ancho de las columnas
        - resultados: Es una matriz donde el número de columnas es el mismo de columnas especificadas para el TreeView, las filas son variables dependiendo de los resultados
        - proporcion1: Porcentaje del total del ancho de la pantalla
        - proporcion2: Porcentaje del total del ato de la ventana
    """

    def __init__(self, 
                 parent,
                 elemento_tabla: str,
                 elemento_owner: str,
                 nombre_elemento_owner: str,
                 columnas: list,
                 nombre_columnas: list,
                 ancho_columnas: list,
                 resultados,
                 proporcion1,
                 proporcion2):
        """
            Constructor, requiere de:
            - db: Base de datos, objeto tipo Database
        """
        super().__init__()
        self.parent = parent
        self.elemento_tabla = elemento_tabla
        self.elemento_owner = elemento_owner
        self.nombre_elemento_owner = nombre_elemento_owner
        
        # Crear la versión plural de los títulos de los elementos
        if self.elemento_tabla == "profesor":
            self.elemento_tabla_pl = f"{self.elemento_tabla}es"# Versión plural
        else:
            self.elemento_tabla_pl = f"{self.elemento_tabla}s"# Versión plural

        if self.elemento_owner == "profesor":
            self.elemento_owner_pl = f"{self.elemento_owner}es"# Versión plural
        else:
            self.elemento_owner_pl = f"{self.elemento_owner}s"# Versión plural

        # Se define el tamaño de la ventana y se centra
        self.proporcion1 = proporcion1
        self.proporcion2 = proporcion2
        centrar_ventana(
            self,
            self.proporcion1,
            self.proporcion2)
        self.resizable(True, True)

        # Título de la ventana
        self.title(f"{self.elemento_tabla_pl.capitalize()} del {self.elemento_owner.capitalize()}")

        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        self.rowconfigure(2,weight=1)
        self.columnconfigure(0,weight=1)
        # Frame Header - Contiene el título 
        self.frame_header = FrameHeader(self)
        self.frame_header.pack(fill="x", padx=20, pady=10)
        #self.frame_header.grid(row=0,column=0, padx=(10,10), sticky='we')

        # Elementos del Treeview
        self.columnas = columnas
        self.nombre_columnas = nombre_columnas
        self.ancho_columnas = ancho_columnas
        self.resultados = resultados

        self.frame_tabla_resultados = FrameTablaResultados(self)
        self.frame_tabla_resultados.pack(fill='both', expand=True, padx=20)
        #self.frame_tabla_resultados.pack(fill="both", padx=20, pady=10)
        #self.frame_tabla_resultados.grid(row=1,column=0, padx=(10,10), sticky='we')

        # Crear el frame para el Footer - Contiene los botones de acción
        self.frame_footer = FrameFooter(self)
        self.frame_footer.pack(padx=20, pady=10)
        #self.frame_footer.grid(row=2,column=0, padx=(10,10), sticky='we')

        self.protocol("WM_DELETE_WINDOW", parent.cerrar_resultados)


    def actualizar_titulos(self, nombre_elemento_owner: str):
        # Actualiza los títulos si se selecciona un nuevo estudiante
        self.nombre_elemento_owner = nombre_elemento_owner
        
        # Actualizar título
        self.frame_header.label_titulo.configure(text=f"{self.elemento_tabla_pl.capitalize()} de {self.elemento_owner}: {self.nombre_elemento_owner}")
