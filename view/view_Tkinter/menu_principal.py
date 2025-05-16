import customtkinter as ctk
from PIL import Image, ImageTk
import os
# from view.viewTkinter.viewEstudiante.menuEstudiante import MenuEstudiante
# from view.viewTkinter.viewDocenteFull.menuDocenteFull import MenuDocenteFull
from controllers.estudiante_controller import EstudianteController
from controllers.profesor_controller import ProfesorController
from controllers.curso_controller import CursoController

#Crear la clase principal de la ventana la cual se encargar de recibir a las demas ventanas
class MenuPrincipal:
    def __init__(self, db=None, tema_actual="System"):
        self.db = db    
        self.root = ctk.CTk()
        self.root.title("Sistema de Gestión Académica")
        
        # Configurar el tema de la ventana
        ctk.set_appearance_mode(tema_actual)
        self.tema_actual = tema_actual

        # Obtener el ancho y alto de la pantalla
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()

        # Asignar tamaño de la ventana (más grande para el nuevo diseño)
        ancho_ventana = int(ancho_pantalla * 0.8)
        alto_ventana = int(alto_pantalla * 0.8)
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}")

        # Configuración de restricciones de la ventana
        self.root.resizable(True, True)

        # Coordenadas centradas
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        # Crear el frame principal
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)

        # Frame superior para el título y el botón de tema
        self.frame_superior = ctk.CTkFrame(self.frame_principal)
        self.frame_superior.pack(fill="x", padx=10, pady=10)

        # Título con estilo moderno
        self.titulo = ctk.CTkLabel(
            self.frame_superior, 
            text="Sistema de Gestión Académica",
            font=("Helvetica", 24, "bold")
        )
        self.titulo.pack(side="left", padx=20)

        # Botón de tema con icono
        self.btn_cambiar_tema = ctk.CTkButton(
            self.frame_superior,
            text="🌓 Cambiar Tema",
            command=self.cambiar_tema,
            width=120
        )
        self.btn_cambiar_tema.pack(side="right", padx=20)

        # Frame para el contenido principal (grid de 2x3)
        self.frame_contenido = ctk.CTkFrame(self.frame_principal)
        self.frame_contenido.pack(fill="both", expand=True, padx=10, pady=10)

        # Crear los botones principales con iconos y descripciones
        botones = [
            ("👥 Estudiantes", "Gestionar estudiantes", self.abrir_ventana_estudiantes),
            ("👨‍🏫 Docentes", "Gestionar docentes", self.abrir_ventana_docentes),
            ("📚 Cursos", "Gestionar cursos", self.abrir_ventana_cursos),
            ("⏰ Horarios", "Gestionar horarios", self.abrir_ventana_horarios),
            ("📝 Matrículas", "Gestionar matrículas", self.abrir_ventana_matriculas),
            ("📊 Estadísticas", "Ver estadísticas", self.mostrar_estadisticas)
        ]

        # Crear grid de botones
        for i, (texto, descripcion, comando) in enumerate(botones):
            frame_boton = ctk.CTkFrame(self.frame_contenido)
            frame_boton.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            
            btn = ctk.CTkButton(
                frame_boton,
                text=texto,
                command=comando,
                height=100,
                font=("Helvetica", 16, "bold")
            )
            btn.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Agregar descripción
            label_desc = ctk.CTkLabel(
                frame_boton,
                text=descripcion,
                font=("Helvetica", 12)
            )
            label_desc.pack(pady=(0, 5))

        # Configurar el grid
        self.frame_contenido.grid_columnconfigure(0, weight=1)
        self.frame_contenido.grid_columnconfigure(1, weight=1)
        self.frame_contenido.grid_columnconfigure(2, weight=1)
        self.frame_contenido.grid_rowconfigure(0, weight=1)
        self.frame_contenido.grid_rowconfigure(1, weight=1)

        # Cargar estadísticas iniciales
        self.cargar_estadisticas()

    def cargar_estadisticas(self):
        try:
            # Crear controladores
            estudiante_controller = EstudianteController(self.db)
            docente_controller = ProfesorController(self.db)
            curso_controller = CursoController(self.db)

            # Obtener estadísticas
            total_estudiantes = len(estudiante_controller.listar_estudiantes())
            total_docentes = len(docente_controller.listar_docentes())
            total_cursos = len(curso_controller.listar_cursos())

            # Actualizar etiquetas de estadísticas si existen
            if hasattr(self, 'label_estadisticas'):
                self.label_estadisticas.configure(
                    text=f"Estadísticas:\n"
                         f"Estudiantes: {total_estudiantes}\n"
                         f"Docentes: {total_docentes}\n"
                         f"Cursos: {total_cursos}"
                )
        except Exception as e:
            print(f"Error al cargar estadísticas: {e}")

    def mostrar_estadisticas(self):
        # Crear ventana de estadísticas
        ventana_stats = ctk.CTkToplevel(self.root)
        ventana_stats.title("Estadísticas del Sistema")
        ventana_stats.geometry("400x300")
        ventana_stats.resizable(False, False)
        
        # Configurar el tema
        ctk.set_appearance_mode(self.tema_actual)
        
        # Frame para las estadísticas
        frame_stats = ctk.CTkFrame(ventana_stats)
        frame_stats.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            frame_stats,
            text="Estadísticas del Sistema",
            font=("Helvetica", 20, "bold")
        )
        titulo.pack(pady=10)
        
        # Cargar y mostrar estadísticas
        try:
            estudiante_controller = EstudianteController(self.db)
            docente_controller = ProfesorController(self.db)
            curso_controller = CursoController(self.db)
            
            total_estudiantes = len(estudiante_controller.listar_estudiantes())
            total_docentes = len(docente_controller.listar_docentes())
            total_cursos = len(curso_controller.listar_cursos())
            
            # Mostrar estadísticas con iconos
            stats_text = f"""
            👥 Total de Estudiantes: {total_estudiantes}
            👨‍🏫 Total de Docentes: {total_docentes}
            📚 Total de Cursos: {total_cursos}
            """
            
            label_stats = ctk.CTkLabel(
                frame_stats,
                text=stats_text,
                font=("Helvetica", 16),
                justify="left"
            )
            label_stats.pack(pady=20)
            
        except Exception as e:
            label_error = ctk.CTkLabel(
                frame_stats,
                text=f"Error al cargar estadísticas: {str(e)}",
                text_color="red"
            )
            label_error.pack(pady=20)
        
        # Botón para cerrar
        btn_cerrar = ctk.CTkButton(
            frame_stats,
            text="Cerrar",
            command=ventana_stats.destroy
        )
        btn_cerrar.pack(pady=10)

    def abrir_ventana_estudiantes(self):
        self.root.destroy()
        # menu_estudiante = MenuEstudiante(db=self.db, tema_actual=self.tema_actual)
        # menu_estudiante.root.mainloop()

    def abrir_ventana_docentes(self):
        self.root.destroy()
        # menu_docente = MenuDocenteFull(db=self.db, tema_actual=self.tema_actual)
        # menu_docente.root.mainloop()

    def abrir_ventana_cursos(self):
        # TODO: Implementar ventana de cursos
        pass

    def abrir_ventana_horarios(self):
        # TODO: Implementar ventana de horarios
        pass

    def abrir_ventana_matriculas(self):
        # TODO: Implementar ventana de matrículas
        pass

    def cambiar_tema(self):
        if self.tema_actual == "Light":
            ctk.set_appearance_mode("Dark")
            self.tema_actual = "Dark"
            self.btn_cambiar_tema.configure(text="☀️ Cambiar Tema")
        else:
            ctk.set_appearance_mode("Light")
            self.tema_actual = "Light"
            self.btn_cambiar_tema.configure(text="🌓 Cambiar Tema")
