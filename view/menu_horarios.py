from controllers.horario_controller import HorarioController
from mysql.connector import IntegrityError
from datetime import datetime

def menu_horarios(db):

    horario_controller = HorarioController(db)

    while True:
        print("Bienvenido")
        print("1. Registrar horario.")
        print("2. Listar horarios")
        print("3. Obtener horario por ID.")
        print("4. Actualizar horario")
        print("5. Eliminar horario")
        print("9. Salir.")

        opcion = int(input("Selecciona la opcion: "))
        if opcion == 1:
            opcion_registrar_horario(horario_controller)
        elif opcion == 2:
            opcion_listar_horarios(horario_controller)
        elif opcion == 3:
            opcion_obtener_horario_por_id(horario_controller)
        elif opcion == 4:
            opcion_actualizar_horario(horario_controller)
        elif opcion == 5:
            opcion_eliminar_horario_por_id(horario_controller)
        elif opcion == 9:
            print("Saliste.")
            break

def opcion_registrar_horario(horario_controller):
    print ("============Registrar Horario=============")
    curso_id = input("ID del curso: ")
    dia_semana = input("Día de la semana: ")
    hora_inicio = input("Hora de inicio: ")
    hora_fin = input("Hora de fin: ")

    try:
        hora_inicio = datetime.strptime(hora_inicio, "%H:%M")
        hora_fin = datetime.strptime(hora_fin, "%H:%M")

        hora_inicio = datetime.time(hora_inicio)
        hora_fin = datetime.time(hora_fin)

        horario_controller.registrar_horario(curso_id, dia_semana, hora_inicio, hora_fin)
        print("Horario registrado correctamente")
    except IntegrityError as e:
        print(f"Error de integridad: {e.msg}")
    except Exception as e: 
        print(f"Error al registrar el horario: {str(e)}")

def opcion_listar_horarios(horario_controller):
    print ("============Listar Horarios=============")
    try:
        horarios, nombre_cursos = horario_controller.listar_horarios()
        if horarios:
            print("ID Horario\tID Curso\tCurso\tDía de semana\tHora inicio\tHora fin")
            for e,p in zip(horarios,nombre_cursos):
                print(f"{e.id_horario} | {e.curso_id} | {p} | {e.dia_semana} | {e.hora_inicio} | {e.hora_fin} |")
            input("---")
        else:
            print("No se encontraron horarios registrados.")
    except Exception as e:
        print(f"Error al listar los horarios: {str(e)}")

def opcion_obtener_horario_por_id(horario_controller):
    print("============Obtener horario por ID=============")
    id_horario = int(input("ID del horario: "))
    try:
        horario, nombre_curso = horario_controller.obtener_horario_por_id(id_horario)
        if horario:
            print(f"ID Horario: {horario.id_horario}")
            print(f"ID Curso: {horario.curso_id}")
            print(f"Nombre Curso: {nombre_curso}")
            print(f"Día de semana: {horario.dia_semana}")
            print(f"Hora Inicio: {horario.hora_inicio}")
            print(f"Hora Fin: {horario.hora_fin}")
            input("--------------------------")
        else:
            print("Horario no encontrado")
            return
    except Exception as e:
        print(f"Error del horario: {str(e)}")

def opcion_actualizar_horario(horario_controller):
    # Primero se obtiene el horario:
    id_horario = int(input("ID del horario: "))
    try:
        horario, nombre_curso = horario_controller.obtener_horario_por_id(id_horario)
        if horario:
            curso_id_actual = horario.curso_id
            dia_semana_actual = horario.dia_semana
            hora_inicio_actual = horario.hora_inicio
            hora_fin_actual = horario.hora_fin

            print(f"ID: {horario.id_horario}")
            curso_id = input(f"ID Curso Actual: {horario.curso_id}, Nuevo Curso ID:").strip()
            dia_semana = input(f"Día Semana Actual: {horario.dia_semana}, Nueva Descripción: ").strip()
            hora_inicio = input(f"Hora Inicio Actual: {horario.hora_inicio}, Hora Inicio Horas: ").strip()
            hora_fin = input(f"Hora Fin Actual: {horario.hora_fin}, Hora Fin nuevo: ").strip()

            hora_inicio = datetime.strptime(hora_inicio, "%H:%M")
            hora_fin = datetime.strptime(hora_fin, "%H:%M")

            hora_inicio = datetime.time(hora_inicio)
            hora_fin = datetime.time(hora_fin)

            if curso_id == '':
                curso_id = curso_id_actual
            if dia_semana == '':
                dia_semana = dia_semana_actual
            if hora_inicio == '':
                hora_inicio = hora_inicio_actual
            if hora_fin == '':
                hora_fin = hora_fin_actual
            
            horario_controller.actualizar_horario_por_id(horario.id_horario,curso_id,dia_semana,hora_inicio,hora_fin)
            print("Horario actualizado correctamente.")
            input("--------------------------")
        else:
            print("Horario no encontrado")
            return
    except Exception as e:
        print(f"Error del horario: {str(e)}")


def opcion_eliminar_horario_por_id(horario_controller):
    print("============Eliminar horario por ID=============")
    id_horario = int(input("ID del horario: "))
    try:
        horario_controller.eliminar_horario_por_id(id_horario)
    except Exception as e:
        print(f"Error del horario: {str(e)}")