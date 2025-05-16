from controllers.profesor_controller import ProfesorController
from mysql.connector import IntegrityError

def menu_profesores(db):

    profesor_controller = ProfesorController(db)

    while True:
        print("Bienvenido")
        print("1. Registrar profesor.")
        print("2. Listar profesores")
        print("3. Obtener profesor por ID.")
        print("4. Actualizar profesor")
        print("5. Eliminar profesor")
        print("9. Salir.")

        opcion = int(input("Selecciona la opcion: "))
        if opcion == 1:
            opcion_registrar_profesor(profesor_controller)
        elif opcion == 2:
            opcion_listar_profesores(profesor_controller)
        elif opcion == 3:
            opcion_obtener_profesor_por_id(profesor_controller)
        elif opcion == 4:
            opcion_actualizar_profesor(profesor_controller)
        elif opcion == 5:
            opcion_eliminar_profesor_por_id(profesor_controller)
        elif opcion == 9:
            print("Saliste.")
            break

def opcion_registrar_profesor(profesor_controller):
    print ("============Registrar Profesor=============")
    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    correo = input("Correo: ")
    telefono = input("Teléfono: ")
    especialidad = input("Especialidad: ")

    try:
        profesor_controller.registrar_profesor(nombres, apellidos, correo, telefono, especialidad)
        input("Profesor registrado correctamente")
    except IntegrityError as e:
        print(f"Error de integridad: {e.msg}")
    except Exception as e: 
        print(f"Error al registrar el profesor: {str(e)}")

def opcion_listar_profesores(profesor_controller):
    print ("============Listar profesores=============")
    try:
        profesores = profesor_controller.listar_profesores()
        if profesores:
            print("ID\tNombres\tApellidos\tCorreo\tTeléfono\tEspecialidad")
            for p in profesores:
                print(f"{p.id_profesor} | {p.nombre} {p.apellido} | {p.correo} | {p.telefono} | {p.especialidad}")
            input("---")
        else:
            print("No se encontraron profesores registrados.")
    except Exception as e:
        print(f"Error al listar los profesores: {str(e)}")

def opcion_obtener_profesor_por_id(profesor_controller):
    print("============Obtener profesor por ID=============")
    id_profesor = int(input("ID del profesor: "))
    try:
        profesor = profesor_controller.obtener_profesor_por_id(id_profesor)
        if profesor:
            print(f"ID: {profesor.id_profesor}")
            print(f"Nombre: {profesor.nombre}")
            print(f"Apellido: {profesor.apellido}")
            print(f"Correo: {profesor.correo}")
            print(f"Teléfono: {profesor.telefono}")
            input("--------------------------")
        else:
            print("Profesor no encontrado")
            return
    except Exception as e:
        print(f"Error del profesor: {str(e)}")

def opcion_actualizar_profesor(profesor_controller):
    # Primero se obtiene el profesor:
    id_profesor = int(input("ID del profesor: "))
    try:
        profesor = profesor_controller.obtener_profesor_por_id(id_profesor)
        if profesor:
            nombre_actual = profesor.nombre
            apellido_actual = profesor.apellido
            correo_actual = profesor.correo
            telefono_actual = profesor.telefono
            especialidad_actual = profesor.especialidad

            print(f"ID: {profesor.id_profesor}")
            nombre = input(f"Nombre Actual: {profesor.nombre}, Nuevo Nombre:").strip()
            apellido = input(f"Apellido Actual: {profesor.apellido}, Nuevo Apellido: ").strip()
            correo = input(f"Correo Actual: {profesor.correo}, Correo Nuevo: ").strip()
            telefono = input(f"Teléfono Actual: {profesor.telefono}, Telèfono nuevo: ").strip()
            especialidad = input(f"Especialidad Actual: {profesor.especialidad}, Especialidad nueva: ").strip()

            if nombre == '':
                nombre = nombre_actual
            if apellido == '':
                apellido = apellido_actual
            if correo == '':
                correo = correo_actual
            if telefono == '':
                telfono = telefono_actual
            if especialidad == '':
                especialidad = especialidad_actual
            
            profesor_controller.actualizar_profesor_por_id(profesor.id_profesor,nombre,apellido,correo,especialidad,telefono)
            print("Profesor actualizado correctamente.")
            input("--------------------------")
        else:
            print("Profesor no encontrado")
            return
    except Exception as e:
        print(f"Error del profesor: {str(e)}")


def opcion_eliminar_profesor_por_id(profesor_controller):
    print("============Eliminar profesor por ID=============")
    id_profesor = int(input("ID del profesor: "))
    try:
        profesor_controller.eliminar_profesor_por_id(id_profesor)
    except Exception as e:
        print(f"Error del profesor: {str(e)}")