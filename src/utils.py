import os
from werkzeug.utils import secure_filename
from datetime import datetime

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

# Funcao que recebe um dataframe, calcula e separa os kpis por periodo e retorna um dataframe com os dados


def separarKPIs(dataframe):
    # Salvar períodos dos indicadores em formato DateTime
    periodoDate = ['01/01/21 10:00:00', '01/02/21 10:00:00', '01/03/21 10:00:00', '01/04/21 10:00:00', '01/05/21 10:00:00', '01/06/21 10:00:00',
                   '01/07/21 10:00:00', '01/08/21 10:00:00', '01/09/21 10:00:00', '01/10/21 10:00:00', '01/11/21 10:00:00', '01/12/21 10:00:00', '01/01/22 10:00:00',
                   '01/02/22 10:00:00', '01/03/22 10:00:00', '01/04/22 10:00:00', '01/05/22 10:00:00', '01/06/22 10:00:00', '01/07/22 10:00:00',
                   '01/08/22 10:00:00', '01/09/22 10:00:00', '01/10/22 10:00:00', '01/11/22 10:00:00', '01/12/22 10:00:00']
    data = []
    for linha in dataframe.itertuples():
        indice_periodo = 0
        for i in range(7, 31):
            previsto = i
            realizado = i + 24
            farol = 0

            try:
                if linha[realizado] == 0 or linha[realizado] == None:
                    farol = 4  # CINZA
                elif ((linha[realizado] * 100) / linha[previsto]) >= 100:
                    farol = 3  # VERDE
                elif (((linha[realizado] * 100) / linha[previsto]) >= 90) & (((linha[realizado] * 100) / linha[previsto]) < 100):
                    farol = 2  # AMARELO
                else:
                    farol = 1  # VERMELHO
            except ZeroDivisionError:
                farol = 4  # CINZA

            try:
                calculado = linha[realizado] / linha[previsto]
            except ZeroDivisionError:
                calculado = 0

            date_time_obj = datetime.strptime(
                periodoDate[indice_periodo], '%d/%m/%y %H:%M:%S')

            data.append({
                "id": linha.id,
                "nome_projeto": linha.nome_projeto,
                "tipo_kpi": linha.tipo_kpi,
                'kpi': linha.kpi,
                'competencia': date_time_obj,
                'previsto': linha[previsto],
                'realizado': linha[realizado],
                'calculado': calculado,
                'farol': farol
            })
            indice_periodo += 1

    return data
