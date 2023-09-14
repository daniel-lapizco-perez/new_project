import psycopg2

from flask import Flask, render_template, request, url_for, redirect

from datetime import datetime, timezone

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

@app.route('/tickets')
def tickets():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tickets;')
    tickets = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('tickets.html', tickets=tickets)

@app.route('/create_ticket/', methods=('GET', 'POST'))
def create_ticket():
    if request.method == 'POST':
        titulo = request.form['titulo']
        departamento = request.form['departamento']
        status = request.form['status']
        #creacion = request.form['creacion']
        creacion = datetime.now (timezone.utc)
        #actualizacion = request.form['actualizacion']
        actualizacion = datetime.now (timezone.utc)
        #cierre = request.form['cierre']
        cierre = datetime.now (timezone.utc)
        tecnico = request.form['tecnico']
        created_by = request.form['created_by']
        descripcion = request.form['descripcion']
        porcentaje = request.form['porcentaje']

        conn = get_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO tickets (titulo, departamento, status, fecha_apertura, fecha_actualizacion, fecha_cierre, id_tecnico, created_by, descripcion, porcentaaje)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %i, %i, %s, %i)'
                    (titulo, departamento, status, creacion, actualizacion, cierre, tecnico, created_by, descripcion, porcentaje))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('tickets')
    return render_template('create_ticket.html')