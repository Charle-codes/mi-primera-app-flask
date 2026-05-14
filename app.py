from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/saludo', methods=['GET', 'POST'])
def saludo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo'] # Capturamos el nuevo campo
        return f"Gracias {nombre}, hemos registrado tu correo: {correo}"
    return render_template('saludo.html')

if __name__ == '__main__':
    app.run(debug=True)
