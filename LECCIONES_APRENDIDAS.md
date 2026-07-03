# Lecciones Aprendidas — Taller Práctico
## Sistema de Gestión de Expedientes (Prototipo → Base de Datos → API REST)

> **Nota:** este documento es una base. Complétalo con tu experiencia real
> (errores que te salieron, cosas que te costaron, qué harías distinto).

---

## 1. Del prototipo al diseño de la base de datos

- Aprendí que un prototipo visual ya contiene las **entidades** del sistema:
  la pantalla de login implica una tabla `usuarios`; la tabla "Agenda del día"
  muestra expedientes con aseguradora, cliente y juzgado; y el menú de
  Configuración confirma que aseguradoras y juzgados son catálogos aparte.
- Los contadores de colores (Pendientes / En curso / Cerrados) no son una
  tabla: son un **estado** dentro de la tabla expedientes, que luego se
  cuenta con `GROUP BY`.

## 2. Diseño relacional

- Usé **llaves foráneas** (`aseguradora_id`, `juzgado_id`) en vez de repetir
  el texto del nombre en cada expediente. Esto evita errores de escritura,
  ahorra espacio y permite cambiar un nombre en un solo lugar (normalización).
- El tipo `ENUM` sirve para restringir el estado a valores válidos y evitar
  datos sucios como "Pendiente", "PENDIENTE" o "pendinte".

## 3. Conexión Python ↔ MySQL

- El conector `mysql-connector-python` permite ejecutar SQL desde Python.
- Aprendí a usar **consultas parametrizadas** (`%s`) en lugar de concatenar
  texto, lo que protege contra inyección SQL.
- `cursor(dictionary=True)` devuelve los resultados como diccionarios, lo que
  facilita convertirlos a JSON con `jsonify`.
- Es importante **cerrar la conexión** (`db.close()`) después de cada consulta.

## 4. API REST con Flask

- Cada **método HTTP** tiene un significado: GET lee, POST crea, PUT
  actualiza y DELETE elimina. La misma ruta `/api/expedientes` cambia de
  comportamiento según el método.
- Los **códigos de estado** comunican el resultado: 200 (OK), 201 (creado),
  400 (petición mal formada), 401 (no autorizado), 404 (no encontrado),
  409 (conflicto/duplicado).
- La API devuelve **JSON**, no HTML: el frontend (el prototipo) consumiría
  estos datos para pintar la pantalla.

## 5. Seguridad

- Las contraseñas **nunca se guardan en texto plano**: se usa
  `generate_password_hash` al crear el usuario y `check_password_hash` al
  hacer login. Ni siquiera el administrador de la base de datos puede ver
  la contraseña real.

## 6. Dificultades encontradas (completa con las tuyas)

- [ ] Ejemplo: error de conexión a MySQL por contraseña incorrecta → lo
      resolví verificando las credenciales en `get_db()`.
- [ ] Ejemplo: `ModuleNotFoundError: flask` → me faltaba activar el entorno
      virtual antes de instalar.
- [ ] ...

## 7. Mejoras futuras

- Agregar autenticación con tokens (JWT) para proteger los endpoints.
- Filtrar la agenda por fecha (`/api/expedientes?fecha=2019-01-07`).
- Construir el frontend que consuma la API y reproduzca el prototipo.
- Recuperación de contraseña (enlace "Olvidaste tu contraseña").
