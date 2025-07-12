class Estudiante:
    """
        Constructor de la clase Estudiantes
        Args:
            id_estudiante: Identificador único del estudiante
            nombre: Nombre del estudiante
            apellido: Apellido del estudiante
            correo: Correo del estudiante
            telefono: Teléfono del estudiante
        """
    
    def __init__(self, id_estudiante, nombre, apellido, correo, telefono):
        self.id_estudiante = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.telefono = telefono