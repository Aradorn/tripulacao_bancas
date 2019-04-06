import pandas as pd
from Funcao_Custo import *

def heuristica_vizinho(tabela_custos,quantidade_professores,quantidade_bancas,orientadores):

    custo_best = 99999999999999
    best_prof = []
    professores_geral = []
    bancas = pd.DataFrame(columns=['Banca', 'Composicao', 'Custo'])

    for banca in range(quantidade_bancas):
        #professor_inicial = random.randint(0,quantidade_professores-1)
        professor_inicial = orientadores[banca]
        professores = list(range(quantidade_professores))
        del (professores[professor_inicial])
        composicao = [professor_inicial]
        n = len(professores)

        while len(composicao) < 3:
            for i in range(n - 1):
                teste_composicao = composicao[:]
                teste_composicao.append(professores[i])
                if custo_bancas(tabela_custos, banca, teste_composicao, professores_geral) < custo_best:
                    custo_best = custo_bancas(tabela_custos, banca, teste_composicao, professores_geral)
                    best_prof = professores[i]

            composicao.append(best_prof)
            custo_best = 99999999999999
            professores.remove(best_prof)
            n = len(professores)
            professores_geral.append(best_prof)
            best_prof = []
        professores_geral.append(professor_inicial)

        Banca = ("Banca {}".format(banca))
        Composicao = composicao
        Custo = custo_bancas(tabela_custos, banca, composicao, professores_geral)

        banca_individual = {'Banca': Banca, 'Composicao': Composicao, 'Custo': Custo}
        bancas = bancas.append(banca_individual, ignore_index=True)

        custo_best = 99999999999999
        best_prof = []

    return bancas

def converter_nomes(composicao_bancas,dic_professores):

    composicao = []

    for banca in composicao_bancas:
        banca_indiv = []
        for professor in banca:
            banca_indiv.append(dic_professores[professor])
        composicao.append(banca_indiv)

    return composicao