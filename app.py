from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3
import os

app=Flask(__name__)
app.secret_key='tu_clave_secreta'

DATABASE=os.path.join('database','productos.db')

def get_connection_db():
    conn=sqlite3.connect(DATABASE)
    conn.row_factory=sqlite3.Row
    return conn

def init_db():
    if not os.path.exists('database'):
        os.makedirs('database')
    conn=get_connection_db()
    conn.execute('''
            CREATE TABLE IF NOT EXISTS productos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(30),
                precio REAL,
                stock INTEGER DEFAULT 0
            )
                 ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn=get_connection_db()
    productos=conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('index.html',productos=productos)

@app.route('/nuevo', methods=['GET','POST'])
def nuevo():
    if request.method=='POST':
        nombre=request.form['nombre']
        precio=float(request.form['precio'])
        stock=int(request.form['stock'] or 0)
        
        conn=get_connection_db()
        conn.execute('INSERT INTO productos (nombre,precio,stock) VALUES(?,?,?)',(nombre,precio,stock))
        conn.commit()
        conn.close()
        
        flash('Producto añadido correctamente!')
        return redirect(url_for('index'))
    
    return render_template('nuevo.html')

@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    conn=get_connection_db()
    producto=conn.execute('SELECT * FROM productos WHERE id=?',(id,)).fetchone()

    if request.method=='POST':
        nombre=request.form['nombre']
        precio=float(request.form['precio'])
        stock=int(request.form['stock'] or 0)
        
        conn.execute('UPDATE productos SET nombre=? , precio=?, stock=? WHERE id=?',(nombre,precio,stock,id))
        conn.commit()
        conn.close()
        
        flash('Producto actualizado correctamente!')
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('editar.html',producto=producto)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn=get_connection_db()
    conn.execute('DELETE FROM productos WHERE id=?',(id,))
    conn.commit()
    conn.close()
    flash('Producto eliminado correctamente!')
    return redirect(url_for('index'))

if __name__=="__main__":
    init_db()
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=10000)