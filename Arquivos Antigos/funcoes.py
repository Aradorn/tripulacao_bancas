import numpy as np
import random as rd
import timeit
from copy import copy


def custo_bancas(composicao_banca,professores,disponibilidade):
    custo = 0
    for banca in range(len(composicao_banca[0,:])):
        for professor in range(len(composicao_banca[:,0])):
            custo_professor = disponibilidade[professores.index(composicao_banca[professor,banca]),banca]+(composicao_banca == composicao_banca[professor,banca]).sum()
            custo = custo + custo_professor
    return custo

def custo_real(composicao_banca,professores,disponibilidade):
    custo = 0
    for banca in range(len(composicao_banca[0,:])):
        for professor in range(len(composicao_banca[:,0])):
            custo_professor = disponibilidade[professores.index(composicao_banca[professor,banca]),banca]
            custo = custo + custo_professor
    return custo

def custo1(tabela,orientadores,composicao, professores):
    quantidade_bancas = len(orientadores)
    custo_interno = 0
    for banca in range(quantidade_bancas):
        orientador_banca = professores.index(orientadores[banca])
        custo_interno = custo_interno + tabela[orientador_banca, composicao[banca]]
    return custo_interno

def busca_trajetoria(dados_horarios,orientadores):
    disponibilidade = dados_horarios[0]
    dados_geral = dados_horarios[1]
    quantidade_professores = dados_horarios[2]
    quantidade_horarios = dados_horarios[3]
    quantidade_bancas = len(orientadores)
    professores = np.array(dados_geral[:, 1]).tolist()
    quantidade_bancas = len(orientadores)
    composicao = []
    horarios = list(range(quantidade_horarios))
    horarios_geral = list(range(quantidade_horarios))
    for banca in range(quantidade_bancas):
        orientador_banca = professores.index(orientadores[banca])
        horarios = horarios_geral
        horario_best = rd.choice(horarios)
        for horario in horarios:
            if horario in horarios:
                if disponibilidade[orientador_banca, horario] < disponibilidade[orientador_banca, horario_best]:
                    horario_best = horario
        composicao.append(horario_best)
        horarios_geral.remove(horario_best)
    return composicao

def tabu(disponibilidade, Si, BTmax, Lt, nvizinho, orientadores, professores):

    Sb = copy(Si)
    melhor_iter = 0
    qtd_swaps = 2
    T = np.zeros((Lt,qtd_swaps),dtype=np.int)

    tempo = timeit.default_timer()
    iter = 0

    while((iter - melhor_iter) < BTmax):
        iter = iter + 1
        lista = swap(disponibilidade, Sb, T, nvizinho, qtd_swaps,orientadores, professores)
        Sv = lista[0]
        for i in reversed(range(Lt)):
            T[i] = T[i - 1]
        T[0,] = lista[1]
        if custo1(disponibilidade,orientadores,Sv, professores) < custo1(disponibilidade, orientadores, Sb, professores):
            Sb = Sv
            melhor_iter = copy(iter)
            if (custo1(disponibilidade, orientadores, Sb, professores) == 0):
                melhor_iter = iter+BTmax

    tempo = timeit.default_timer()- tempo
    lista = [Sb,tempo]

    return lista

def swap(disponibilidade, Si, T, nvizinho, qtd_swaps, orientadores, professores):

    custo_best = custo1(disponibilidade, orientadores, Si, professores)
    SBv = copy(Si)
    qtd_swaps = qtd_swaps
    for i in range(nvizinho):
        tabu = True
        while (tabu == True):
            v = rd.sample(range(len(Si)),qtd_swaps)
            for j in range(len(T[:])):
                for k in range(qtd_swaps):
                    if(T[j][k]==v[k]):
                        tabu = True
                    else:
                        tabu = False
        Sv = copy(Si)
        for m in range(int(qtd_swaps / 2)):
            for n in reversed(range(int(qtd_swaps / 2),qtd_swaps)):
                x = Sv[v[m]]
                Sv[v[m]] = Sv[v[n]]
                Sv[v[n]] = x
        if (custo1(disponibilidade,orientadores, Sv, professores) < custo_best):
            SBv = Sv
            custo_best = custo1(disponibilidade,orientadores, Sv, professores)

    lista = [SBv, v]

    return lista

#-----------------------Tabu de Composicao----------------------------------

def tabu_composicao(composicao_banca,professores,disponibilidade,nvizinho,Lt,BTmax):

    Si = copy(composicao_banca[1:,:])
    Sb = copy(composicao_banca[1:,:])
    melhor_iter = 0
    Lt = 10
    
    #--------------------Criacao Lista Tabu--------------------
    T = []
    a = [0,0]
    b = [0,0]
    t = np.array([a,b])
    for i in range(Lt):
        T.append(t)
    
    tempo = timeit.default_timer()
    iter = 0

    while((iter - melhor_iter) < BTmax):
        iter = iter + 1

        lista = swap_composicao(Si,professores,disponibilidade,composicao_banca,nvizinho,T)

        Sv = lista[0]
        v = lista[1]

        #----Atualizar Tabu
        T.append(v)
        if((len(T)-Lt)>0):
            T = T[(len(T)-Lt):]

        if custo_bancas(Sv,professores,disponibilidade) < custo_bancas(Sb,professores,disponibilidade):
            Sb = copy(Sv)
            melhor_iter = copy(iter)
            if (custo_bancas(Sb,professores,disponibilidade) == 0):
                melhor_iter = iter+BTmax

    tempo = timeit.default_timer()- tempo
    lista = [Sb,tempo]

    return lista

def swap_composicao(Si,professores,disponibilidade,composicao_banca,nvizinho,T):

    custo_best = custo_bancas(Si,professores,disponibilidade)
    SBv = copy(Si)
    orientador = composicao_banca[0,:]
 
    for i in range(nvizinho):
        Tabu = True
        while(Tabu == True):
            validador = True
            while(validador == True):           

                Linha = rd.sample(range(len(Si[:,0])),2)
                Coluna = rd.sample(range(len(Si[0,:])),2)
                v = np.array([Linha,Coluna])

                if(Si[v[0,0],v[1,0]]==orientador[v[1,0]] or Si[v[0,0],v[1,0]]==Si[0,v[1,0]] or Si[v[0,0],v[1,0]]==Si[1,v[1,0]] 
                    or Si[v[0,1],v[1,1]]==orientador[v[1,1]] or Si[v[0,1],v[1,1]]==Si[0,v[1,1]]
                    or Si[v[0,1],v[1,1]]==Si[1,v[1,1]]):
                    validador = True
                else:
                    validador = False

            for i in range(len(T)):
                if(v[0,0]!=T[i][0,0] or v[1,0]!=T[i][1,0] or v[0,1]!=T[i][0,1] or v[1,1]!=T[i][1,1]):
                    Tabu = False
                else:
                    Tabu = True

            Sv = copy(Si)
            x = Sv[v[0,0],v[1,0]]
            Sv[v[0,0],v[1,0]] = Sv[v[0,1],v[1,1]]
            Sv[v[0,1],v[1,1]] = x

            if (custo_bancas(Sv,professores,disponibilidade) < custo_best):
                SBv = copy(Sv)
                custo_best = custo_bancas(SBv,professores,disponibilidade)

    lista = [SBv, v]

    return lista

