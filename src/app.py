from crypt import methods
import json
from flask import Flask,jsonify, render_template, request
from flaskext.mysql import MySQL
from datetime import datetime, date
from numpy import datetime64
import pymysql

def connectDatabase():
    return pymysql.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='google_drive'
)

app =Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def pageNotFound(error):
    return render_template('pageNotFound.html'),404

@app.route('/changePublicFilesVisibility', methods=['POST'])
def changePublicFilesVisibility():

    try:
        acum = 0
        db = connectDatabase()
        cursor = db.cursor()
        jsonUserFiles = getUserFiles().json
        for usrFile in jsonUserFiles['userFiles']:
            updatedUserFile = usrFile
            if (usrFile['file_visibility'] == "Public"):
                updatedUserFile['file_visibility'] = "Private"
                dateTimeFormat = datetime.strptime(updatedUserFile['file_lastModified'], "%a, %d %b %Y %H:%M:%S %Z")
                updatedLastModified = dateTimeFormat.date()
                sql = """UPDATE User_Drive SET id_file={0}, file_name='{1}', file_extension='{2}', file_owner='{3}', file_visibility='{4}', file_lastModified='{5}' WHERE id_file = {0}""".format(
                updatedUserFile['id_file'],updatedUserFile['file_name'], updatedUserFile['file_extension'], updatedUserFile['file_owner'], updatedUserFile['file_visibility'], updatedLastModified)
                cursor.execute(sql)
                db.commit()
                sendEmail(updatedUserFile['file_owner'])
                acum = acum + 1
        
        if (acum > 0):
            return "Se modifico la visibilidad de {0} archivos que eran publicos".format(acum)
        
        else:
            return "Todos los archivos del usuario son privados"

        

    except Exception as ex:
        return "Error"

def sendEmail(fileOwner):
    print("Email sended to ", fileOwner)


@app.route('/getUserFiles',methods=['GET'])
def getUserFiles():
    try:
        sql = "SELECT * from User_Drive"
        db = connectDatabase()
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

@app.route('/getUserFile/<idFile>', methods=['GET'])
def getUserFile(idFile):
    try:
        db = connectDatabase()
        cursor = db.cursor()
        sql = "SELECT * FROM User_Drive WHERE id_file = '{0}'".format(idFile)
        cursor.execute(sql)
        data = cursor.fetchone()
        if data != None:
            userFile = {"id_file":data[0],"file_name":data[1],"file_extension":data[2], "file_owner":data[3], "file_visibility":data[4],"file_lastModified":data[5]}
            return userFile
        else:
            return None

    except Exception as ex:
        return ex

@app.route('/newUserFile',methods=['POST'])
def newUserFile():
    try:
        id_file = request.form["id_file"]
        file_name = request.form["file_name"]
        file_extension = request.form["file_extension"]
        file_owner = request.form["file_owner"]
        file_visibility = request.form["file_visibility"]
        file_lastModified = request.form["file_lastModified"]
        newUserFile = {
            "id_file": int(id_file),
            "file_name": file_name,
            "file_extension": file_extension,
            "file_owner": file_owner,
            "file_visibility": file_visibility,
            "file_lastModified": file_lastModified
        }
        userFileExists = getUserFile(id_file)
        if (userFileExists == None):
            db = connectDatabase()
            cursor = db.cursor()
            sql = """INSERT INTO User_Drive (id_file,file_name,file_extension,file_owner,file_visibility,file_lastModified) VALUES ({0},'{1}','{2}','{3}','{4}','{5}')""".format(newUserFile['id_file'],
            newUserFile['file_name'], newUserFile['file_extension'],
            newUserFile['file_owner'], newUserFile['file_visibility'],newUserFile['file_lastModified'])
            cursor.execute(sql)
            db.commit() ##Confirmo la accion de insertar un nuevo archivo
            return jsonify({"message":"User file created"})
        else:
            return jsonify({"message": "Error, input user file already exists"})

    except Exception as ex:
        return jsonify({"message":"Error"})

@app.route('/panel',methods=['POST'])
def panel():
    try:
        db = pymysql.connect(
        host='localhost',
        user='root',
        password='12345678'
        )
        cursor = db.cursor()
        sqlCreateDB = "CREATE SCHEMA `google_drive` ;"
        cursor.execute(sqlCreateDB)
        sqlCreateTable = """CREATE TABLE `google_drive`.`User_Drive` (
`id_file` INT NOT NULL,
`file_name` VARCHAR(45) NOT NULL,
`file_extension` VARCHAR(6) NULL,
`file_owner` VARCHAR(45) NOT NULL,
`file_visibility` VARCHAR(10) NOT NULL,
`file_lastModified` DATE NOT NULL,
PRIMARY KEY (`id_file`),
UNIQUE INDEX `id_file_UNIQUE` (`id_file` ASC) VISIBLE);"""
        cursor.execute(sqlCreateTable)
        return render_template('panel.html')

    except Exception as ex:
        return "<h3>Error al crear la base de datos</h3>"


@app.route('/deleteUserFile/<idFile>',methods=['DELETE'])
def deleteUserFile(idFile):
    try:
        cursor = db.cursor()
        sql = "DELETE FROM User_Drive WHERE id_file = '{0}'".format(idFile)
        cursor.execute(sql)
        return jsonify({"message":"User file deleted"})

    except Exception as ex:
        return jsonify({"message":"Error"})

@app.route('/updateUserFile',methods=['PUT'])
def updateUserFile():
    try:
        id_file = request.form["id_file"]
        fileToUpdate = getUserFile(id_file)
        print(fileToUpdate)
        # input_file_name = request.form["file_name"]
        # input_file_extension = request.form["file_extension"]
        # input_file_owner = request.form["file_owner"]
        # input_file_visibility = request.form["file_visibility"]
        # input_file_lastModified = request.form["file_lastModified"]
        # updatedUserFile = {
        #     "id_file": int(id_file),
        #     "file_name": file_name,
        #     "file_extension": file_extension,
        #     "file_owner": file_owner,
        #     "file_visibility": file_visibility,
        #     "file_lastModified": file_lastModified
        # }
        # db = connectDatabase()
        # cursor = db.cursor()
        # sql = """UPDATE User_Drive SET id_file={0}, file_name='{1}', file_extension='{2}', file_owner='{3}', file_visibility='{4}', file_lastModified='{5}' WHERE id_file = {6}""".format(
        #     idFile,updatedUserFile['file_name'], updatedUserFile['file_extension'], updatedUserFile['file_owner'], updatedUserFile['file_visibility'], updatedUserFile['file_lastModified'],idFile
        # )
        # cursor.execute(sql)
        # db.commit() ##Confirmo la accion de insertar un nuevo archivo
        return jsonify({"message":"User file updated"})

    except Exception as ex:
        return jsonify({"message":"Error"}) 

if __name__ == '__main__':
    app.register_error_handler(404, pageNotFound)
    app.run(debug=True) ## Le pongo el debug true para que refleje los cambios en tiempo real


