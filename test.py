cursos = [{'id_curso': 1, 'nombre': 'Matematicas Discretas', 'profesor': 'Pedro Lopez', 'descripcion': 'Matematicas Discretas', 'duracion_horas': 100, 'horarios': 'Lunes 08:00-10:00, Miercoles 10:00-12:00, Lunes 13:00-15:00'}]

lista = []

for c in cursos:
    fila = []
    elementos = c.values()
    for e in elementos:
        fila.append(e)

    lista.append(fila)


print(lista)