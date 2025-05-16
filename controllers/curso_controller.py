
#from config.database import Database
from models.Curso import Curso

class CursoController:

    # The controller will require a DB object
    def __init__(self, db):
        self.db = db

    def registrar_curso(self,nombre,descripcion,duracion_horas,profesor_id):
        
        sql = """
            INSERT INTO cursos (nombre,descripcion,duracion_horas,profesor_id)
            VALUES (%s,%s,%s,%s);
        """
        params=(nombre,descripcion,duracion_horas,profesor_id)
        self.db.execute_query(sql,params)
    
    def listar_cursos(self):
        # sql = "SELECT * FROM cursos"
        # sql = "SELECT id_curso, nombre, descripcion, duracion_horas, profesor_id FROM cursos"
        sql = """
            SELECT cursos.id_curso, cursos.nombre, cursos.descripcion, cursos.duracion_horas, cursos.profesor_id, profesores.nombre, profesores.apellido FROM cursos 
            JOIN profesores on (cursos.profesor_id = profesores.id_profesor);
        """
        resultados = self.db.execute_select(sql)
        nombre_profesores = [f"{detalles_curso[5]} {detalles_curso[6]}" for detalles_curso in resultados] # Los nombres de los profesores se encuentran en la 5ta columna de resultados
        return [Curso(*resultado[0:5]) for resultado in resultados], nombre_profesores
    
    def obtener_curso_por_id(self,id_curso):
        """
            Retorna el objeto del curso con el ID especificado
        """
        sql = """
            SELECT cursos.id_curso, cursos.nombre, cursos.descripcion, cursos.duracion_horas, cursos.profesor_id, concat(profesores.nombre,' ',profesores.apellido) as nombre_profesor FROM cursos 
            JOIN profesores on (cursos.profesor_id = profesores.id_profesor)
            WHERE id_curso = %s
        """
        params = (id_curso,)
        resultado = self.db.execute_select(sql, params)
        nombre_profesor = resultado[0][5]
        return Curso(*resultado[0][0:5]) if resultado else None, nombre_profesor

    def actualizar_curso_por_id(self,id_curso,nombre,descripcion,duracion_horas,profesor_id):
        """
            Actualiza todos los parámetros de un curso por su ID
        """
        sql = """
            UPDATE cursos SET nombre=%s, descripcion=%s, duracion_horas=%s, profesor_id=%s 
            WHERE id_curso= %s
        """
        params = (nombre,descripcion,duracion_horas,profesor_id,id_curso)
        resultado = self.db.execute_select(sql, params)

    def eliminar_curso_por_id(self, id_curso):
        """
            Elimina un curso dando un ID
        """
        sql = """
            DELETE FROM cursos WHERE id_curso= %s
        """
        params = (id_curso,)
        resultado = self.db.execute_query(sql, params)

