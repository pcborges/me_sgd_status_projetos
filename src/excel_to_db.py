import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from config import getDBConnectionString
from .db_utils import softDelete
from .utils import separarKPIs

engine = create_engine(getDBConnectionString())


def alocacoesToDB(path):
    try:
        alocacaoDF = pd.read_excel(path,
                                   sheet_name='02-Alocação')
    except Exception:
        return 'Aba 02-Alocação não encontrada, verifique se não houveram mudanças na estrutura da planilha'

    try:
        alocacaoDF = alocacaoDF.iloc[0:, 0:8]
        alocacaoDF.fillna('N/D', inplace=True)
        colunas = {
            "STARTUP": "startup",
            "ORGÃO": "sigla_orgao",
            "ESPECIALIDADE": "especialidade",
            'CARGO': 'cargo',
            "NOME": "nome",
            "OBS": "observacao",
            "ALOCAÇÃO": "situacao",
            "UF": "uf",
        }

        alocacaoDF.rename(columns=colunas, inplace=True)
        # Remover espaços de strings
        alocacaoDF['startup'] = alocacaoDF['startup'].str.strip()
        alocacaoDF['especialidade'] = alocacaoDF['especialidade'].str.strip()
        alocacaoDF['uf'] = alocacaoDF['uf'].str.strip()
        #
        # Status 9 indica a visão mais atualizada da informação
        alocacaoDF = alocacaoDF.assign(in_carga=9)
        alocacaoDF = alocacaoDF.assign(dt_carga=datetime.now())
        alocacaoDF.set_index('startup')

    except Exception as err:
        print(err)
        return 'Problemas ao efetuar tratamentos da aba 02-Alocação, verifique se houveram mudanças na estrutura de colunas da planilha.'

    try:
        softDelete(engine, 'alocacoes')
    except Exception as err:
        print("ERRO DE BANCO", err)
        return 'Erro ao efetuar exclusão lógica dos registros de Alocacoes'
    try:
        alocacaoDF.to_sql(name='alocacoes', con=engine,
                          if_exists='append', index=False)
    except Exception as err:
        print(err)
        return 'Erro ao salvar dados convertidos de Projetos para o MySQL'

    return 'OK'


def relatoPontosAtencaoToDB(path):
    # Importar dados da planilha na aba KPI's
    try:
        relatosDF = pd.read_excel(path,
                                  sheet_name='Apoio-Projetos', usecols=['Relato', 'Pontos de Atenção',
                                                                        'Última Atualização', 'ID'])
    except Exception:
        return 'Aba de Apoio-Projetos não encontrada.'
    # tratar informações das Startups
    try:
        relatosDF.rename(columns={'Relato': 'relato', 'Pontos de Atenção': 'pontos_atencao',
                         'Última Atualização': 'ultima_atualizacao', 'ID': 'id'}, inplace=True)
        relatosDF[['relato', 'pontos_atencao']].replace(
            ['^\s', '\t', '\n', '_x([0-9a-fA-F]{4})_'], value='', regex=True, inplace=True)

    except Exception:
        return 'Problemas ao converter dados da Aba Apoio-Projetos'
    # Recuperar projetos do DB para fazer validacoes
    try:
        query = 'SELECT id, startup FROM `projetos` where in_carga = 9'
        projetosDF = pd.read_sql(
            query, con=engine)
    except Exception as err:
        print(err)
        return 'Problemas ao buscar dados de projetos do banco de dados.'
    # Consolidar informações em um único dataframe
    try:
        projetosRelatosDF = relatosDF.merge(
            projetosDF, on='id', how='left')
        projetosRelatosDF.fillna({'orgao': 'N/D', 'relato': 'N/D',
                                  'pontos_atencao': 'N/D', 'ultima_atualizacao': ''}, inplace=True)
        projetosRelatosDF = projetosRelatosDF.assign(in_carga=9)
        projetosRelatosDF = projetosRelatosDF.assign(dt_carga=datetime.now())
        projetosRelatosDF.set_index('id')
    except Exception as err:
        print(err)
        return 'Problemas ao relacionar pontos de atenção e relatos aos projetos, verificar se existe ID na aba Apoio-Projetos'
    try:
        softDelete(engine, 'relatos')
    except Exception as err:
        print("ERRO DE BANCO", err)
        return 'Erro ao efetuar exclusão lógica dos registros de Relatos'

    try:
        projetosRelatosDF.to_sql(name='relatos', con=engine,
                                 if_exists='append', index=False)
    except Exception as err:
        print(err)
        return 'Erro ao salvar dados convertidos de Projetos para o MySQL'

    return 'OK'


def kpisToDB(path):
    # Importar dados da planilha na aba KPI's
    try:
        kpisDF = pd.read_excel(path,
                               sheet_name='06-Apoio-KPIs consolidados', header=1)
    except Exception:
        return 'Aba 06-Apoio-KPIs não encontrada na planilha'

    # Converter colunas dos KPIS REALIZADOS em float
    try:
        for x in range(38, 63):
            nomeColuna = kpisDF.columns[x]
            kpisDF[nomeColuna] = pd.to_numeric(
                kpisDF[nomeColuna], errors='coerce')
    except Exception:
        return 'Verificar se colunas de KPIs Previstos/Realizados existem apenas valores numéricos.'

    try:
        # Gerar o Dataframe sem as colunas desnecessárias e com o nome das colunas renomeados.
        kpisLimpoDF = kpisDF.drop([kpisDF.columns[0], 'Fonte', 'Valor \nbase', 'Valor \nalvo', 'Atual', 'Linha de base', 'Responsável', 'Atual.1', '%Realizado',
                                   'Unnamed: 64', 'Unnamed: 65', 'Formula'], axis='columns')
        # DE_PARA de colunas e nomes que devem ser renomeados para facilitar a leitura
        renameColumns = {
            'ID': 'id',
            'Nome do projeto': 'nome_projeto',
            'KPI': 'kpi',
            'Tipo': 'tipo_kpi',
            'Data base': 'data_base',
            'Data alvo': 'data_alvo',
            kpisLimpoDF.columns[6]: 'prev_jan_2021',
            kpisLimpoDF.columns[7]: 'prev_fev_2021',
            kpisLimpoDF.columns[8]: 'prev_mar_2021',
            kpisLimpoDF.columns[9]: 'prev_abr_2021',
            kpisLimpoDF.columns[10]: 'prev_mai_2021',
            kpisLimpoDF.columns[11]: 'prev_jun_2021',
            kpisLimpoDF.columns[12]: 'prev_jul_2021',
            kpisLimpoDF.columns[13]: 'prev_ago_2021',
            kpisLimpoDF.columns[14]: 'prev_set_2021',
            kpisLimpoDF.columns[15]: 'prev_out_2021',
            kpisLimpoDF.columns[16]: 'prev_nov_2021',
            kpisLimpoDF.columns[17]: 'prev_dez_2021',
            kpisLimpoDF.columns[18]: 'prev_jan_2022',
            kpisLimpoDF.columns[19]: 'prev_fev_2022',
            kpisLimpoDF.columns[20]: 'prev_mar_2022',
            kpisLimpoDF.columns[21]: 'prev_abr_2022',
            kpisLimpoDF.columns[22]: 'prev_mai_2022',
            kpisLimpoDF.columns[23]: 'prev_jun_2022',
            kpisLimpoDF.columns[24]: 'prev_jul_2022',
            kpisLimpoDF.columns[25]: 'prev_ago_2022',
            kpisLimpoDF.columns[26]: 'prev_set_2022',
            kpisLimpoDF.columns[27]: 'prev_out_2022',
            kpisLimpoDF.columns[28]: 'prev_nov_2022',
            kpisLimpoDF.columns[29]: 'prev_dez_2022',
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
        kpisLimpoDF.rename(columns=renameColumns, inplace=True)
        kpisLimpoDF.fillna({'kpi': 'Não Informado'}, inplace=True)
        kpisLimpoDF.fillna(0, inplace=True)
        kpisLimpoDF.drop(kpisLimpoDF[kpisLimpoDF['nome_projeto']
                         == 'Indicadores Consolidados'].index, inplace=True)
    except Exception as err:
        print(err)
        return 'Problemas ao converter colunas do excel, verificar nomes e estrutura da tabela.'

    # Recuperar os Kpis separados para salvar no banco
    try:
        kpisConsolidados = pd.DataFrame(data=separarKPIs(kpisLimpoDF))
        # remover espaços do inicio da descrição dos KPI's
        kpisConsolidados['kpi'].replace(
            ['^\s', '\n'], value='', regex=True, inplace=True)
    except Exception as err:
        print(err)
        return 'Erro ao consolidar indicadores, verificar se não foi alterada a estrutura da tabela.'

    try:
        # Carregar tabela de projetos do DB para fazer validações
        query = 'SELECT id, startup FROM `projetos` where in_carga = 9'
        projetosDF = pd.read_sql(
            query, con=engine)
    except Exception as e:
        return f'Erro ao recuperar dados do Banco de Dados: {e}'

    try:
        consolidadoDF = kpisConsolidados.merge(
            projetosDF, on="id", how="left")
        columns_order = ['id', 'startup', 'nome_projeto', 'tipo_kpi',
                         'kpi', 'competencia', 'previsto', 'realizado', 'calculado', 'farol']
        consolidadoDF = consolidadoDF.reindex(columns=columns_order)
        # Status 9 indica a visão mais atualizada da informação
        consolidadoDF.drop(['nome_projeto'], axis='columns', inplace=True)
        consolidadoDF = consolidadoDF.assign(in_carga=9)
        consolidadoDF = consolidadoDF.assign(dt_carga=datetime.now())
        consolidadoDF.set_index('id')
    except Exception:
        return 'Problemas ao consolidar dados de KPIs com dados dos Projetos no Banco de Dados'

    try:
        projetosNulos = consolidadoDF.loc[consolidadoDF['startup'].isnull(
        )]
        if not projetosNulos.empty:
            listaProjetosDiferentes = projetosNulos['id'].unique()
            return f'Existem Projetos na Aba KPIs que não estão no DB de Projetos, IDs: {listaProjetosDiferentes} '
    except Exception as e:
        return f'Erro ao buscar projetos que existem na planilha de Kpis e não existem na tabela de projetos'

    try:
        softDelete(engine, 'indicadores')
    except Exception as err:
        print("ERRO DE BANCO", err)
        return 'Erro ao efetuar exclusão lógica dos registros de Indicadores'

    try:
        consolidadoDF.to_sql(name='indicadores', con=engine,
                             if_exists='append', index=False)
    except Exception as e:
        print(e)
        return 'Erro ao salvar dados convertidos de Projetos para o MySQL'

    return 'OK'


def projetosToDB(path):
    # Importar dados da planilha na aba KPI's
    nomeAba = '03 - GP CGPE'
    try:
        projetosDF = pd.read_excel(
            path, sheet_name=nomeAba, header=2)
    except Exception:
        return f'Aba {nomeAba} não encontrada, verifique se o arquivo enviado está no padrão esperado.'
    filtroColunas = ['ID', 'ÓRGÃO', 'Projeto', 'Resumo', 'Startup', 'Líder do Projeto', 'Email',
                     'Telefone', 'Titular CGPE', 'Substituto CGPE ', 'Status', 'SITUAÇÃO', 'Observação']

    newColumnsNames = {
        "ÓRGÃO": "sigla_orgao", "Projeto": "nome_projeto", "Resumo": "resumo", "Líder do Projeto": "lider_squad", "Email": "email_lider",
        "Telefone": "telefone_lider", "Titular CGPE": "titular_cgpe", "Substituto CGPE ": "substituto_cgpe", "Status": "status",
        "SITUAÇÃO": "situacao", "Observação": "observacao", 'Startup': 'startup', 'ID': 'id'
    }
    # Enviar dados tratados para o GBQ
    try:
        projetosDF = projetosDF.loc[:, filtroColunas]
        projetosDF.rename(columns=newColumnsNames, inplace=True)
        projetosDF.fillna('N/D', inplace=True)
        projetosDF['nome_projeto'] = projetosDF['nome_projeto'].str.strip()
        projetosDF['resumo'] = projetosDF['resumo'].str.strip()
        # Status 9 indica a visão mais atualizada da informação
        projetosDF = projetosDF.assign(in_carga=9)
        projetosDF = projetosDF.assign(dt_carga=datetime.now())
        projetosDF.set_index('id')
    except Exception as err:
        print(err)
        return 'Problemas ao converter nome de colunas, verifique se a planilha não foi modificada.'

    # Verificar duplicidade de projetos
    if len(projetosDF['nome_projeto'].unique()) < len(projetosDF.index):
        return f'Aba {nomeAba} tem projetos com mesmo nome, favor verificar.'

    try:
        softDelete(engine, 'projetos')
    except Exception as err:
        print("ERRO DE BANCO", err)
        return 'Erro ao efetuar exclusão lógica dos registros de Projetos'
    try:
        projetosDF.to_sql(name='projetos', con=engine,
                          if_exists='append', index=False)
    except Exception as err:
        print(err)
        return 'Erro ao salvar dados convertidos de Projetos para o MySQL'

    return 'OK'
