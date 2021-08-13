import os
from flask import Flask,  request,  render_template, flash
from src.tratar_dados import getProjetosEmExecucaoHTML, getProjetosPriorizadosJSON, getProjetosEmDiagnosticoHTML, getTotaisProjetosPriorizados
from src.excel_to_db import kpisToDB, relatoPontosAtencaoToDB, projetosToDB, alocacoesToDB
from src.utils import validateFileReq
from config import getUploadPass

UPLOAD_FOLDER = os.getcwd() + 'upload'
SENHA_UPLOAD = getUploadPass()

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
            msgStartups = relatoPontosAtencaoToDB(path)
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
        msgProjetos = None
        msgAlocacoes = None

        if request.form.get('carga_projetos'):
            msgProjetos = projetosToDB(path)
        if request.form.get('carga_alocacoes'):
            msgAlocacoes = alocacoesToDB(path)

        if not msgProjetos == None:
            if msgProjetos == 'OK':
                flash('Dados dos Projetos carregados com sucesso.',
                      category='success')
            else:
                flash(msgProjetos, category='error')

        if not msgAlocacoes == None:
            if msgAlocacoes == 'OK':
                flash('Dados das Alocações carregadas com sucesso.',
                      category='success')
            else:
                flash(msgAlocacoes, category='error')

        return render_template('upload_form.html')


if __name__ == "__main__":
    app.run(port=33507)
