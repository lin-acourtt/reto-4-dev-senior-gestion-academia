#from config.database import Database
from models.Curso import Curso

class CursoController:

    # The controller will require a DB object
    def __init__(self, db):
        """
        Constructor del controlador de cursos
        Args:
            db: Objeto Database para manejar la conexión
        """
        self.db = db

    def registrar_curso(self, nombre, id_profesor, descripcion=None, duracion_horas=None):
        """
        Registra un nuevo curso en la base de datos
        Args:
            nombre: Nombre del curso
            descripcion: Descripción detallada del curso
            duracion_horas: Duración total del curso en horas
            id_profesor: ID del profesor asignado
        Returns:
            bool: True si se registró exitosamente, False en caso contrario
        """
        try:
            sql = """
                INSERT INTO cursos (nombre,descripcion,duracion_horas,profesor_id)
                VALUES (%s,%s,%s,%s);
            """
            params=(nombre,descripcion,duracion_horas,id_profesor)
            self.db.execute_query(sql,params)
            return True
        except Exception as e:
            print(f"Error al registrar curso: {str(e)}")
            return False

    def listar_cursos(self):
        """
        Obtiene la lista de cursos desde la base de datos
        Returns:
            list[Curso]: Lista de objetos Curso
        """
        try:
            # Consulta SQL para obtener cursos con información del profesor y conteo de estudiantes
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
                GROUP BY c.id_curso, c.nombre, profesor, c.descripcion, c.duracion_horas
                ORDER BY c.id_curso
            """
            resultados = self.db.execute_select(query)
            
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
            raise Exception
            #print(f"Error al listar cursos: {str(e)}")
            #return []

    def obtener_curso_por_id(self, id_curso):
        """
        Obtiene un curso específico por su ID
        Args:
            id_curso: ID del curso a buscar
        Returns:
            Curso: Objeto Curso si se encuentra, None en caso contrario
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
                WHERE c.id_curso = %s
                GROUP BY c.id_curso, c.nombre, profesor, c.descripcion, c.duracion_horas
            """
            resultado = self.db.fetchone(query, (id_curso,))
            
            if resultado:
                return Curso(
                    id_curso=resultado[0],
                    nombre=resultado[1],
                    profesor=resultado[2],
                    num_estudiantes=resultado[3],
                    horarios=resultado[4] if resultado[4] else "Sin horario asignado",
                    descripcion=resultado[5],
                    duracion_horas=resultado[6]
                )
            return None
            
        except Exception as e:
            print(f"Error al obtener curso: {str(e)}")
            return None

    def actualizar_curso(self, id_curso, nombre, id_profesor, descripcion=None, duracion_horas=None):
        """
        Actualiza los datos de un curso existente
        Args:
            id_curso: ID del curso a actualizar
            nombre: Nuevo nombre del curso
            id_profesor: Nuevo ID del profesor asignado
            descripcion: Nueva descripción del curso
            duracion_horas: Nueva duración en horas
        Returns:
            bool: True si se actualizó exitosamente, False en caso contrario
        """
        try:
            query = """
                UPDATE cursos 
                SET nombre = %s, 
                    profesor_id = %s, 
                    descripcion = %s, 
                    duracion_horas = %s 
                WHERE id_curso = %s
            """
            self.db.execute_query(query, (nombre, id_profesor, descripcion, duracion_horas, id_curso))
            return True
        except Exception as e:
            print(f"Error al actualizar curso: {str(e)}")
            return False

    def eliminar_curso(self, id_curso):
        """
        Elimina un curso de la base de datos
        Args:
            id_curso: ID del curso a eliminar
        Returns:
            bool: True si se eliminó exitosamente, False en caso contrario
        """
        try:
            # Primero eliminamos las matrículas y horarios asociados
            self.db.execute_query("DELETE FROM matriculas WHERE curso_id = %s", (id_curso,))
            self.db.execute_query("DELETE FROM horarios WHERE curso_id = %s", (id_curso,))
            # Luego eliminamos el curso
            self.db.execute_query("DELETE FROM cursos WHERE id_curso = %s", (id_curso,))
            return True
        except Exception as e:
            print(f"Error al eliminar curso: {str(e)}")
            return False

