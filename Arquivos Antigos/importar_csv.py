import pandas as pd

def importar_disponibilidade():
    dados_df = pd.read_csv('Disponibilidade Professores.csv')
    dados_df = dados_df.replace('Disponível',int(0))
    dados_df = dados_df.replace('Insdisponível',int(1))

    dados = dados_df.values
    dados = dados[:, 2:len(dados[0])]
    dados_geral = dados_df.values
    quantidade_horarios = int(len(dados[0]))
    quantidade_professores = int(len(dados[:, 1]))

    return dados, dados_geral, quantidade_professores, quantidade_horarios

def importar_orientadores():
    orientadores_df = pd.read_csv('Orientadores_Bancas.csv')
    orientadores = orientadores_df.values
    orientadores = orientadores[:,1:len(orientadores[0])]

    return orientadores


