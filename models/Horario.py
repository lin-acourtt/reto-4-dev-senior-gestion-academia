class Horario:
    """
        Constructor de la clase Horario
        Args:
            id_horario: Identificador único del horario
            curso_id: ID del curso asociado al horario
            dia_semana: Día de la semana
            hora_inicio: Hora de inicio de la clase
            hora_fin: Hora de fin de la clase
        """
    
    def __init__(self, id_horario, curso_id, dia_semana, hora_inicio, hora_fin):
        self.id_horario = id_horario
        self.curso_id = curso_id
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin