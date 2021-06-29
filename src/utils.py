import os
import json
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.getcwd() + 'upload'
ALLOWED_EXTENSIONS = {'xlsm', 'xlsx'}


def getGoogleCredentials():
    PROJECT_ID = os.environ.get("PROJECT_ID")
    PRIVATE_KEY_ID = os.environ.get("PRIVATE_KEY_ID")
    PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
    CLIENT_EMAIL = os.environ.get("CLIENT_EMAIL")
    CLIENT_ID = os.environ.get("CLIENT_ID")

    with open(os.getcwd() + '/credentials/sgdkeybigquery.json', 'r') as f:
        credenciais = json.load(f)

    credenciais["project_id"] = PROJECT_ID
    credenciais["private_key_id"] = PRIVATE_KEY_ID
    credenciais["private_key"] = PRIVATE_KEY
    credenciais["client_email"] = CLIENT_EMAIL
    credenciais["client_id"] = CLIENT_ID

    return credenciais


def validateFileReq(request):
    # check if the post request has the file part
    if 'file' not in request.files:
        return {"message": "Arquivo não encontrado"}
    file = request.files['file']
    if file.filename == '':
        return {"message": "Arquivo é obrigatório"}
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join("upload", filename))
        path = os.getcwd() + '/upload/' + filename
        return {"message": "Arquivo salvo", "path": path}
    else:
        return {"message": "O formato de arquivo enviado não é permitido, apenas extensões .xlsm, .xlsx"}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
