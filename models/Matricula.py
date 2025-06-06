class Matricula:
    
    def __init__(self, id_matricula, estudiante_id, curso_id, fecha_matricula):
        self.id_matricula = id_matricula
        self.estudiante_id = estudiante_id
        self.curso_id = curso_id
        self.fecha_matricula = fecha_matricula
        # Atributos para objetos relacionados
        self.estudiante = None  # Objeto Estudiante
        self.curso = None      # Objeto Curso
        
    def __str__(self):
        """Representación en string del objeto Matricula"""
        estudiante_nombre = f"{self.estudiante.nombre} {self.estudiante.apellido}" if self.estudiante else "Estudiante no especificado"
        curso_nombre = self.curso.nombre if self.curso else "Curso no especificado"
        fecha = self.fecha_matricula.strftime("%d/%m/%Y") if self.fecha_matricula else "No especificada"
        return f"Matrícula {self.id_matricula}: {estudiante_nombre} - {curso_nombre} ({fecha})"