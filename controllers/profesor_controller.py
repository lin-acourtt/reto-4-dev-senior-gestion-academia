
from config.database import Database
from models.Profesor import Profesor

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

