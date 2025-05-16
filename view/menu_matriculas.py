from controllers.matricula_controller import MatriculaController
from mysql.connector import IntegrityError
from datetime import datetime

def menu_matriculas(db):

    matricula_controller = MatriculaController(db)

    while True:
        print("Bienvenido")
        print("1. Registrar matricula.")
        print("2. Listar matriculas")
        print("3. Obtener matricula por ID.")
        print("4. Actualizar matricula")
        print("5. Eliminar matricula")
        print("9. Salir.")

        opcion = int(input("Selecciona la opcion: "))
        if opcion == 1:
            opcion_registrar_matricula(matricula_controller)
        elif opcion == 2:
            opcion_listar_matriculas(matricula_controller)
        elif opcion == 3:
            opcion_obtener_matricula_por_id(matricula_controller)
        elif opcion == 4:
            opcion_actualizar_matricula(matricula_controller)
        elif opcion == 5:
            opcion_eliminar_matricula_por_id(matricula_controller)
        elif opcion == 9:
            print("Saliste.")
            break

def opcion_registrar_matricula(matricula_controller):
    print ("============Registrar Matricula=============")
    estudiante_id = input("ID del estudiante: ")
    curso_id = input("ID del curso: ")
    fecha_matricula = input("Fecha de matrícula: ")

    try:
        fecha_matricula = datetime.strptime(fecha_matricula, "%Y-%m-%d")

        fecha_matricula = datetime.date(fecha_matricula)

        matricula_controller.registrar_matricula(estudiante_id, curso_id, fecha_matricula)
        print("Matricula registrada correctamente")
    except IntegrityError as e:
        print(f"Error de integridad: {e.msg}")
    except Exception as e: 
        print(f"Error al registrar el matricula: {str(e)}")

def opcion_listar_matriculas(matricula_controller):
    print ("============Listar Matriculas=============")
    try:
        matriculas, nombre_estudiantes, nombre_cursos = matricula_controller.listar_matriculas()
        if matriculas:
            print("ID Matricula\tID Estudiante\tNombre Estudiante\tID Curso\tNombre Curso\tFecha de matrícula")
            for m,e,c in zip(matriculas,nombre_estudiantes,nombre_cursos):
                print(f"{m.id_matricula} | {m.estudiante_id} | {e} | {m.curso_id} | {c} | {m.fecha_matricula} |")
            input("---")
        else:
            print("No se encontraron matriculas registrados.")
    except Exception as e:
        print(f"Error al listar los matriculas: {str(e)}")

def opcion_obtener_matricula_por_id(matricula_controller):
    print("============Obtener matricula por ID=============")
    id_matricula = int(input("ID del matricula: "))
    try:
        matricula, nombre_estudiante, nombre_curso = matricula_controller.obtener_matricula_por_id(id_matricula)
        if matricula:
            print(f"ID Matricula: {matricula.id_matricula}")
            print(f"ID Estudiante: {matricula.estudiante_id}")
            print(f'Nombre Estudiante: {nombre_estudiante}')
            print(f"ID Curso: {matricula.curso_id}")
            print(f'Nombre Curso: {nombre_curso}')
            print(f"Fecha de matrícula: {matricula.fecha_matricula}")
            input("--------------------------")
        else:
            print("Matricula no encontrado")
            return
    except Exception as e:
        print(f"Error del matricula: {str(e)}")

def opcion_actualizar_matricula(matricula_controller):
    # Primero se obtiene el matricula:
    id_matricula = int(input("ID del matricula: "))
    try:
        matricula, nombre_estudiante, nombre_curso = matricula_controller.obtener_matricula_por_id(id_matricula)
        if matricula:
            estudiante_id_actual = matricula.estudiante_id
            curso_id_actual = matricula.curso_id
            fecha_matricula_actual = matricula.fecha_matricula

            print(f"ID: {matricula.id_matricula}")
            estudiante_id = input(f"ID Estudiante Actual: {matricula.estudiante_id}, Nuevo ID Estudiante: ")
            curso_id = input(f"ID Curso Actual: {matricula.curso_id}, Nuevo Curso ID:").strip()
            fecha_matricula = input(f"Fecha matrícula Actual: {matricula.fecha_matricula}, Nueva Fecha Matrícula: ").strip()

            if estudiante_id == "":
                estudiante_id = estudiante_id_actual
            if curso_id == '':
                curso_id = curso_id_actual
            if fecha_matricula == '':
                fecha_matricula = fecha_matricula_actual
            else:
                fecha_matricula = datetime.strptime(fecha_matricula, "%Y-%m-%d")
                fecha_matricula = datetime.date(fecha_matricula)
            
            matricula_controller.actualizar_matricula_por_id(matricula.id_matricula,estudiante_id,curso_id,fecha_matricula)
            print("Matricula actualizado correctamente.")
            input("--------------------------")
        else:
            print("Matricula no encontrado")
            return
    except Exception as e:
        print(f"Error del matricula: {str(e)}")


def opcion_eliminar_matricula_por_id(matricula_controller):
    print("============Eliminar matricula por ID=============")
    id_matricula = int(input("ID del matricula: "))
    try:
        matricula_controller.eliminar_matricula_por_id(id_matricula)
    except Exception as e:
        print(f"Error del matricula: {str(e)}")