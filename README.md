# Taller Práctico — Sistema de Gestión de Expedientes

API REST desarrollada con **Python + Flask + MySQL**, basada en un prototipo
de sistema para bufete de abogados (login, agenda del día, dashboard de
expedientes por estado).

## Estructura del proyecto

```
taller-expedientes/
├── app.py                    # API REST (Flask)
├── schema.sql                # Esquema de la base de datos + datos de prueba
├── requirements.txt          # Dependencias de Python
├── LECCIONES_APRENDIDAS.md   # Documento de lecciones aprendidas
├── pruebas.http              # Pruebas de la API (extensión REST Client de VS Code)
└── README.md
```

## Requisitos

- Python 3.10 o superior
- MySQL Server 8.x
- Visual Studio Code (opcional: extensión **REST Client** para usar `pruebas.http`)

## Instalación paso a paso

### 1. Crear y activar el entorno virtual

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac / Linux:
source venv/bin/activate
```

### 2. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 3. Crear la base de datos

```bash
mysql -u root -p < schema.sql
```

(O abre `schema.sql` en MySQL Workbench y ejecútalo completo.)

### 4. Configurar la conexión

En `app.py`, dentro de la función `get_db()`, cambia
`password="TU_CLAVE_AQUI"` por tu contraseña de MySQL.

### 5. Ejecutar el servidor

```bash
python app.py
```

La API queda disponible en `http://127.0.0.1:5000`

## Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /api/usuarios | Crear usuario |
| POST | /api/login | Iniciar sesión |
| GET | /api/expedientes | Listar expedientes (Agenda del día) |
| GET | /api/expedientes/&lt;id&gt; | Ver un expediente |
| POST | /api/expedientes | Crear expediente |
| PUT | /api/expedientes/&lt;id&gt; | Actualizar expediente |
| DELETE | /api/expedientes/&lt;id&gt; | Eliminar expediente |
| GET | /api/dashboard | Totales por estado (pendiente / en curso / cerrado) |
| GET | /api/aseguradoras | Listar aseguradoras |
| POST | /api/aseguradoras | Crear aseguradora |
| GET | /api/juzgados | Listar juzgados |
| POST | /api/juzgados | Crear juzgado |

## Pruebas rápidas con curl

```bash
# Listar expedientes
curl http://127.0.0.1:5000/api/expedientes

# Dashboard
curl http://127.0.0.1:5000/api/dashboard

# Crear usuario
curl -X POST http://127.0.0.1:5000/api/usuarios -H "Content-Type: application/json" -d "{\"nombre\":\"Juan Perez\",\"usuario\":\"jperez\",\"contrasena\":\"1234\"}"

# Login
curl -X POST http://127.0.0.1:5000/api/login -H "Content-Type: application/json" -d "{\"usuario\":\"jperez\",\"contrasena\":\"1234\"}"
```

También puedes abrir `pruebas.http` en VS Code (con la extensión REST Client)
y hacer clic en "Send Request" sobre cada prueba.

## Subir al repositorio

```bash
git init
git add .
git commit -m "Taller: API REST de expedientes con Flask y MySQL"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/taller-expedientes.git
git push -u origin main
```
