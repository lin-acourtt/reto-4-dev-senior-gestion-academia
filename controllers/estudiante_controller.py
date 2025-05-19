
from config.database import Database
from models.Estudiante import Estudiante

class EstudianteController:

    # The controller will require a DB object
    def __init__(self, db):
        self.db = db

    def registrar_estudiante(self,nombre,apellido,correo,telefono):
        
        sql = """
            INSERT INTO estudiantes (nombre,apellido,correo_electronico,telefono)
            VALUES (%s,%s,%s,%s);
        """
        params=(nombre,apellido,correo,telefono)
        self.db.execute_query(sql,params)
    
    def listar_estudiantes(self):
        # sql = "SELECT * FROM estudiantes"
        sql = "SELECT id_estudiante, nombre, apellido, correo_electronico, telefono FROM estudiantes"
        resultados = self.db.execute_select(sql)
        return [Estudiante(*resultado) for resultado in resultados]
    
    def obtener_estudiante_por_id(self,id_estudiante):
        """
            Retorna el objeto del estudiante con el ID especificado
        """
        sql = """SELECT id_estudiante, nombre, apellido, correo_electronico, telefono FROM estudiantes WHERE id_estudiante = %s"""
        params = (id_estudiante,)
        resultado = self.db.execute_select(sql, params)
        return Estudiante(*resultado[0]) if resultado else None

    def actualizar_estudiante_por_id(self,id_estudiante,nombre,apellido,correo,telefono):
        """
            Actualiza todos los parámetros de un estudiante por su ID
        """
        sql = """
            UPDATE estudiantes SET nombre=%s, apellido=%s, correo_electronico=%s, telefono=%s 
            WHERE id_estudiante= %s
        """
        params = (nombre,apellido,correo,telefono,id_estudiante)
        self.db.execute_query(sql,params)
        #resultado = self.db.execute_select(sql, params)

    def eliminar_estudiante_por_id(self, id_estudiante):
        """
            Elimina un estudiante dando un ID
        """
        sql = """
            DELETE FROM estudiantes WHERE id_estudiante= %s
        """
        params = (id_estudiante,)
        resultado = self.db.execute_query(sql, params)

