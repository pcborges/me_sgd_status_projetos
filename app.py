import os
from flask import Flask,  request,  render_template, flash
from src.tratar_dados import getProjetosEmExecucaoHTML, getProjetosPriorizadosJSON, getProjetosEmDiagnosticoHTML, getTotaisProjetosPriorizados
from src.excel_to_db import kpisToDB, startupsToDB
from src.utils import validateFileReq
import config

UPLOAD_FOLDER = os.getcwd() + 'upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "sgdapp"


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload')
def upload():
    return render_template('upload_form.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard_ds.html')


@app.route('/data-load', methods=['POST'])
def data_load():
    if request.method == 'POST':
        resp = validateFileReq(request)
        path = resp['path']
        if path == '':
            return render_template('index.html', mensagem=resp['message'])
        # Validar se os campos checkbox estão marcados
        msgStartups = None
        msgKpis = None
        if request.form.get('carga_startups'):
            msgStartups = startupsToDB(path)
        if request.form.get('carga_kpis'):
            msgKpis = kpisToDB(path)

        print(msgKpis, 'outra ', msgStartups)
        if not msgKpis == None:
            if msgKpis == 'OK':
                flash('Dados dos Indicadores carregados com sucesso.',
                      category='success')
            else:
                flash(msgKpis, category='error')

        if not msgStartups == None:
            if msgStartups == 'OK':
                flash('Dados das Startups carregados com sucesso.',
                      category='success')
            else:
                flash(msgStartups, category='error')
        return render_template('upload_form.html')


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
