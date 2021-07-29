import os
from flask import Flask,  request,  render_template, flash
from src.tratar_dados import getProjetosEmExecucaoHTML, getProjetosPriorizadosJSON, getProjetosEmDiagnosticoHTML, getTotaisProjetosPriorizados
from src.excel_to_db import kpisToDB, startupsToDB, projetosToDB, alocacoesToDB
from src.utils import validateFileReq
import config

UPLOAD_FOLDER = os.getcwd() + 'upload'
SENHA_UPLOAD = os.environ['SENHA_UPLOAD']

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


@app.route('/upload-indicadores', methods=['POST'])
def upload_indicadores():
    if request.method == 'POST':
        print(request.form.get("senha"))
        if request.form.get('senha') != SENHA_UPLOAD:
            flash(
                'Senha inválida, não será possível carregar os Dados dos Indicadores.', category='error')
            return render_template('upload_form.html')
        resp = validateFileReq(request)
        try:
            path = resp['path']
        except KeyError:
            flash('Arquivo é obrigatório', category='error')
            return render_template('upload_form.html')
            # return render_template('index.html', mensagem=resp['message'])
        # Validar se os campos checkbox estão marcados
        msgStartups = None
        msgKpis = None
        if request.form.get('carga_startups'):
            msgStartups = startupsToDB(path)
        if request.form.get('carga_kpis'):
            msgKpis = kpisToDB(path)

        if not msgKpis == None:
            if msgKpis == 'OK':
                flash('Dados dos Indicadores carregados com sucesso.',
                      category='success')
            else:
                flash(f'{msgKpis}', category='error')

        if not msgStartups == None:
            if msgStartups == 'OK':
                flash('Dados de Relato e Pontos de Atenção carregados com sucesso.',
                      category='success')
            else:
                flash(msgStartups, category='error')
        return render_template('upload_form.html')


@app.route('/upload-projetos', methods=['POST'])
def upload_projetos():
    if request.method == 'POST':
        if request.form.get('senha') != SENHA_UPLOAD:
            flash(
                'Senha inválida, não será possível carregar os Dados dos Projetos.', category='error')
            return render_template('upload_form.html')

        resp = validateFileReq(request)
        try:
            path = resp['path']
        except KeyError:
            flash('Arquivo é obrigatório', category='error')
            return render_template('upload_form.html')

        msgProjetos = projetosToDB(path)

        if msgProjetos == 'OK':
            flash('Dados dos Projetos carregados com sucesso.',
                  category='success')
        else:
            flash(msgProjetos, category='error')

        return render_template('upload_form.html')


@app.route('/upload-alocacoes', methods=['POST'])
def upload_alocacoes():
    if request.method == 'POST':
        if request.form.get('senha') != SENHA_UPLOAD:
            flash(
                'Senha inválida, não será possível carregar os Dados de Alocação dos Servidores.', category='error')
            return render_template('upload_form.html')

        resp = validateFileReq(request)
        try:
            path = resp['path']
        except KeyError:
            flash('Arquivo é obrigatório', category='error')
            return render_template('upload_form.html')

        msgAlocacoes = alocacoesToDB(path)

        if msgAlocacoes == 'OK':
            flash('Dados das Alocações carregadas com sucesso.',
                  category='success')
        else:
            flash(msgAlocacoes, category='error')

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
