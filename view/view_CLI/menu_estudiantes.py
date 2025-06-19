from controllers.estudiante_controller import EstudianteController
from mysql.connector import IntegrityError

def menu_estudiantes(db):

    estudiante_controller = EstudianteController(db)

    while True:
        print("Bienvenido")
        print("1. Registrar estudiante.")
        print("2. Listar estudiantes")
        print("3. Obtener estudiante por ID.")
        print("4. Actualizar estudiante")
        print("5. Eliminar estudiante")
        print("9. Salir.")

        opcion = int(input("Selecciona la opcion: "))
        if opcion == 1:
            opcion_registrar_estudiante(estudiante_controller)
        elif opcion == 2:
            opcion_listar_estudiantes(estudiante_controller)
        elif opcion == 3:
            opcion_obtener_estudiante_por_id(estudiante_controller)
        elif opcion == 4:
            opcion_actualizar_estudiante(estudiante_controller)
        elif opcion == 5:
            opcion_eliminar_estudiante_por_id(estudiante_controller)
        elif opcion == 9:
            print("Saliste.")
            break

def opcion_registrar_estudiante(estudiante_controller):
    print ("============Registrar Estudiante=============")
    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    correo = input("Correo: ")
    telefono = input("Teléfono: ")

    try:
        estudiante_controller.registrar_estudiante(nombres, apellidos, correo, telefono)
        print("Estudiante registrado correctamente")
    except IntegrityError as e:
        print(f"Error de integridad: {e.msg}")
    except Exception as e: 
        print(f"Error al registrar el estudiante: {str(e)}")

def opcion_listar_estudiantes(estudiante_controller):
    print ("============Listar Estudiantes=============")
    try:
        estudiantes = estudiante_controller.listar_estudiantes()
        if estudiantes:
            print("ID\tNombres\tApellidos\tCorreo\tTeléfono")
            for e in estudiantes:
                print(f"{e.id_estudiante} | {e.nombre} {e.apellido} | {e.correo} | {e.telefono}")
            input("---")
        else:
            print("No se encontraron estudiantes registrados.")
    except Exception as e:
        print(f"Error al listar los estudiantes: {str(e)}")

def opcion_obtener_estudiante_por_id(estudiante_controller):
    print("============Obtener estudiante por ID=============")
    id_estudiante = int(input("ID del estudiante: "))
    try:
        estudiante = estudiante_controller.obtener_estudiante_por_id(id_estudiante)
        if estudiante:
            print(f"ID: {estudiante.id_estudiante}")
            print(f"Nombre: {estudiante.nombre}")
            print(f"Apellido: {estudiante.apellido}")
            print(f"Correo: {estudiante.correo}")
            print(f"Teléfono: {estudiante.telefono}")
            input("--------------------------")
        else:
            print("Estudiante no encontrado")
            return
    except Exception as e:
        print(f"Error del estudiante: {str(e)}")

def opcion_actualizar_estudiante(estudiante_controller):
    # Primero se obtiene el estudiante:
    id_estudiante = int(input("ID del estudiante: "))
    try:
        estudiante = estudiante_controller.obtener_estudiante_por_id(id_estudiante)
        if estudiante:
            nombre_actual = estudiante.nombre
            apellido_actual = estudiante.apellido
            correo_actual = estudiante.correo
            telefono_actual = estudiante.telefono

            print(f"ID: {estudiante.id_estudiante}")
            nombre = input(f"Nombre Actual: {estudiante.nombre}, Nuevo Nombre:").strip()
            apellido = input(f"Apellido Actual: {estudiante.apellido}, Nuevo Apellido: ").strip()
            correo = input(f"Correo Actual: {estudiante.correo}, Correo Nuevo: ").strip()
            telefono = input(f"Teléfono Actual: {estudiante.telefono}, Telèfono nuevo: ").strip()

            if nombre == '':
                nombre = nombre_actual
            if apellido == '':
                apellido = apellido_actual
            if correo == '':
                correo = correo_actual
            if telefono == '':
                telfono = telefono_actual
            
            estudiante_controller.actualizar_estudiante_por_id(estudiante.id_estudiante,nombre,apellido,correo,telefono)
            print("Estudiante actualizado correctamente.")
            input("--------------------------")
        else:
            print("Estudiante no encontrado")
            return
    except Exception as e:
        print(f"Error del estudiante: {str(e)}")


def opcion_eliminar_estudiante_por_id(estudiante_controller):
    print("============Eliminar estudiante por ID=============")
    id_estudiante = int(input("ID del estudiante: "))
    try:
        estudiante_controller.eliminar_estudiante_por_id(id_estudiante)
    except Exception as e:
        print(f"Error del estudiante: {str(e)}")