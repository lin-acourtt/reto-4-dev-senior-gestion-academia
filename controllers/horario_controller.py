#from config.database import Database
from models.Horario import Horario
from models.Curso import Curso

class HorarioController:
    """
        Controlador para realizar operaciones con la tabla de horarios. 
        - Métodos:
            - registrar_horario -> Registra un solo horario
            - listar_horarios -> Obtiene una lista de todos los horarios
            - obtener_horario_por_id -> Obtiene detalles de horario por su ID.
            - actualizar_horario_por_id -> Actualiza todos los atributos de un horario.
            - eliminar_horario_por_id -> Elimina un horario por su ID.
            - obtener_horarios_por_curso -> Obtiene los horarios asociados al ID de curso que se le especifique.
    """

    # The controller will require a DB object
    def __init__(self, db):
        self.db = db

    def registrar_horario(self,curso_id,dia_semana,hora_inicio,hora_fin):
        
        sql = """
            INSERT INTO Horarios (curso_id,dia_semana,hora_inicio,hora_fin)
            VALUES (%s,%s,%s,%s);
        """
        params=(curso_id,dia_semana,hora_inicio,hora_fin)
        self.db.execute_query(sql,params)
    
    def listar_horarios(self):
        # sql = "SELECT * FROM horarios"
        # sql = "SELECT id_horario, nombre, descripcion, duracion_horas, profesor_id FROM horarios"
        sql = """
            SELECT Horarios.id_horario, Horarios.curso_id, Horarios.dia_semana, Horarios.hora_inicio, Horarios.hora_fin, 
            Cursos.nombre FROM Horarios 
            JOIN Cursos on (Horarios.curso_id = Cursos.id_curso);
        """
        resultados = self.db.execute_select(sql)
        nombre_cursos = [detalles_horario[5] for detalles_horario in resultados] # Es nombre del curso de este horario
        return [Horario(*resultado[0:5]) for resultado in resultados], nombre_cursos
    
    def obtener_horario_por_id(self,id_horario):
        """
            Retorna el objeto del horario con el ID especificado
        """
        sql = """
            SELECT Horarios.id_horario, Horarios.curso_id, Horarios.dia_semana, Horarios.hora_inicio, Horarios.hora_fin, 
            Cursos.nombre FROM Horarios 
            JOIN Cursos on (Horarios.curso_id = Cursos.id_curso)
            WHERE id_horario = %s
        """
        params = (id_horario,)
        resultado = self.db.execute_select(sql, params)
        nombre_curso = resultado[0][5]
        return Horario(*resultado[0][0:5]) if resultado else None, nombre_curso

    def actualizar_horario_por_id(self,id_horario,curso_id,dia_semana,hora_inicio,hora_fin):
        """
            Actualiza todos los parámetros de un horario por su ID
        """
        sql = """
            UPDATE Horarios SET curso_id=%s, dia_semana=%s, hora_inicio=%s, hora_fin=%s 
            WHERE id_horario= %s
        """
        params = (curso_id,dia_semana,hora_inicio,hora_fin,id_horario)
        resultado = self.db.execute_select(sql, params)

    def eliminar_horario_por_id(self, id_horario):
        """
            Elimina un horario dando un ID
        """
        sql = """
            DELETE FROM Horarios WHERE id_horario= %s
        """
        params = (id_horario,)
        resultado = self.db.execute_query(sql, params)

    def obtener_horarios_por_curso(self, curso_id):
        """
        Obtiene todos los horarios asignados a un curso específico.
        
        Args:
            curso_id (int): ID del curso del cual se quieren obtener los horarios
            
        Returns:
            list: Lista de objetos Horario con la información del curso asociado
        """
        try:
            sql = """
                SELECT h.id_horario, h.curso_id, h.dia_semana, h.hora_inicio, h.hora_fin,
                       c.nombre as nombre_curso, c.profesor_id, CONCAT(p.nombre,' ',p.apellido) as nombre_profesor, c.descripcion, c.duracion_horas
                FROM Horarios h
                JOIN Cursos c ON h.curso_id = c.id_curso
                JOIN Profesores p ON c.profesor_id = p.id_profesor
                WHERE h.curso_id = %s
                ORDER BY 
                    CASE h.dia_semana
                        WHEN 'Lunes' THEN 1
                        WHEN 'Martes' THEN 2
                        WHEN 'Miércoles' THEN 3
                        WHEN 'Jueves' THEN 4
                        WHEN 'Viernes' THEN 5
                        WHEN 'Sábado' THEN 6
                        WHEN 'Domingo' THEN 7
                    END,
                    h.hora_inicio
            """
            params = (curso_id,)
            resultado = self.db.execute_select(sql, params)
            
            """horarios = []
            for row in resultado:
                horario = Horario(
                    id_horario=row[0],
                    curso_id=row[1],
                    dia_semana=row[2],
                    hora_inicio=row[3],
                    hora_fin=row[4]
                )
                # Agregar información del curso al horario
                horario.curso = Curso(
                    id_curso=row[1],
                    nombre=row[5],
                    profesor=row[6],
                    descripcion=row[7],
                    duracion_horas=row[8]
                )
                horarios.append(horario)
                """
            #return horarios
            return resultado
            
        except Exception as e:
            print(f"Error al obtener horarios del curso: {str(e)}")
            return []

