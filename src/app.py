from crypt import methods
from flask import Flask,jsonify
from flaskext.mysql import MySQL
import pymysql

db = pymysql.connect(
    host='localhost',
    user='root',
    password='12345678',
    db='google_drive'
)

app =Flask(__name__)

@app.route('/')
def index():
    return "Hola mundo probando"

def pageNotFound(error):
    return "<h1>La pagina que intentas buscar no existe...</h1>"


@app.route('/getUserFiles',methods=['GET'])
def getUserFiles():
    try:
        sql = "SELECT * from User_Drive"
        cursor = db.cursor()
        cursor.execute(sql)
        datos=cursor.fetchall()
        user_files = []
        for item in datos:
            userFile = {"id_file":item[0],"file_name":item[1],"file_extension":item[2], "file_owner":item[3], "file_visibility":item[4],"file_lastModified":item[5]}
            user_files.append(userFile)
        return jsonify({"userFiles":user_files, "message":"User files showed"})
    except Exception as ex:
        return jsonify({"message":"Error"})


if __name__ == '__main__':
    app.register_error_handler(404, pageNotFound)
    app.run(debug=True) ## Le pongo el debug true para que refleje los cambios en tiempo real


