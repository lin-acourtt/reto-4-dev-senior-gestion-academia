from view.view_Tkinter.menu_principal import MenuPrincipal
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
        app = MenuPrincipal(db=db)
        # Iniciar el bucle principal de la aplicación
        app.root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
    finally:
        db.close()

# vídeo por 52:58