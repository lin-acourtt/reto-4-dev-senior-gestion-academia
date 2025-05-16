-- Crear la base de datos
CREATE DATABASE if NOT EXISTS proyecto_gestion_cursos_academia;

-- Usar la base de datos 
USE proyecto_gestion_cursos_academia;

-- Tabla: Estudiantes
CREATE TABLE Estudiantes (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    correo_electronico VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20)
);

-- Tabla: Profesores
CREATE TABLE Profesores (
    id_profesor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    correo_electronico VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    especialidad VARCHAR(50)
);

-- Tabla: Cursos
CREATE TABLE Cursos (
    id_curso INT AUTO_INCREMENT PRIMARY KEY, 
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    duracion_horas INT,
    profesor_id INT, 
    FOREIGN KEY (profesor_id) REFERENCES Profesores(id_profesor)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Tabla: Matrículas (Releación N:N entre estudiantes y cursos)
CREATE TABLE Matriculas (
    id_matricula INT AUTO_INCREMENT PRIMARY KEY,
    estudiante_id INT,
    curso_id INT,
    fecha_matricula DATE,
    FOREIGN KEY (estudiante_id) REFERENCES Estudiantes(id_estudiante)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (curso_id) REFERENCES Cursos(id_curso)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Tabla: Horarios (Relación 1:N Entre cursos y horarios)
CREATE TABLE Horarios (
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    curso_id INT,
    dia_semana VARCHAR(50),
    hora_inicio TIME,
    hora_fin TIME,
    FOREIGN KEY (curso_id) REFERENCES Cursos(id_curso)
        ON DELETE CASCADE ON UPDATE CASCADE
);


INSERT INTO Estudiantes (nombre, apellido, correo_electronico, telefono)
VALUES ('Juan', 'Perez', 'jperez@dominio.com', '1234567'),
       ('Maria', 'Gomez', 'mgomez@dominio.com', '9876543');

INSERT INTO Profesores (nombre, apellido, correo_electronico, telefono, especialidad)
VALUES ('Pedro', 'Lopez', 'plopez@dominio.com', '555-1234', 'Matematicas'),
       ('Ana', 'Sanchez', 'asanchez@dominio.com', '555-4321', 'Lenguajes');

INSERT INTO Cursos (nombre, descripcion, duracion_horas, profesor_id)
VALUES ('Matematicas Discretas', 'Matematicas Discretas', 100, 1),
       ('Programacion Avanzada', 'Programacion Avanzada', 80, 2);

INSERT INTO Matriculas (estudiante_id, curso_id, fecha_matricula)
VALUES (1, 1, '2021-03-15'),
       (1, 2, '2021-04-15'),
       (2, 1, '2021-03-15');

INSERT INTO Horarios (curso_id, dia_semana, hora_inicio, hora_fin)
VALUES (1, 'Lunes', '08:00:00', '10:00:00'),
       (1, 'Miercoles', '10:00:00', '12:00:00'),
       (2, 'Martes', '14:00:00', '16:00:00');