import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    'src\sgdkeybigquery.json')


def cargaKpisGBQ():
    # Importar dados da planilha na aba KPI's
    kpis = pd.read_excel("upload/farois_projetos_govbr.xlsm",
                         sheet_name='06-Apoio-KPIs consolidados', header=1)

    renameColumns = {
        'Nome do projeto': 'nome_projeto',
        'KPI': 'kpi',
        'Tipo': 'tipo_kpi',
        'Data base': 'data_base',
        'Data alvo': 'data_alvo',
        kpis.columns[12]: 'prev_jan_2021',
        kpis.columns[13]: 'prev_fev_2021',
        kpis.columns[14]: 'prev_mar_2021',
        kpis.columns[15]: 'prev_abr_2021',
        kpis.columns[16]: 'prev_mai_2021',
        kpis.columns[17]: 'prev_jun_2021',
        kpis.columns[18]: 'prev_jul_2021',
        kpis.columns[19]: 'prev_ago_2021',
        kpis.columns[20]: 'prev_set_2021',
        kpis.columns[21]: 'prev_out_2021',
        kpis.columns[22]: 'prev_nov_2021',
        kpis.columns[23]: 'prev_dez_2021',
        kpis.columns[24]: 'prev_jan_2022',
        kpis.columns[25]: 'prev_fev_2022',
        kpis.columns[26]: 'prev_mar_2022',
        kpis.columns[27]: 'prev_abr_2022',
        kpis.columns[28]: 'prev_mai_2022',
        kpis.columns[29]: 'prev_jun_2022',
        kpis.columns[30]: 'prev_jul_2022',
        kpis.columns[31]: 'prev_ago_2022',
        kpis.columns[32]: 'prev_set_2022',
        kpis.columns[33]: 'prev_out_2022',
        kpis.columns[34]: 'prev_nov_2022',
        kpis.columns[35]: 'prev_dez_2022',
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
    # Converter colunas para float
    for x in range(37, 61):
        nomeColuna = kpis.columns[x]
        kpis[nomeColuna] = pd.to_numeric(kpis[nomeColuna], errors='coerce')

    kpis.drop([kpis.columns[0], 'Fonte', 'Valor \nbase', 'Valor \nalvo', 'Atual', 'Linha de base', 'Responsável', 'Atual.1', '%Realizado',
               'Unnamed: 63', 'Unnamed: 64', 'Formula'], axis='columns', inplace=True)

    kpis.rename(columns=renameColumns, inplace=True)
    kpis.fillna({'kpi': 'Não Informado'}, inplace=True)
    kpis.fillna(0, inplace=True)

    # print(kpis.dtypes)
    # Enviar dados tratados para o GBQ
    kpis.to_gbq(credentials=credentials, destination_table='projetos_sgd.kpis',
                if_exists='replace', project_id='sgdgovbr')


def cargaProjetosGBQ():
    # Importar dados da planilha na aba Startups
    projetosDF = pd.read_excel("upload/farois_projetos_govbr.xlsm",
                               sheet_name='Apoio-Projetos')

    # StartupsDF = df.loc[0:, ['Nome do projeto', 'Sigla Orgão', 'Status do Projeto', 'Fase', 'Líder no Órgão',
    #                          'Líder do SQUAD', 'Equipe SGD', 'Temporários', 'Escopo do Projeto',
    #                          'Números do Projeto', 'Motivo Recomendação', 'Pontos de Atenção']]

    # StartupsDF.rename(columns={'Nome do projeto': 'projeto', 'Status do Projeto': 'status_projeto',
    #                            'Sigla Orgão': 'sigla_orgao', 'Fase': 'fase', 'Líder no Órgão': 'lider_orgao',
    #                            'Líder do SQUAD': 'lider_squad', 'Sigla Orgão': 'sigla_orgao', 'Temporários': 'qtd_temporarios', 'Equipe SGD': 'equipe_sgd',
    #                            'Escopo do Projeto': 'escopo_projeto', 'Números do Projeto': 'numeros_projeto',
    #                            'Motivo Recomendação': 'motivos_recomendacao', 'Pontos de Atenção': 'pontos_atencao'
    #                            }, inplace=True)

    # StartupsDF.fillna({'qtd_temporarios': 0, 'equipe_sgd': 0, 'lider_orgao': 'N/D',
    #                   'lider_squad': 'N/D', 'pontos_atencao': 'N/D'}, inplace=True)

    projetosDF.rename(columns={'Area/Projeto': 'nome_projeto', 'Orgao': 'orgao', 'Status': 'status', 'Relato': 'relato', 'Pontos de Atenção': 'pontos_atencao',
                               'Última Atualização': 'ultima_atualizacao'}, inplace=True)
    projetosDF.replace('\n', ' ', regex=True, inplace=True)
    projetosDF.fillna({'pontos_atencao': 'N/D', 'relato': 'N/D',
                       'ultima_atualizacao': 0}, inplace=True)
    projetosDF.to_gbq(credentials=credentials, destination_table='projetos_sgd.startups',
                      if_exists='append', project_id='sgdgovbr')
    # Enviar dados tratados para o GBQ
    # StartupsDF.to_gbq(credentials=credentials, destination_table='projetos_sgd.startups',
    # if_exists='replace', project_id='sgdgovbr')


# cargaKpisGBQ()




cargaProjetosGBQ()
