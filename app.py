from flask import Flask, render_template, request
import os
import psycopg2

app = Flask(__name__)

def conectar_db():
    url = os.environ.get('DB_URL')
    return psycopg2.connect(url)

# --- TRUCO AUTOMÁTICO: Este bloque creará la tabla por ti ---
try:
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            correo VARCHAR(100) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("¡Tabla 'usuarios' verificada o creada con éxito!")
except Exception as e:
    print(f"No se pudo crear la tabla automáticamente: {e}")
# -----------------------------------------------------------

# Esta es ahora tu única ruta principal
@app.route('/', methods=['GET', 'POST'])
def saludo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        
        try:
            conn = conectar_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO usuarios (nombre, correo) VALUES (%s, %s)", (nombre, correo))
            conn.commit()
            cur.close()
            conn.close()
            
            # PASO CLAVE: Aquí llamamos a la nueva pantalla y le pasamos las variables
            return render_template('exito.html', nombre=nombre, correo=correo)
            
        except Exception as e:
            return f"Hubo un error al guardar: {e}"

    return render_template('saludo.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
