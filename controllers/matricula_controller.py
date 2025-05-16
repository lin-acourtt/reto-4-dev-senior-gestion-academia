
#from config.database import Database
from models.Matricula import Matricula

class MatriculaController:

    # The controller will require a DB object
    def __init__(self, db):
        self.db = db

    def registrar_matricula(self,estudiante_id,curso_id,fecha_matricula):
        
        sql = """
            INSERT INTO matriculas (estudiante_id,curso_id,fecha_matricula)
            VALUES (%s,%s,%s);
        """
        params=(estudiante_id,curso_id,fecha_matricula)
        self.db.execute_query(sql,params)
    
    def listar_matriculas(self):
        # sql = "SELECT * FROM matriculas"
        # sql = "SELECT id_matricula, nombre, descripcion, duracion_horas, profesor_id FROM matriculas"
        sql = """
            SELECT matriculas.id_matricula, matriculas.estudiante_id, matriculas.curso_id, matriculas.fecha_matricula,
            CONCAT(estudiantes.nombre,' ',estudiantes.apellido) AS nombre_estudiante,
            cursos.nombre AS nombre_curso
            FROM matriculas 
            JOIN estudiantes on (matriculas.estudiante_id = estudiantes.id_estudiante)
            JOIN cursos on (matriculas.curso_id = cursos.id_curso);
        """
        resultados = self.db.execute_select(sql)
        nombre_estudiantes = [detalles_matricula[4] for detalles_matricula in resultados] # Es nombre del estudiante de esta matrícula
        nombre_cursos = [detalles_matricula[5] for detalles_matricula in resultados] # Es nombre del curso de este matricula
        return [Matricula(*resultado[0:4]) for resultado in resultados], nombre_estudiantes, nombre_cursos
    
    def obtener_matricula_por_id(self,id_matricula):
        """
            Retorna el objeto del matricula con el ID especificado
        """
        sql = """
            SELECT matriculas.id_matricula, matriculas.estudiante_id, matriculas.curso_id, matriculas.fecha_matricula,
            CONCAT(estudiantes.nombre,' ',estudiantes.apellido) AS nombre_estudiante,
            cursos.nombre AS nombre_curso
            FROM matriculas 
            JOIN estudiantes on (matriculas.estudiante_id = estudiantes.id_estudiante)
            JOIN cursos on (matriculas.curso_id = cursos.id_curso)
            WHERE id_matricula = %s
        """
        params = (id_matricula,)
        resultado = self.db.execute_select(sql, params)
        nombre_estudiante = resultado[0][4]
        nombre_curso = resultado[0][5]
        return Matricula(*resultado[0][0:4]) if resultado else None, nombre_estudiante, nombre_curso

    def actualizar_matricula_por_id(self,id_matricula,estudiante_id,curso_id,fecha_matricula):
        """
            Actualiza todos los parámetros de un matricula por su ID
        """
        sql = """
            UPDATE matriculas SET estudiante_id=%s, curso_id=%s, fecha_matricula=%s
            WHERE id_matricula= %s
        """
        params = (estudiante_id,curso_id,fecha_matricula,id_matricula)
        resultado = self.db.execute_select(sql, params)

    def eliminar_matricula_por_id(self, id_matricula):
        """
            Elimina un matricula dando un ID
        """
        sql = """
            DELETE FROM matriculas WHERE id_matricula= %s
        """
        params = (id_matricula,)
        resultado = self.db.execute_query(sql, params)

