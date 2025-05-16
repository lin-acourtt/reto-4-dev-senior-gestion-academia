
#from config.database import Database
from models.Horario import Horario

class HorarioController:

    # The controller will require a DB object
    def __init__(self, db):
        self.db = db

    def registrar_horario(self,curso_id,dia_semana,hora_inicio,hora_fin):
        
        sql = """
            INSERT INTO horarios (curso_id,dia_semana,hora_inicio,hora_fin)
            VALUES (%s,%s,%s,%s);
        """
        params=(curso_id,dia_semana,hora_inicio,hora_fin)
        self.db.execute_query(sql,params)
    
    def listar_horarios(self):
        # sql = "SELECT * FROM horarios"
        # sql = "SELECT id_horario, nombre, descripcion, duracion_horas, profesor_id FROM horarios"
        sql = """
            SELECT horarios.id_horario, horarios.curso_id, horarios.dia_semana, horarios.hora_inicio, horarios.hora_fin, 
            cursos.nombre FROM horarios 
            JOIN cursos on (horarios.curso_id = cursos.id_curso);
        """
        resultados = self.db.execute_select(sql)
        nombre_cursos = [detalles_horario[5] for detalles_horario in resultados] # Es nombre del curso de este horario
        return [Horario(*resultado[0:5]) for resultado in resultados], nombre_cursos
    
    def obtener_horario_por_id(self,id_horario):
        """
            Retorna el objeto del horario con el ID especificado
        """
        sql = """
            SELECT horarios.id_horario, horarios.curso_id, horarios.dia_semana, horarios.hora_inicio, horarios.hora_fin, 
            cursos.nombre FROM horarios 
            JOIN cursos on (horarios.curso_id = cursos.id_curso)
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
            UPDATE horarios SET curso_id=%s, dia_semana=%s, hora_inicio=%s, hora_fin=%s 
            WHERE id_horario= %s
        """
        params = (curso_id,dia_semana,hora_inicio,hora_fin,id_horario)
        resultado = self.db.execute_select(sql, params)

    def eliminar_horario_por_id(self, id_horario):
        """
            Elimina un horario dando un ID
        """
        sql = """
            DELETE FROM horarios WHERE id_horario= %s
        """
        params = (id_horario,)
        resultado = self.db.execute_query(sql, params)

