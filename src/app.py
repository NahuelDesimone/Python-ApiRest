from flask import Flask

app =Flask(__name__)

@app.route('/')
def index():
    return "Hola mundo probando"

if __name__ == '__main__':
    app.run(debug=True) ## Le pongo el debug true para que refleje los cambios en tiempo real

