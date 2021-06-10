import os
import time
from flask import Flask, flash, request, redirect, url_for, abort, render_template
from werkzeug.utils import secure_filename
from src.tratar_dados import getProjetosEmExecucaoHTML, getProjetosPriorizadosJSON, getProjetosEmDiagnosticoHTML

UPLOAD_FOLDER = os.getcwd() + 'upload'
ALLOWED_EXTENSIONS = {'xlsm', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app = Flask("Projeto")


@app.route('/')
def index():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/dashboard', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            abort(400, "file no in request.files")
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            abort(400, "filename em branco")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("upload", filename))
        else:
            abort(400, "arquivo nao permitido")

    path = os.getcwd() + '\\upload\\' + filename
    #"D:\\Patrick\\Ministerio Economia\\Projeto Situacao Startups\\upload\\" + filename
    projetosJson = getProjetosPriorizadosJSON(path)
    print(type(projetosJson[0]['status']))
    html_emExecucao = getProjetosEmExecucaoHTML(path)
    html_emDiagnostico = getProjetosEmDiagnosticoHTML(path)
    dataModificacao = time.strftime(
        '%d/%m/%Y', time.localtime(os.path.getmtime(path)))
    # print(dataDF.head())
    return render_template('dashboard.html', projetos=projetosJson, execucao=html_emExecucao, diagnostico=html_emDiagnostico, dataModificacao=dataModificacao)


app.run(debug=True)
