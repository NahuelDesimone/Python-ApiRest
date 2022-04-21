from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

credentials_file = 'credentials_module.json'

def login(): ##La funcion login retorna una instancia del objeto google drive ya autenticado
    googleAuth = GoogleAuth()
    googleAuth.LoadCredentialsFile(credentials_file)

    if (googleAuth.access_token_expired): ##Si el token expira se refresca y genera uno nuevo
        googleAuth.Refresh()
        googleAuth.SaveCredentialsFile(credentials_file)
    else:
        googleAuth.Authorize()

    return GoogleDrive(googleAuth)

def createFile(fileName, fileContent, parentFolderId):
    credentials = login()
    newFile = credentials.CreateFile({'title': fileName, 'parents': [{'kind': 'drive#fileLink', 'id': parentFolderId}]})
    newFile.SetContentString(fileContent)
    newFile.Upload()

def uploadFile(filePath, parentFolderId):
    credentials = login()
    newFile = credentials.CreateFile({'parents': [{'kind': 'drive#fileLink', 'id': parentFolderId}]})
    newFile['title'] = filePath.split('/')[-1]
    newFile.SetContentFile(filePath)
    newFile.Upload()


if __name__ == "__main__":
    #createFile('HolaDrive.txt', "Contenido de archivo de prueba",'1pz-AG8QOp0HlXjqnoDmNO0s-tPUR1egG')
    uploadFile('/Users/nahueldesimone/Downloads/English CV - Nahuel Desimone.pdf', '1pz-AG8QOp0HlXjqnoDmNO0s-tPUR1egG')