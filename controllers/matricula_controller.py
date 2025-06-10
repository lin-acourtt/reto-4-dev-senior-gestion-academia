#from config.database import Database
from models.Matricula import Matricula
from models.Estudiante import Estudiante
from models.Curso import Curso

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
        resultado = self.db.execute_query(sql, params)

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

    def buscar_matriculas(self, id_curso=None, nombre_curso=None, nombre_estudiante=None):
        """
        Busca matrículas según los filtros proporcionados
        
        Args:
            id_curso (int, optional): ID del curso para filtrar
            nombre_curso (str, optional): Nombre del curso para filtrar
            nombre_estudiante (str, optional): Nombre del estudiante para filtrar
            
        Returns:
            list: Lista de objetos Matricula con información detallada
        """
        try:
            # Debug: Imprimir parámetros recibidos
           # print(f"Buscando matrículas con parámetros: id_curso={id_curso}, nombre_curso={nombre_curso}, nombre_estudiante={nombre_estudiante}")
            
            query = """
                SELECT 
                    m.id_matricula,
                    m.estudiante_id,
                    m.curso_id,
                    m.fecha_matricula,
                    e.nombre as nombre_estudiante,
                    e.apellido as apellido_estudiante,
                    c.nombre as nombre_curso,
                    CONCAT(p.nombre, ' ', p.apellido) as profesor
                FROM matriculas m
                JOIN estudiantes e ON m.estudiante_id = e.id_estudiante
                JOIN cursos c ON m.curso_id = c.id_curso
                LEFT JOIN profesores p ON c.profesor_id = p.id_profesor
                WHERE 1=1
            """
            params = []
            
            if id_curso:
                query += " AND m.curso_id = %s"
                params.append(id_curso)
            elif nombre_curso:
                query += " AND c.nombre LIKE %s"
                params.append(f"%{nombre_curso}%")
                
            if nombre_estudiante:
                query += " AND (e.nombre LIKE %s OR e.apellido LIKE %s)"
                params.extend([f"%{nombre_estudiante}%", f"%{nombre_estudiante}%"])
                
            query += " ORDER BY m.fecha_matricula DESC"
            
            # Debug: Imprimir query y parámetros
            # print(f"Query: {query}")
            # print(f"Parámetros: {params}")
            
            resultados = self.db.execute_select(query, tuple(params))
            
            # Debug: Imprimir resultados
            #print(f"Número de resultados encontrados: {len(resultados)}")
            #if resultados:
            #    print("Primer resultado:", resultados[0])
            
            matriculas = []
            for row in resultados:
                # Crear objeto Estudiante
                estudiante = Estudiante(
                    id_estudiante=row[1],
                    nombre=row[4],
                    apellido=row[5],
                    correo=None,
                    telefono=None
                )
                
                # Crear objeto Curso
                curso = Curso(
                    id_curso=row[2],
                    nombre=row[6],
                    profesor=row[7],
                    num_estudiantes=None,
                    horarios=None,
                    descripcion=None,
                    duracion_horas=None
                )
                
                # Crear objeto Matricula
                matricula = Matricula(
                    id_matricula=row[0],
                    estudiante_id=row[1],
                    curso_id=row[2],
                    fecha_matricula=row[3]
                )
                
                # Agregar objetos relacionados
                matricula.estudiante = estudiante
                matricula.curso = curso
                
                matriculas.append(matricula)
            
            # Debug: Imprimir número de matrículas creadas
            #print(f"Número de matrículas creadas: {len(matriculas)}")
            
            return matriculas
            
        except Exception as e:
            print(f"Error al buscar matrículas: {str(e)}")
            # Debug: Imprimir el traceback completo
            #import traceback
            #traceback.print_exc()
            return []

    def obtener_estudiantes_por_curso(self,id_curso):
        """
            Retorna el objeto del matricula con el ID especificado
        """
        sql = """
            SELECT m.id_matricula, 
                m.estudiante_id, 
                CONCAT(e.nombre, ' ', e.apellido) as nombre_estudiante, 
                m.fecha_matricula 
                FROM matriculas m
                JOIN estudiantes e ON m.estudiante_id = e.id_estudiante
                WHERE m.curso_id=%s;
        """
        params = (id_curso,)
        resultado = self.db.execute_select(sql, params)

        return resultado

