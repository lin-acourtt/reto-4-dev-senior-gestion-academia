class Curso:
    def __init__(self, id_curso, nombre, profesor, num_estudiantes, horarios, descripcion=None, duracion_horas=None):
        """
        Constructor de la clase Curso
        Args:
            id_curso: Identificador único del curso
            nombre: Nombre del curso
            profesor: Nombre completo del profesor asignado
            num_estudiantes: Número de estudiantes matriculados
            horarios: Horarios asignados al curso
            descripcion: Descripción detallada del curso
            duracion_horas: Duración total del curso en horas
        """
        self.id_curso = id_curso
        self.nombre = nombre
        self.profesor = profesor
        self.num_estudiantes = num_estudiantes
        self.horarios = horarios
        self.descripcion = descripcion
        self.duracion_horas = duracion_horas

    def __str__(self):
        """Representación en string del objeto Curso"""
        return f"Curso {self.id_curso}: {self.nombre} - Profesor: {self.profesor} - Duración: {self.duracion_horas} horas"