import pandas as pd
import json


def getIndicadoresProjetos(path, index_mes_ano_indicador=16):
    df = pd.read_excel(path, sheet_name='KPIs', header=1)
    #startupsDF = aba1.loc[0:, ['Nome do projeto','Sigla Orgão', 'Status do Projeto', 'Líder do SQUAD']]
    # referenciaEsperado 16 é o mês de Maio/21 (número da coluna da planilha transformada no dataframe)
    referenciaEsperado = index_mes_ano_indicador
    referenciaRealizado = referenciaEsperado + 25
    kpisDF = df.iloc[0:, [1, 3, 6, referenciaEsperado, referenciaRealizado]]
    kpisDF.columns.values[3] = 'Esperado'
    kpisDF.columns.values[4] = 'Realizado'
    # kpisDF.columns
    #kpisDF.loc[kpisDF['Esperado Mai/21'] > kpisDF['Realizado Mai/21'], 'KPI Maio/2021'] = 'Atrasado'
    kpisDF.fillna(value={'Esperado': 0, 'Realizado': 0,
                  'KPI': ''}, inplace=True)
    kpisDF['Farol'] = kpisDF.apply(getIndicadorKPI, axis=1)
    kpisDF = kpisDF.reindex(
        columns=['Nome do projeto', 'KPI', 'Esperado', 'Realizado', 'Farol'])
    kpisDF['Nome do projeto'] = kpisDF['Nome do projeto'].str.lower()
    execucaoDF = kpisDF[kpisDF['KPI'].str.contains("Exec")]
    execucaoDF = execucaoDF.reset_index(drop=True)
    entregasDF = kpisDF[kpisDF['KPI'].str.contains("Entregas")]
    entregasDF = entregasDF.reset_index(drop=True)
    dfFinal = getDFComIndicadorConsolidado(execucaoDF, entregasDF)
    farol = {4: 'VERDE', 3: 'AMARELO', 2: 'VERMELHO', 1: 'CINZA'}
    dfFinal['Farol'].replace(farol, inplace=True)
    dfFinal.drop(['KPI', 'Esperado', 'Realizado'],
                 axis='columns', inplace=True)
    # return dfFinal.to_json(orient="split")
    return dfFinal


def getProjetosEmExecucaoHTML(path, index_mes_ano_indicador=16):
    df = pd.read_excel(path, sheet_name='Startups')
    df = df.loc[0:, ['Nome do projeto', 'Sigla Orgão',
                     'Status do Projeto', 'Líder do SQUAD']]
    df.fillna(value={'Líder do SQUAD': 'N/D'}, inplace=True)
    df['Nome do projeto'] = df['Nome do projeto'].str.lower()
    emExecucaoDF = df[df['Status do Projeto'].str.contains("Exec")]
    indicadoresDF = getIndicadoresProjetos(path, index_mes_ano_indicador)
    projetosEmExecucaoDFTotal = pd.merge(
        emExecucaoDF, indicadoresDF, how='left', on='Nome do projeto')
    projetosEmExecucaoDFTotal.fillna(value={'Farol': 'CINZA'})
    return projetosEmExecucaoDFTotal.to_html(index=False, classes=['table', 'table-striped'], justify='left', table_id='emExecucao')


def getProjetosEmDiagnosticoHTML(path, index_mes_ano_indicador=16):
    df = pd.read_excel(path, sheet_name='Startups')
    df = df.loc[0:, ['Nome do projeto', 'Sigla Orgão',
                     'Status do Projeto', 'Fase', 'Líder do SQUAD']]
    df['Nome do projeto'] = df['Nome do projeto'].str.lower()
    df.fillna(value={'Líder do SQUAD': 'N/D'}, inplace=True)
    emDiagnosticoDF = df[df['Status do Projeto'].str.contains(
        "Diagn")]
    emDiagnosticoDF.drop('Status do Projeto', axis='columns', inplace=True)
    fases = {'1.1 - Prospectado': 'Prospectado', '3.2 - Definição de Escopo': 'Definição de Escopo', '3.4 - Elaboração do ACT e Plano de Trabalho': 'Elaboração do ACT',
             '4.1 - Assinatura do ACT': 'Assinatura do ACT'}
    emDiagnosticoDF['Fase'].replace(fases, inplace=True)
    indicadoresDF = getIndicadoresProjetos(path, index_mes_ano_indicador)
    projetosEmDiagnosticoTotal = pd.merge(
        emDiagnosticoDF, indicadoresDF, how='left', on='Nome do projeto')
    projetosEmDiagnosticoTotal.fillna(value={'Farol': 'CINZA'})
    return projetosEmDiagnosticoTotal.to_html(index=False, classes=['table', 'table-striped'], justify='left', table_id='emDiagnostico')


def getProjetosPriorizadosJSON(path):
    df = pd.read_excel(path, sheet_name='Startups')
    df = df[['Nome do projeto', 'Status do Projeto',
             'Líder do SQUAD', 'Sigla Orgão']]
    indexRemove = df[df['Status do Projeto'] == '1-Em espera'].index
    df.drop(indexRemove, inplace=True)
    df.fillna(value={'Líder do SQUAD': 'N/D'}, inplace=True)
    df.rename(columns={'Nome do projeto': 'nome', 'Status do Projeto': 'status',
              'Líder do SQUAD': 'lider', 'Sigla Orgão': 'sigla_orgao'}, inplace=True)
    status = {'5-Execução': 'execucao', '3-Diagnóstico': 'diagnostico',
              '2-Priorização Estratégica': 'priorizacao'}
    df['status'].replace(status, inplace=True)
    dfJson = df.to_json(orient='records')
    return json.loads(dfJson)
    #df.to_html(index=False, classes=['table', 'table-striped'],  justify='left')


def getTotaisProjetosPriorizados(listaProjetos):
    qtdDiagnostico = 0
    qtdExecucao = 0
    qtdPactuacao = 0
    total = 0
    for projeto in listaProjetos:
        if projeto['status'] == "diagnostico":
            qtdDiagnostico += 1
        elif projeto['status'] == "execucao":
            qtdExecucao += 1
        else:
            qtdPactuacao += 1
    total = qtdDiagnostico + qtdExecucao + qtdPactuacao
    return {'total': total, 'execucao': qtdExecucao, 'diagnostico': qtdDiagnostico, 'pactuacao': qtdPactuacao}


def getIndicadorKPI(linha):
    try:
        # if linha['Esperado Mai/21'] == None | linha['Realizado Mai/21'] == None:
        # return 'CINZA'
        if ((linha['Realizado'] * 100) / linha['Esperado']) >= 85:
            return 4  # VERDE
        elif (((linha['Realizado'] * 100) / linha['Esperado']) >= 70) & (((linha['Realizado'] * 100) / linha['Esperado']) < 85):
            return 3  # AMARELO
        else:
            return 2  # VERMELHO
    except ZeroDivisionError:
        return 1  # CINZA


def getDFComIndicadorConsolidado(execucao, entregas):
    data = []
    for index, row in execucao.iterrows():
        row2 = entregas.iloc[index, -1]
        if row['Farol'] == row2:
            data.append(row)
        elif row['Farol'] > row2:
            data.append(entregas.iloc[index])
        else:
            data.append(row)

    return pd.DataFrame(data)
