import psycopg2

from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="proyecto",
        user='postgres',
        password='root'
    )

    return conn


@app.route('/')
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM empleados;')
    empleados = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', empleados=empleados)

@app.route('/create_empleado/', methods=('GET', 'POST'))
def create_empleado():

    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        departamento = request.form['departamento']
        rol = request.form['rol']

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO empleados (nombre, correo, departamento, rol)'
                    'VALUES (%s, %s, %s, %s)',
                    (nombre, correo, departamento, rol))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('empleados'))

    return render_template('create_empleado.html')