from view.menu_estudiantes import menu_estudiantes
from view.menu_profesores import menu_profesores
from view.menu_cursos import menu_cursos
from view.menu_horarios import menu_horarios
from view.menu_matriculas import menu_matriculas
from config.database import Database

if __name__ == "__main__":
    db = Database()
    try:
        # menu_estudiantes(db)
        # menu_profesores(db)
        # menu_cursos(db)
        # menu_horarios(db)
        menu_matriculas(db)
    finally:
        db.close()

# vídeo por 52:58