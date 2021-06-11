import os
import time
from flask import Flask, flash, request, redirect, url_for, abort, render_template
from werkzeug.utils import secure_filename
from src.tratar_dados import getProjetosEmExecucaoHTML, getProjetosPriorizadosJSON, getProjetosEmDiagnosticoHTML

UPLOAD_FOLDER = os.getcwd() + 'upload'
ALLOWED_EXTENSIONS = {'xlsm', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
            mensagemErro = "Arquivo é obrigatório."
            return render_template('index.html', mensagem=mensagemErro)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join("upload", filename))
        else:
            mensagemErro = "O formato de arquivo enviado não é permitido, apenas extensões .xlsm, .xlsx"
            return render_template('index.html', mensagem=mensagemErro)

    path = os.getcwd() + '/upload/' + filename
    mesAnoReferencia = int(request.form.get('mes_ano'))
    request.form.getlist('mes_ano')
    #"D:\\Patrick\\Ministerio Economia\\Projeto Situacao Startups\\upload\\" + filename
    try:
        projetosJson = getProjetosPriorizadosJSON(path)
        html_emExecucao = getProjetosEmExecucaoHTML(path, mesAnoReferencia)
        html_emDiagnostico = getProjetosEmDiagnosticoHTML(
            path, mesAnoReferencia)
    except:
        mensagemErro = "Houve algum erro no processamento do arquivo, certifique-se de que o arquivo enviado está no padrão necessário."
        return render_template('index.html', mensagem=mensagemErro)

    if mesAnoReferencia == 14:
        periodoReferencia = '03/2021'
    elif mesAnoReferencia == 15:
        periodoReferencia = '04/2021'
    else:
        periodoReferencia = '05/2021'

    return render_template('dashboard.html', projetos=projetosJson, execucao=html_emExecucao, diagnostico=html_emDiagnostico, periodoReferencia=periodoReferencia)


if __name__ == "__main__":
    app.run(debug=True, port=33507)
