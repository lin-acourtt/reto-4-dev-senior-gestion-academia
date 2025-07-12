
from config.database import Database
from models.Estudiante import Estudiante

class EstudianteController:
    """
        Controlador para realizar operaciones con la tabla de estudiantes. 
        - Métodos:
            - registrar_estudiante -> Registra un solo estudiante
            - listar_estudiantes -> Obtiene una lista de todos los estudiantes
            - obtener_estudiante_por_id -> Obtiene detalles de estudiante por su ID.
            - actualizar_estudiante_por_id -> Actualiza todos los atributos de un estudiante.
            - eliminar_estudiante_por_id -> Elimina un estudiante por su ID.
    """

    # The controller will require a DB object
    def __init__(self, db):
        self.db = db

    def registrar_estudiante(self,nombre,apellido,correo,telefono):
        
        sql = """
            INSERT INTO Estudiantes (nombre,apellido,correo_electronico,telefono)
            VALUES (%s,%s,%s,%s);
        """
        params=(nombre,apellido,correo,telefono)
        self.db.execute_query(sql,params)
    
    def listar_estudiantes(self):
        # sql = "SELECT * FROM estudiantes"
        sql = "SELECT id_estudiante, nombre, apellido, correo_electronico, telefono FROM Estudiantes"
        resultados = self.db.execute_select(sql)
        return [Estudiante(*resultado) for resultado in resultados]
    
    def obtener_estudiante_por_id(self,id_estudiante):
        """
            Retorna el objeto del estudiante con el ID especificado
        """
        sql = """SELECT id_estudiante, nombre, apellido, correo_electronico, telefono FROM Estudiantes WHERE id_estudiante = %s"""
        params = (id_estudiante,)
        resultado = self.db.execute_select(sql, params)
        return Estudiante(*resultado[0]) if resultado else None

    def actualizar_estudiante_por_id(self,id_estudiante,nombre,apellido,correo,telefono):
        """
            Actualiza todos los parámetros de un estudiante por su ID
        """
        sql = """
            UPDATE Estudiantes SET nombre=%s, apellido=%s, correo_electronico=%s, telefono=%s 
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
            DELETE FROM Estudiantes WHERE id_estudiante= %s
        """
        params = (id_estudiante,)
        resultado = self.db.execute_query(sql, params)

