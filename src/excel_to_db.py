import pandas as pd
import time
from google.oauth2 import service_account
from src.utils import getGoogleCredentials
import os

SGB_BIGQUERY_JSON = os.getenv("SGB_BIGQUERY_JSON")


def uploadDataGBQ(path):
    credentials = service_account.Credentials.from_service_account_info(
        getGoogleCredentials())

    start_time = time.time()
    # Importar dados da planilha na aba KPI's
    kpisDF = pd.read_excel(path,
                           sheet_name='06-Apoio-KPIs consolidados', header=1)

    # Converter colunas dos KPIS REALIZADOS em float
    for x in range(37, 61):
        nomeColuna = kpisDF.columns[x]
        kpisDF[nomeColuna] = pd.to_numeric(kpisDF[nomeColuna], errors='coerce')

    # DE_PARA de colunas e nomes que devem ser renomeados para facilitar a leitura
    renameColumns = {
        'Nome do projeto': 'nome_projeto',
        'KPI': 'kpi',
        'Tipo': 'tipo_kpi',
        'Data base': 'data_base',
        'Data alvo': 'data_alvo',
        kpisDF.columns[12]: 'prev_jan_2021',
        kpisDF.columns[13]: 'prev_fev_2021',
        kpisDF.columns[14]: 'prev_mar_2021',
        kpisDF.columns[15]: 'prev_abr_2021',
        kpisDF.columns[16]: 'prev_mai_2021',
        kpisDF.columns[17]: 'prev_jun_2021',
        kpisDF.columns[18]: 'prev_jul_2021',
        kpisDF.columns[19]: 'prev_ago_2021',
        kpisDF.columns[20]: 'prev_set_2021',
        kpisDF.columns[21]: 'prev_out_2021',
        kpisDF.columns[22]: 'prev_nov_2021',
        kpisDF.columns[23]: 'prev_dez_2021',
        kpisDF.columns[24]: 'prev_jan_2022',
        kpisDF.columns[25]: 'prev_fev_2022',
        kpisDF.columns[26]: 'prev_mar_2022',
        kpisDF.columns[27]: 'prev_abr_2022',
        kpisDF.columns[28]: 'prev_mai_2022',
        kpisDF.columns[29]: 'prev_jun_2022',
        kpisDF.columns[30]: 'prev_jul_2022',
        kpisDF.columns[31]: 'prev_ago_2022',
        kpisDF.columns[32]: 'prev_set_2022',
        kpisDF.columns[33]: 'prev_out_2022',
        kpisDF.columns[34]: 'prev_nov_2022',
        kpisDF.columns[35]: 'prev_dez_2022',
        '2021-01-01 00:00:00.1': 'real_jan_2021',
        '2021-02-01 00:00:00.1': 'real_fev_2021',
        '2021-03-01 00:00:00.1': 'real_mar_2021',
        '2021-04-01 00:00:00.1': 'real_abr_2021',
        '2021-05-01 00:00:00.1': 'real_mai_2021',
        '2021-06-01 00:00:00.1': 'real_jun_2021',
        '2021-07-01 00:00:00.1': 'real_jul_2021',
        '2021-08-01 00:00:00.1': 'real_ago_2021',
        '2021-09-01 00:00:00.1': 'real_set_2021',
        '2021-10-01 00:00:00.1': 'real_out_2021',
        '2021-11-01 00:00:00.1': 'real_nov_2021',
        '2021-12-01 00:00:00.1': 'real_dez_2021',
        '2022-01-01 00:00:00.1': 'real_jan_2022',
        '2022-02-01 00:00:00.1': 'real_fev_2022',
        '2022-03-01 00:00:00.1': 'real_mar_2022',
        '2022-04-01 00:00:00.1': 'real_abr_2022',
        '2022-05-01 00:00:00.1': 'real_mai_2022',
        '2022-06-01 00:00:00.1': 'real_jun_2022',
        '2022-07-01 00:00:00.1': 'real_jul_2022',
        '2022-08-01 00:00:00.1': 'real_ago_2022',
        '2022-09-01 00:00:00.1': 'real_set_2022',
        '2022-10-01 00:00:00.1': 'real_out_2022',
        '2022-11-01 00:00:00.1': 'real_nov_2022',
        '2022-12-01 00:00:00.1': 'real_dez_2022',
        'Última importação': 'ultima_importacao'
    }

    # Gerar o Dataframe sem as colunas desnecessárias e com o nome das colunas renomeados.
    kpisLimpoDF = kpisDF.drop([kpisDF.columns[0], 'Fonte', 'Valor \nbase', 'Valor \nalvo', 'Atual', 'Linha de base', 'Responsável', 'Atual.1', '%Realizado',
                               'Unnamed: 63', 'Unnamed: 64', 'Formula'], axis='columns')
    kpisLimpoDF.rename(columns=renameColumns, inplace=True)
    kpisLimpoDF.fillna({'kpi': 'Não Informado'}, inplace=True)
    kpisLimpoDF.fillna(0, inplace=True)

    # Definição dos períodos
    periodo = ['jan_2021', 'fev_2021', 'mar_2021', 'abr_2021', 'mai_2021', 'jun_2021', 'jul_2021', 'ago_2021',
               'set_2021', 'out_2021', 'nov_2021', 'dez_2021', 'jan_2022', 'fev_2022', 'mar_2022', 'abr_2022', 'mai_2022',
               'jun_2022', 'jul_2022', 'ago_2022', 'set_2022', 'out_2022', 'nov_2022', 'dez_2022']

    # Funcao que calcula e separa os kpis por periodo e retorna um dicionário com os dados

    def separarKPIs(dataframe):
        data = []
        for linha in dataframe.itertuples():
            indice_periodo = 0
            for i in range(6, 30):
                previsto = i
                realizado = i + 24
                farol = 0

                try:
                    if ((linha[realizado] * 100) / linha[previsto]) >= 80:
                        farol = 'VERDE'  # 1  # VERDE
                    elif (((linha[realizado] * 100) / linha[previsto]) >= 60) & (((linha[realizado] * 100) / linha[previsto]) < 80):
                        farol = 'AMARELO'  # 2  # AMARELO
                    else:
                        farol = 'VERMELHO'  # 3  # VERMELHO
                except ZeroDivisionError:
                    farol = 'CINZA'  # 4  # CINZA

                try:
                    calculado = linha[realizado] / linha[previsto]
                except ZeroDivisionError:
                    calculado = 0

                data.append({
                    "nome_projeto": linha.nome_projeto,
                    "tipo_kpi": linha.tipo_kpi,
                    'kpi': linha.kpi,
                    'periodo': periodo[indice_periodo],
                    'previsto': linha[previsto],
                    'realizado': linha[realizado],
                    'calculado': calculado,
                    'farol': farol
                })
                indice_periodo += 1

        return data

    kpisConsolidados = pd.DataFrame(data=separarKPIs(kpisLimpoDF))
    # remover espaços do inicio da descrição dos KPI's
    kpisConsolidados['kpi'].replace(
        ['^\s', '\n'], value='', regex=True, inplace=True)

    # Enviar dados tratados para o GBQ
    try:
        kpisConsolidados.to_gbq(credentials=credentials, destination_table='projetos_sgd.kpisPorPeriodo',
                                if_exists='replace', project_id='sgdgovbr')
    except:
        print('Deu erro na hora de jogar os dados no GBQ')
        return 'Deu erro'

    print('Tempo de execução: %s segundos' % (time.time() - start_time))
    return 'OK'
