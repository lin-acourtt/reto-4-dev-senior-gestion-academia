class Profesor:
    """
        Constructor de la clase Profesor
        Args:
            id_profesor: Identificador único del profesor
            nombre: Nombre del profesor
            apellido: Apellido del profesor
            correo: Correo del profesor
            telefono: Teléfono del profesor
            especialidad: Especialidad del profesor
        """
    
    def __init__(self, id_profesor, nombre, apellido, correo, telefono, especialidad):
        self.id_profesor = id_profesor
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.telefono = telefono
        self.especialidad = especialidad