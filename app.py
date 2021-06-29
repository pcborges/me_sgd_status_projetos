import os
from flask import Flask,  request,  render_template
from src.tratar_dados import getProjetosEmExecucaoHTML, getProjetosPriorizadosJSON, getProjetosEmDiagnosticoHTML, getTotaisProjetosPriorizados
from src.excel_to_db import uploadDataGBQ
from src.utils import validateFileReq
import config


UPLOAD_FOLDER = os.getcwd() + 'upload'
ALLOWED_EXTENSIONS = {'xlsm', 'xlsx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/carga')
def carga():
    return render_template('cargadados.html')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/bigquery', methods=['POST'])
def big_query():
    if request.method == 'POST':
        resp = validateFileReq(request)
        path = resp['path']
        if path == '':
            return render_template('index.html', mensagem=resp['message'])
    processamento = uploadDataGBQ(path)
    if processamento == 'OK':
        return render_template('cargadados.html', sucesso='Dados carregados com sucesso!')
    else:
        return render_template('cargadados.html', erro=processamento)


@app.route('/dashboard', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        resp = validateFileReq(request)
        path = resp['path']
        if path == '':
            return render_template('index.html', mensagem=resp['message'])

    mesAnoReferencia = int(request.form.get('mes_ano'))
    request.form.getlist('mes_ano')

    try:
        projetosJson = getProjetosPriorizadosJSON(path)
        html_emExecucao = getProjetosEmExecucaoHTML(path, mesAnoReferencia)
        html_emDiagnostico = getProjetosEmDiagnosticoHTML(
            path, mesAnoReferencia)
        totais = getTotaisProjetosPriorizados(projetosJson)
    except:
        mensagemErro = "Houve algum erro no processamento do arquivo, certifique-se de que o arquivo enviado está no padrão necessário."
        return render_template('index.html', mensagem=mensagemErro)

    if mesAnoReferencia == 14:
        periodoReferencia = '03/2021'
    elif mesAnoReferencia == 15:
        periodoReferencia = '04/2021'
    else:
        periodoReferencia = '05/2021'
    return render_template('dashboard.html', projetos=projetosJson, execucao=html_emExecucao, diagnostico=html_emDiagnostico, periodoReferencia=periodoReferencia, totais=totais)


if __name__ == "__main__":
    app.run(port=33507)
