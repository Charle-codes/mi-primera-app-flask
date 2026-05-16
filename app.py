from flask import Flask, render_template, request
import os
import psycopg2

# 1. Primero creamos la aplicación Flask
app = Flask(__name__)

# 2. Definimos la función para conectar a la base de datos
def conectar_db():
    url = os.environ.get('DB_URL')
    return psycopg2.connect(url)
# --- TRUCO AUTOMÁTICO: Este bloque mantendrá tu tabla segura ---
try:
    conn = conectar_db()
    cur = conn.cursor()
    
    # Ya NO borramos la tabla. Solo verificamos que exista con UNIQUE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            correo VARCHAR(100) NOT NULL UNIQUE
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("¡Estructura de la tabla 'usuarios' verificada!")
except Exception as e:
    print(f"No se pudo verificar la estructura automáticamente: {e}"
# -----------------------------------------------------------


# 4. Ahora sí, ponemos todas las rutas juntas usando @app.route

# Ruta 1: El formulario principal (Raíz)
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
            
            return render_template('exito.html', nombre=nombre, correo=correo)
            
        except psycopg2.errors.UniqueViolation:
            # Capturamos el error de duplicado de forma ultra segura
            if 'conn' in locals() and conn:
                conn.rollback()
            if 'cur' in locals() and cur:
                cur.close()
            if 'conn' in locals() and conn:
                conn.close()
            
            return render_template('saludo.html', error="Este correo electrónico ya se encuentra registrado.")
            
        except Exception as e:
            return f"Hubo un error inesperado al guardar: {e}"

    return render_template('saludo.html')


# Ruta 2: La página "secreta" para ver los usuarios registrados
@app.route('/usuarios')
def ver_usuarios():
    try:
        conn = conectar_db()
        cur = conn.cursor()
        # Le pedimos a la base de datos todos los registros ordenados del más nuevo al más viejo
        cur.execute("SELECT id, nombre, correo FROM usuarios ORDER BY id DESC;")
        lista_usuarios = cur.fetchall() # Guarda los resultados en una lista
        cur.close()
        conn.close()
        
        # Le pasamos la lista a nuestro nuevo archivo HTML
        return render_template('lista.html', usuarios=lista_usuarios)
    except Exception as e:
        return f"Error al consultar la base de datos: {e}"


# 5. Por último, el bloque que enciende el servidor
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
