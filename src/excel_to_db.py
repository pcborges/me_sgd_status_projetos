import pandas as pd
import time
from google.oauth2 import service_account
from datetime import datetime

credentials = service_account.Credentials.from_service_account_file(
    'google-credentials.json')


def startupsToDB(path):
    # Importar dados da planilha na aba KPI's
    print('CARGA_STARTUPS_INICIO')
    start_time = time.time()
    try:
        startupsDF = pd.read_excel(path,
                                   sheet_name='Apoio-Projetos')
        metadadosDF = pd.read_excel(
            path, sheet_name='Apoio-Metadados', header=1)
    except Exception:
        return 'Aba de Apoio-Projetos ou Apoio-Metadados não encontrada.'
    # tratar informações das Startups
    try:
        startupsDF.rename(columns={'Area/Projeto': 'nome_projeto', 'Orgao': 'orgao', 'Status': 'status', 'Relato': 'relato',
                          'Pontos de Atenção': 'pontos_atencao', 'Última Atualização': 'ultima_atualizacao'}, inplace=True)
        startupsDF['relato'].replace(
            ['^\s', '\t', '\n'], value='', regex=True, inplace=True)

    except Exception:
        return 'Problemas ao converter dados da Aba Apoio-Projetos'
    # tratar informações da aba de metadados
    try:
        metadadosFiltradoDF = metadadosDF.iloc[:, 0:3]
        metadadosFiltradoDF.rename(columns={
                                   'Unnamed: 0': 'id', 'Unnamed: 1': 'nome_resumido', 'Unnamed: 2': 'nome_projeto'}, inplace=True)
    except Exception:
        return 'Problemas ao converter dados da Aba Apoio-Metadados, verifique se não houve mudança na estrutura da planilha.'
    # Consolidar informações em um único dataframe
    try:
        startupsConsolidadoDF = metadadosFiltradoDF.merge(
            startupsDF, on='nome_projeto', how='left')
        startupsConsolidadoDF.fillna({'orgao': 'N/D', 'relato': 'N/D',
                                      'pontos_atencao': 'N/D', 'ultima_atualizacao': '', 'status': 'Pactuação'}, inplace=True)
    except Exception:
        return 'Problemas ao consolidar abas Apoio-Projetos e Apoio-Metadados, verificar se não houve alterações no layout das planilhas'
    # Enviar dados tratados para o GBQ
    try:
        startupsConsolidadoDF.to_gbq(credentials=credentials, destination_table='projetos_sgd.startups',
                                     if_exists='replace', project_id='sgdgovbr')
    except Exception:
        return 'Erro ao salvar dados convertidos da aba Apoio-Projetos no banco de dados.'
    print('Tempo de execução: %s segundos' % (time.time() - start_time))
    print('CARGA_STARTUPS_FIM')
    return 'OK'


def kpisToDB(path):
    print('CARGA_KPIS_INICIO')
    start_time = time.time()
    # Importar dados da planilha na aba KPI's
    try:
        kpisDF = pd.read_excel(path,
                               sheet_name='06-Apoio-KPIs consolidados', header=1)
        metadadosDF = pd.read_excel(
            path, sheet_name='Apoio-Metadados', header=1)
    except Exception:
        return 'Aba 06-Apoio-KPIs consolidados ou Apoio-Metadados não encontrada'

    # Converter colunas dos KPIS REALIZADOS em float
    try:
        for x in range(37, 61):
            nomeColuna = kpisDF.columns[x]
            kpisDF[nomeColuna] = pd.to_numeric(
                kpisDF[nomeColuna], errors='coerce')
    except Exception:
        return 'Problemas ao converter colunas de kpis para float'

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
    try:
        # Gerar o Dataframe sem as colunas desnecessárias e com o nome das colunas renomeados.
        kpisLimpoDF = kpisDF.drop([kpisDF.columns[0], 'Fonte', 'Valor \nbase', 'Valor \nalvo', 'Atual', 'Linha de base', 'Responsável', 'Atual.1', '%Realizado',
                                   'Unnamed: 63', 'Unnamed: 64', 'Formula'], axis='columns')
        kpisLimpoDF.rename(columns=renameColumns, inplace=True)
        kpisLimpoDF.fillna({'kpi': 'Não Informado'}, inplace=True)
        kpisLimpoDF.fillna(0, inplace=True)
        kpisLimpoDF.drop(kpisLimpoDF[kpisLimpoDF['nome_projeto']
                         == 'Indicadores Consolidados'].index, inplace=True)
    except Exception:
        return 'Problemas ao converter colunas do excel, verificar nomes e estrutura da tabela.'

    # Definição dos períodos
    periodo = ['jan_2021', 'fev_2021', 'mar_2021', 'abr_2021', 'mai_2021', 'jun_2021', 'jul_2021', 'ago_2021',
               'set_2021', 'out_2021', 'nov_2021', 'dez_2021', 'jan_2022', 'fev_2022', 'mar_2022', 'abr_2022', 'mai_2022',
               'jun_2022', 'jul_2022', 'ago_2022', 'set_2022', 'out_2022', 'nov_2022', 'dez_2022']

    periodoDate = ['01/01/21 10:00:00', '01/02/21 10:00:00', '01/03/21 10:00:00', '01/04/21 10:00:00', '01/05/21 10:00:00', '01/06/21 10:00:00',
                   '01/07/21 10:00:00', '01/08/21 10:00:00', '01/09/21 10:00:00', '01/10/21 10:00:00', '01/11/21 10:00:00', '01/12/21 10:00:00', '01/01/22 10:00:00',
                   '01/02/22 10:00:00', '01/03/22 10:00:00', '01/04/22 10:00:00', '01/05/22 10:00:00', '01/06/22 10:00:00', '01/07/22 10:00:00',
                   '01/08/22 10:00:00', '01/09/22 10:00:00', '01/10/22 10:00:00', '01/11/22 10:00:00', '01/12/22 10:00:00']

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
                    if linha[realizado] == 0 or linha[realizado] == None:
                        farol = 4  # CINZA
                    elif ((linha[realizado] * 100) / linha[previsto]) >= 80:
                        farol = 3  # VERDE
                    elif (((linha[realizado] * 100) / linha[previsto]) >= 60) & (((linha[realizado] * 100) / linha[previsto]) < 80):
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
                    "nome_projeto": linha.nome_projeto,
                    "tipo_kpi": linha.tipo_kpi,
                    'kpi': linha.kpi,
                    'periodo': date_time_obj,
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
    # Limpar a tabela de METADADOS tirando o que não é útil
    metadadosFiltradoDF = metadadosDF.iloc[:, 0:3]
    metadadosFiltradoDF.rename(columns={
                               'Unnamed: 0': 'id', 'Unnamed: 1': 'nome_resumido', 'Unnamed: 2': 'nome_projeto'}, inplace=True)
    try:
        consolidadoDF = kpisConsolidados.merge(
            metadadosFiltradoDF, on="nome_projeto", how="left")
        columns_order = ['id', 'nome_projeto', 'nome_resumido', 'tipo_kpi',
                         'kpi', 'periodo', 'previsto', 'realizado', 'calculado', 'farol']
        consolidadoDF = consolidadoDF.reindex(columns=columns_order)
    except Exception:
        return 'Problemas ao consolidar abas 06-Apoio-KPIs consolidados e Apoio-Metadados, verificar se não houve alterações no layout das planilhas'

    # Enviar dados tratados para o GBQ
    try:
        consolidadoDF.to_gbq(credentials=credentials, destination_table='projetos_sgd.kpisPorPeriodo',
                             if_exists='replace', project_id='sgdgovbr')
    except Exception:
        return 'Erro ao salvar dados convertidos da aba de KPIs para o BigQuery'

    print('Tempo de execução: %s segundos' % (time.time() - start_time))
    print('CARGA_KPIS_FIM')
    return 'OK'


def projetosToDB(path):
    # Importar dados da planilha na aba KPI's
    print('CARGA_PROJETOS_INICIO')
    start_time = time.time()
    try:
        projetosDF = pd.read_excel(path, sheet_name='01-Projetos')
    except Exception:
        return 'Aba 01-Projetos não encontrada, verifique se o arquivo enviado está no padrão esperado.'

    newColumnsNames = {'Orgão': 'orgao',	'Sigla Orgão': 'sigla_orgao', 	'Nome do projeto': 'nome_projeto',	'Escopo do Projeto': 'escopo_projeto', 	'Números do Projeto': 'numeros_projeto', 	'Recomendação de Implantação': 'recomendacao_implantacao', 	'Motivo Recomendação': 'motivo_recomendacao', 	'Status do Projeto': 'status_projeto', 	'Fase': 'fase_projeto',
                       'Substituto': 'lider_substituto', 	'Líder no Órgão': 'lider_orgao', 	'Líder do SQUAD': 'lider_squad', 	'Gestão': 'qtd_gestao', 'Equipe SGD': 'qtd_equipe_sgd',	'Temporários': 'qtd_temporarios',	'Pessoas Alocadas': 'qtd_pessoas_alocadas', 	'Nível de Risco': 'nivel_risco_projeto', 	'Pontos de Atenção': 'pontos_atencao', 	'Relato': 'relato',	'Processo SEI': 'processo_sei'}
    # Enviar dados tratados para o GBQ
    try:
        projetosDF = projetosDF.iloc[0:, 1:20]
        projetosDF.rename(columns=newColumnsNames, inplace=True)
        projetosDF.fillna({'qtd_gestao': 0,	'qtd_equipe_sgd': 0,
                          'qtd_temporarios': 0}, inplace=True)
        projetosDF.fillna('N/D', inplace=True)
    except Exception:
        return 'Problemas ao converter nome de colunas, verifique se a planilha não foi modificada.'

    # Enviar dados tratados para o GBQ
    try:
        projetosDF.to_gbq(credentials=credentials, destination_table='projetos_sgd.projetos',
                          if_exists='replace', project_id='sgdgovbr')
    except Exception:
        return 'Erro ao salvar dados convertidos de Projetos para o BigQuery'

    print('Tempo de execução: %s segundos' % (time.time() - start_time))
    print('CARGA_PROJETOS_FIM')
    return 'OK'
