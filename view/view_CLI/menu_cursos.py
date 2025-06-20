from controllers.curso_controller import CursoController
from mysql.connector import IntegrityError

def menu_cursos(db):

    curso_controller = CursoController(db)

    while True:
        print("Bienvenido")
        print("1. Registrar curso.")
        print("2. Listar cursos")
        print("3. Obtener curso por ID.")
        print("4. Actualizar curso")
        print("5. Eliminar curso")
        print("9. Salir.")

        opcion = int(input("Selecciona la opcion: "))
        if opcion == 1:
            opcion_registrar_curso(curso_controller)
        elif opcion == 2:
            opcion_listar_cursos(curso_controller)
        elif opcion == 3:
            opcion_obtener_curso_por_id(curso_controller)
        elif opcion == 4:
            opcion_actualizar_curso(curso_controller)
        elif opcion == 5:
            opcion_eliminar_curso_por_id(curso_controller)
        elif opcion == 9:
            print("Saliste.")
            break

def opcion_registrar_curso(curso_controller):
    print ("============Registrar Curso=============")
    nombre = input("Nombre: ")
    descripcion = input("Descripción: ")
    duracion_horas = input("Duración Horas: ")
    profesor_id = input("ID del profesor: ")

    try:
        curso_controller.registrar_curso(nombre, descripcion, duracion_horas, profesor_id)
        print("Curso registrado correctamente")
    except IntegrityError as e:
        print(f"Error de integridad: {e.msg}")
    except Exception as e: 
        print(f"Error al registrar el curso: {str(e)}")

def opcion_listar_cursos(curso_controller):
    print ("============Listar Cursos=============")
    try:
        cursos, nombre_profesores = curso_controller.listar_cursos()
        if cursos:
            print("ID\tNombre\tDescripción\tDuración Horas\tID Profesor\tNombre Profesor")
            for e,p in zip(cursos,nombre_profesores):
                print(f"{e.id_curso} | {e.nombre} | {e.descripcion} | {e.duracion_horas} | {e.profesor_id} | {p}")
            input("---")
        else:
            print("No se encontraron cursos registrados.")
    except Exception as e:
        print(f"Error al listar los cursos: {str(e)}")

def opcion_obtener_curso_por_id(curso_controller):
    print("============Obtener curso por ID=============")
    id_curso = int(input("ID del curso: "))
    try:
        curso, nombre_profesor = curso_controller.obtener_curso_por_id(id_curso)
        if curso:
            print(f"ID: {curso.id_curso}")
            print(f"Nombre: {curso.nombre}")
            print(f"Descripción: {curso.descripcion}")
            print(f"Duración Horas: {curso.duracion_horas}")
            print(f"ID Profesor: {curso.profesor_id}")
            print(f"Nombre Profesor: {nombre_profesor}")
            input("--------------------------")
        else:
            print("Curso no encontrado")
            return
    except Exception as e:
        print(f"Error del curso: {str(e)}")

def opcion_actualizar_curso(curso_controller):
    # Primero se obtiene el curso:
    id_curso = int(input("ID del curso: "))
    try:
        curso, nombre_profesor = curso_controller.obtener_curso_por_id(id_curso)
        if curso:
            nombre_actual = curso.nombre
            descripcion_actual = curso.descripcion
            duracion_horas_actual = curso.duracion_horas
            profesor_id_actual = curso.profesor_id

            print(f"ID: {curso.id_curso}")
            nombre = input(f"Nombre Actual: {curso.nombre}, Nuevo Nombre:").strip()
            descripcion = input(f"Descripción Actual: {curso.descripcion}, Nueva Descripción: ").strip()
            duracion_horas = input(f"Duración Horas Actual: {curso.duracion_horas}, Nueva Duración Horas: ").strip()
            profesor_id = input(f"Profesor ID Actual: {curso.profesor_id}, Profesor ID nuevo: ").strip()

            if nombre == '':
                nombre = nombre_actual
            if descripcion == '':
                descripcion = descripcion_actual
            if duracion_horas == '':
                duracion_horas = duracion_horas_actual
            if profesor_id == '':
                profesor_id = profesor_id_actual
            
            curso_controller.actualizar_curso_por_id(curso.id_curso,nombre,descripcion,duracion_horas,profesor_id)
            print("Curso actualizado correctamente.")
            input("--------------------------")
        else:
            print("Curso no encontrado")
            return
    except Exception as e:
        print(f"Error del curso: {str(e)}")


def opcion_eliminar_curso_por_id(curso_controller):
    print("============Eliminar curso por ID=============")
    id_curso = int(input("ID del curso: "))
    try:
        curso_controller.eliminar_curso_por_id(id_curso)
    except Exception as e:
        print(f"Error del curso: {str(e)}")