from flask import Flask, request, jsonify, render_template
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Blanco507",
        database="bufete_db"
    )

@app.route("/")
def pantalla_login():
    return render_template("login.html")



@app.route("/dashboard")
def pantalla_dashboard():
    return render_template("dashboard.html")


@app.route("/api/usuarios", methods=["POST"])
def crear_usuario():
    d = request.get_json()
    if not d or not all(k in d for k in ("nombre", "usuario", "contrasena")):
        return jsonify({"error": "Faltan datos: nombre, usuario, contrasena"}), 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, usuario, contrasena) VALUES (%s, %s, %s)",
            (d["nombre"], d["usuario"], generate_password_hash(d["contrasena"]))
        )
        db.commit()
        return jsonify({"mensaje": "Usuario creado correctamente"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Ese nombre de usuario ya existe"}), 409
    finally:
        db.close()


@app.route("/api/login", methods=["POST"])
def login():
    d = request.get_json()
    if not d or "usuario" not in d or "contrasena" not in d:
        return jsonify({"error": "Debe enviar usuario y contrasena"}), 400

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (d["usuario"],))
    user = cursor.fetchone()
    db.close()

    if user and check_password_hash(user["contrasena"], d["contrasena"]):
        return jsonify({"mensaje": "Bienvenido", "nombre": user["nombre"]}), 200
    return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route("/api/expedientes", methods=["GET"])
def listar_expedientes():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.id,
               e.cliente,
               a.nombre AS aseguradora,
               j.nombre AS juzgado,
               e.estado,
               e.fecha_audiencia
        FROM expedientes e
        JOIN aseguradoras a ON e.aseguradora_id = a.id
        JOIN juzgados j     ON e.juzgado_id = j.id
        ORDER BY e.fecha_audiencia
    """)
    resultado = cursor.fetchall()
    db.close()
    return jsonify(resultado), 200


@app.route("/api/expedientes/<int:id>", methods=["GET"])
def ver_expediente(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT e.id, e.cliente, a.nombre AS aseguradora,
               j.nombre AS juzgado, e.estado, e.fecha_audiencia
        FROM expedientes e
        JOIN aseguradoras a ON e.aseguradora_id = a.id
        JOIN juzgados j     ON e.juzgado_id = j.id
        WHERE e.id = %s
    """, (id,))
    exp = cursor.fetchone()
    db.close()
    if exp:
        return jsonify(exp), 200
    return jsonify({"error": "Expediente no encontrado"}), 404


@app.route("/api/expedientes", methods=["POST"])
def crear_expediente():
    d = request.get_json()
    if not d or not all(k in d for k in ("cliente", "aseguradora_id", "juzgado_id")):
        return jsonify({"error": "Faltan datos: cliente, aseguradora_id, juzgado_id"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO expedientes (cliente, aseguradora_id, juzgado_id, estado, fecha_audiencia)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        d["cliente"],
        d["aseguradora_id"],
        d["juzgado_id"],
        d.get("estado", "pendiente"),
        d.get("fecha_audiencia")
    ))
    db.commit()
    nuevo_id = cursor.lastrowid
    db.close()
    return jsonify({"mensaje": "Expediente creado", "id": nuevo_id}), 201


@app.route("/api/expedientes/<int:id>", methods=["PUT"])
def actualizar_expediente(id):
    d = request.get_json()
    if not d:
        return jsonify({"error": "Debe enviar datos para actualizar"}), 400

    campos = []
    valores = []
    for campo in ("cliente", "aseguradora_id", "juzgado_id", "estado", "fecha_audiencia"):
        if campo in d:
            campos.append(f"{campo} = %s")
            valores.append(d[campo])

    if not campos:
        return jsonify({"error": "Ningún campo válido para actualizar"}), 400

    valores.append(id)
    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"UPDATE expedientes SET {', '.join(campos)} WHERE id = %s", valores)
    db.commit()
    filas = cursor.rowcount
    db.close()

    if filas == 0:
        return jsonify({"error": "Expediente no encontrado"}), 404
    return jsonify({"mensaje": "Expediente actualizado"}), 200


@app.route("/api/expedientes/<int:id>", methods=["DELETE"])
def eliminar_expediente(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM expedientes WHERE id = %s", (id,))
    db.commit()
    filas = cursor.rowcount
    db.close()

    if filas == 0:
        return jsonify({"error": "Expediente no encontrado"}), 404
    return jsonify({"mensaje": "Expediente eliminado"}), 200

@app.route("/api/dashboard", methods=["GET"])
def dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT estado, COUNT(*) AS total FROM expedientes GROUP BY estado")
    resultado = cursor.fetchall()
    db.close()
    return jsonify(resultado), 200

@app.route("/api/aseguradoras", methods=["GET"])
def listar_aseguradoras():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM aseguradoras ORDER BY nombre")
    resultado = cursor.fetchall()
    db.close()
    return jsonify(resultado), 200


@app.route("/api/aseguradoras", methods=["POST"])
def crear_aseguradora():
    d = request.get_json()
    if not d or "nombre" not in d:
        return jsonify({"error": "Debe enviar el nombre"}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO aseguradoras (nombre) VALUES (%s)", (d["nombre"],))
    db.commit()
    db.close()
    return jsonify({"mensaje": "Aseguradora creada"}), 201


@app.route("/api/juzgados", methods=["GET"])
def listar_juzgados():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM juzgados ORDER BY nombre")
    resultado = cursor.fetchall()
    db.close()
    return jsonify(resultado), 200


@app.route("/api/juzgados", methods=["POST"])
def crear_juzgado():
    d = request.get_json()
    if not d or "nombre" not in d:
        return jsonify({"error": "Debe enviar el nombre"}), 400
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO juzgados (nombre) VALUES (%s)", (d["nombre"],))
    db.commit()
    db.close()
    return jsonify({"mensaje": "Juzgado creado"}), 201


if __name__ == "__main__":
    app.run(debug=True)
