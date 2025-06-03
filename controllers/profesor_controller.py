from config.database import Database
from models.Profesor import Profesor
from models.Curso import Curso

class ProfesorController:

    # The controller will require a DB object
    def __init__(self, db):
        self.db = db

    def registrar_profesor(self,nombre,apellido,correo,telefono,especialidad):
        
        sql = """
            INSERT INTO profesores (nombre,apellido,correo_electronico,telefono,especialidad)
            VALUES (%s,%s,%s,%s,%s);
        """
        params=(nombre,apellido,correo,telefono,especialidad)
        self.db.execute_query(sql,params)
    
    def listar_profesores(self):
        sql = "SELECT id_profesor, nombre, apellido, correo_electronico, telefono, especialidad FROM profesores"
        resultados = self.db.execute_select(sql)
        return [Profesor(*resultado) for resultado in resultados]
    
    def obtener_profesor_por_id(self,id_profesor):
        """
            Retorna el objeto del profesor con el ID especificado
        """
        sql = """SELECT id_profesor, nombre, apellido, correo_electronico, telefono, especialidad FROM profesores WHERE id_profesor = %s"""
        params = (id_profesor,)
        resultado = self.db.execute_select(sql, params)
        return Profesor(*resultado[0]) if resultado else None

    def actualizar_profesor_por_id(self,id_profesor,nombre,apellido,correo,telefono,especialidad):
        """
            Actualiza todos los parámetros de un profesor por su ID
        """
        sql = """
            UPDATE profesores SET nombre=%s, apellido=%s, correo_electronico=%s, telefono=%s, especialidad=%s 
            WHERE id_profesor= %s
        """
        params = (nombre,apellido,correo,telefono,especialidad,id_profesor)
        resultado = self.db.execute_select(sql, params)

    def eliminar_profesor_por_id(self, id_profesor):
        """
            Elimina un profesor dando un ID
        """
        sql = """
            DELETE FROM profesores WHERE id_profesor= %s
        """
        params = (id_profesor,)
        resultado = self.db.execute_query(sql, params)

    def obtener_cursos_profesor(self, id_profesor):
        """
        Obtiene los cursos asociados a un profesor específico
        Args:
            id_profesor: ID del profesor
        Returns:
            list[Curso]: Lista de objetos Curso
        """
        try:
            query = """
                SELECT 
                    c.id_curso,
                    c.nombre,
                    CONCAT(p.nombre, ' ', p.apellido) as profesor,
                    COUNT(DISTINCT m.estudiante_id) as num_estudiantes,
                    GROUP_CONCAT(DISTINCT CONCAT(h.dia_semana, ' ', TIME_FORMAT(h.hora_inicio, '%H:%i'), '-', TIME_FORMAT(h.hora_fin, '%H:%i')) SEPARATOR ', ') as horarios,
                    c.descripcion,
                    c.duracion_horas
                FROM cursos c
                LEFT JOIN profesores p ON c.profesor_id = p.id_profesor
                LEFT JOIN matriculas m ON c.id_curso = m.curso_id
                LEFT JOIN horarios h ON c.id_curso = h.curso_id
                WHERE c.profesor_id = %s
                GROUP BY c.id_curso, c.nombre, profesor, c.descripcion, c.duracion_horas
                ORDER BY c.id_curso
            """
            resultados = self.db.execute_select(query, (id_profesor,))
            
            # Convertir resultados a objetos Curso
            cursos = []
            for row in resultados:
                curso = Curso(
                    id_curso=row[0],
                    nombre=row[1],
                    profesor=row[2],
                    num_estudiantes=row[3],
                    horarios=row[4] if row[4] else "Sin horario asignado",
                    descripcion=row[5],
                    duracion_horas=row[6]
                )
                cursos.append(curso)
                
            return cursos
            
        except Exception as e:
            print(f"Error al obtener cursos del profesor: {str(e)}")
            return []

