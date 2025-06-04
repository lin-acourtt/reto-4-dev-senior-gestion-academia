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

    def obtener_cursos_por_estudiante(self, estudiante_id):
        """
        Obtiene todos los cursos en los que está inscrito un estudiante específico.
        
        Args:
            estudiante_id (int): ID del estudiante del cual se quieren obtener los cursos
            
        Returns:
            list: Lista de diccionarios con la información de los cursos
        """
        try:
            query = """
                SELECT 
                    c.id_curso,
                    c.nombre as nombre_curso,
                    CONCAT(p.nombre, ' ', p.apellido) as profesor,
                    c.descripcion,
                    c.duracion_horas,
                    GROUP_CONCAT(
                        CONCAT(h.dia_semana, ' ', 
                        TIME_FORMAT(h.hora_inicio, '%H:%i'), '-', 
                        TIME_FORMAT(h.hora_fin, '%H:%i')
                    ) SEPARATOR ', ') as horarios
                FROM matriculas m
                JOIN cursos c ON m.curso_id = c.id_curso
                LEFT JOIN profesores p ON c.profesor_id = p.id_profesor
                LEFT JOIN horarios h ON c.id_curso = h.curso_id
                WHERE m.estudiante_id = %s
                GROUP BY c.id_curso, c.nombre, profesor, c.descripcion, c.duracion_horas
                ORDER BY c.nombre
            """
            resultados = self.db.execute_select(query, (estudiante_id,))
            
            cursos = []
            for row in resultados:
                curso = {
                    'id_curso': row[0],
                    'nombre': row[1],
                    'profesor': row[2] if row[2] else "Sin profesor asignado",
                    'descripcion': row[3] if row[3] else "Sin descripción",
                    'duracion_horas': row[4] if row[4] else "No especificada",
                    'horarios': row[5] if row[5] else "Sin horario asignado"
                }
                cursos.append(curso)
                
            return cursos
            
        except Exception as e:
            print(f"Error al obtener cursos del estudiante: {str(e)}")
            return []

