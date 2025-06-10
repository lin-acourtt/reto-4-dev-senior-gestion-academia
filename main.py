from view.view_Tkinter.vista_principal.menu_principal import VentanaMenuPrincipal
# from view.menu_estudiantes import menu_estudiantes
# from view.menu_profesores import menu_profesores
# from view.menu_cursos import menu_cursos
# from view.menu_horarios import menu_horarios
# from view.menu_matriculas import menu_matriculas
from config.database import Database

if __name__ == "__main__":
    db = Database()
    try:
        # Crear la instancia del menú principal
        app = VentanaMenuPrincipal(db=db)
        # Iniciar el bucle principal de la aplicación
        app.iniciar_ventana()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
    finally:
        db.close()

# vídeo por 52:58  <<---  what? << creo que era de la clase xd