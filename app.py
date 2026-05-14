from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/saludo', methods=['GET', 'POST'])
def saludo():

    if request.method == 'POST':

        nombre = request.form['nombre']

        return f"Hola {nombre}"

    return render_template('saludo.html')

if __name__ == '__main__':
    app.run(debug=True)