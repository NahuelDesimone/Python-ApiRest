from numpy import intp
import mysql
import pymysql

db_name = input("Ingrese el nombre de la base de datos a crear: ")

def newDatabase(dbName):

    try:
        db = pymysql.connect(
        host='localhost',
        user='root',
        password='12345678'
        )
        cursor = db.cursor()
        sqlCreateDB = "CREATE SCHEMA `{0}`;".format(dbName)
        cursor.execute(sqlCreateDB)
        return "DB created succesfully"

    except Exception as ex:
        return "Error"

newDatabase(db_name)

