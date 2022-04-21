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