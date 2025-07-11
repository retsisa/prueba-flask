from flask import Flask,jsonify
from flask_cors import CORS
import sqlite3
import os

app=Flask(__name__)
CORS(app)

DB_PATH=os.path.join(os.path.dirname(__file__),'experimento.db')

def init_db():
    conn=sqlite3.connect(DB_PATH)
    c=conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS mensajes
                (id INTEGER PRIMARY KEY, texto TEXT)''')
    
    c.execute("INSERT OR IGNORE INTO mensajes(id,texto) VALUES (1,'Bienvenido a mi experimento!')")
    conn.commit()
    conn.close()
    
@app.route('/api/mensaje')
def get_mensaje():
    conn=sqlite3.connect(DB_PATH)
    c=conn.cursor()
    c.execute("SELECT texto FROM mensajes WHERE id=1")
    mensaje=c.fetchone()[0]
    conn.close()
    return jsonify({'mensaje':mensaje})

if __name__=='__main__':
    init_db()
    app.run(debug=True)