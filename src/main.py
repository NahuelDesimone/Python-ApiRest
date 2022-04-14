import json

def ingresarDatos():

    id_file = input("Ingrese el id del archivo: ")
    file_name = input("Ingrese el nombre del archivo: ")
    file_extension = input("Ingrese la extension del archivo: ")
    file_owner = input("Ingrese el propietario del archivo: ")
    file_visibility = input("Ingrese la visibilidad del archivo: ")
    file_lastModified = input("Ingrese la ultima modificacion del archivo: ")

    inputData = {
        "id_file":id_file,
        "file_name":file_name,
        "file_extension":file_extension,
        "file_owner":file_owner,
        "file_visibility":file_visibility,
        "file_lastModified":file_lastModified
    }

    return json.dumps(inputData)

data = ingresarDatos()
print(data)
