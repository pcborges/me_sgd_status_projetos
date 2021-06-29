import os
import json
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.getcwd() + 'upload'
ALLOWED_EXTENSIONS = {'xlsm', 'xlsx'}


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
