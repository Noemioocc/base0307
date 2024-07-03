from flask import Flask, render_template, request, redirect, url_for, flash # type: ignore
from flask_mysqldb import MySQL # type: ignore
from datetime import datetime

app = Flask(__name__)

#My SQL Connection
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'repuestosdb'
mysql = MySQL(app) 

#Inicializar una sesion
app.secret_key = 'mysecretkey'

@app.route('/', methods=['GET','POST'])
def Index():
    #cur = mysql.connection.cursor()
    #cur.execute('SELECT * FROM usuariosvyv')
    #data = cur.fetchall()
    return render_template('index.html') 


@app.route('/bus', methods=['POST'])
def bus():
    if request.method == 'POST':
        accion1 = request.form['buscar']
        cate = request.form['categoria']
        marc = request.form['marca']
        marce = request.form['mimi']
        now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO accionesvyv (nombre, categoria, modelo, busqueda, hora) VALUES (%s, %s, %s, %s, %s)", (marce, cate, accion1, marc, now))
        mysql.connection.commit()
        cur.close()
    return render_template('index.html') 

@app.route('/bus2', methods=['POST'])
def bus2():
    if request.method == 'POST':
        accion2 = request.form['buscar_codigo']
        now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO accionesvyv (nombre, busqueda, hora) VALUES (%s, %s, %s)", (accion2, accion2, now))
        mysql.connection.commit()
        cur.close()
    return render_template('index.html') 

@app.route('/bus3', methods=['POST'])
def bus3():
    if request.method == 'POST':
        buse = request.form['buscar']
        cur = mysql.connection.cursor()
        #cur.execute("SELECT * FROM repuestosvyv WHERE descripcion = '%s'" % (buse))
        #cur.execute("SELECT * FROM repuestosvyv WHERE descripcion = %s", (buse))
        cur.execute("SELECT * FROM repuestosvyv WHERE descripcion LIKE %s", ("%" + buse + "%",))      
        mysql.connection.commit()
        resultadoBusqueda = cur.fetchall()  
    return resultadoBusqueda 

@app.route('/buscar_usuario', methods=['GET','POST'])
def buscar_usuario():
    if request.method   == "POST":
        usuariovalidacion = request.form['usuario']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuariosvyv WHERE nombre = '%s'" % (usuariovalidacion))
        resultadoBusqueda = cur.fetchall()  
        mysql.connection.commit()
        if resultadoBusqueda:
            return render_template('index.html', usu = usuariovalidacion)
        else:
            flash('El USUARIO NO EXISTE')

        # Si el usuario no existe
            return redirect(url_for('Index'))    
    

@app.route('/principal')
def principal():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM repuestosvyv')
    data = cur.fetchall()
    return render_template('index.html', repuestosvyv = data) 


@app.route('/secundario', methods=['GET','POST'])
def secundario():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM accionesvyv ORDER BY hora DESC')
    data = cur.fetchall()
    return render_template('ver-acciones.html', miDatas = data) 

@app.route('/tercer', methods=['POST'])
def tercer():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM accionesvyv ORDER BY hora DESC')
    data = cur.fetchall()
    return render_template('add-repuesto.html', miDatas = data)     

@app.route('/buscar_repuesto', methods=['GET','POST'])
def buscar_repuesto():
    if request.method   == "POST":
        search = request.form['buscar']
        cat = request.form['categoria']
        mar = request.form['marca']      
        cur = mysql.connection.cursor() 
        #cur.execute("SELECT * FROM repuestosvyv WHERE serie = '%s' ORDER BY id  DESC" % (search))
        #cur.execute("SELECT * FROM repuestosvyv WHERE serie LIKE %s", ("%" + search + "%",))
        cur.execute("SELECT * FROM repuestosvyv WHERE categoria LIKE %s AND serie LIKE %s AND marca LIKE %s", ("%" + cat + "%", "%" + search + "%", "%" + mar + "%"))
        bus()
        resultadoBusqueda = cur.fetchall()  
        now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        mysql.connection.commit()
        if resultadoBusqueda:
            return render_template('index.html', miData = resultadoBusqueda)
        else:        
            nuevosResultados = bus3()
            return render_template('index.html', miData = nuevosResultados)
    
@app.route('/buscar_codigo', methods = ['GET','POST'])    
def buscar_codigo():
    if request.method == "POST":
        codigo = request.form['buscar_codigo']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM repuestosvyv WHERE codigo LIKE %s", ("%" + codigo + "%",))
        resultadoBusqueda = cur.fetchall()  
        bus2()
        now = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        mysql.connection.commit()
        if resultadoBusqueda:
            #print('Se encontro la busqueda')
            return render_template('index.html', miData = resultadoBusqueda)
        else:
            return render_template('index.html', miData = resultadoBusqueda)
    

@app.route('/add_repuesto', methods = ['POST'])
def add_repuesto():
    if request.method == 'POST':
        categoria = request.form['categoria']
        codigo = request.form['codigo']
        descripcion = request.form['descripcion']
        marca = request.form['marca']
        modelo = request.form['modelo']
        serie = request.form['serie']
        link = request.form['link']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO repuestosvyv (categoria, codigo, descripcion, marca, modelo, serie, link) VALUES (%s, %s, %s, %s, %s, %s, %s)',(categoria, codigo, descripcion, marca, modelo, serie, link))
        mysql.connection.commit()
        flash('Repuesto AGREGADO')
        #return redirect(url_for('principal'))
        return render_template('index.html')


@app.route('/edit/<id>')
def get_repuestovyv(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM repuestosvyv WHERE id = %s', [id])
    data = cur.fetchall()
    return render_template('edit-repuesto.html', repuestovyv = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        categoria = request.form['categoria']
        codigo = request.form['codigo']
        descripcion = request.form['descripcion']
        marca = request.form['marca']
        modelo = request.form['modelo']
        serie = request.form['serie']
        link = request.form['link']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE repuestosvyv
            SET categoria = %s,
                codigo = %s,
                descripcion = %s, 
                marca = %s,
                modelo = %s,
                serie = %s,
                link = %s
            WHERE id = %s                                   
        """, (categoria, codigo, descripcion, marca, modelo, serie, link, id))
        mysql.connection.commit()
        flash('Repuesto ACTUALIZADO')
        #return redirect(url_for('principal'))
        return render_template('index.html')



@app.route('/delete/<string:id>')
def delete_repuesto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM repuestosvyv WHERE id= {0}'.format(id))
    mysql.connection.commit()
    flash('Repuesto ELIMINADO correctamente')
    #return redirect(url_for('principal'))
    return render_template('index.html')

"""@app.route('/add_acciones', methods = ['POST'])
def add_acciones():
    if request.method == 'POST':
        usuario = request.form['usuario']
        accion = request.form['accion']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO accionesvyv (usuario, accion) VALUES (%s, %s)',(usuario, accion))
        print('ESTOY AQUI')
        mysql.connection.commit()
        flash('Repuesto AGREGADO')
        #return redirect(url_for('principal'))
        return render_template('consultas-repuestos.html')
"""


if __name__ == '__main__':
    app.run(port = 3000, debug = True)