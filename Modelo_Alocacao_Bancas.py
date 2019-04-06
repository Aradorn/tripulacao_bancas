#!/usr/bin/env python
# coding: utf-8

# <h3>Pacotes

# In[594]:


import numpy as np
import pandas as pd


# <h3> Funções

# In[628]:


#Funções Custo
def custo_bancas(composicao_banca,professores,disponibilidade):
    custo = 0
    for banca in range(len(composicao_banca[0,:])):
        for professor in range(len(composicao_banca[:,0])-1):
            custo_professor = disponibilidade[professores.index(composicao_banca[professor,banca]),banca]+(composicao_banca == composicao_banca[professor,banca]).sum()
            custo = custo + custo_professor
    return custo

def custo_real(composicao_banca,professores,disponibilidade):
    custo = 0
    for banca in range(len(composicao_banca[0,:])):
        for professor in range(len(composicao_banca[:,0])-1):
            custo_professor = disponibilidade[professores.index(composicao_banca[professor,banca]),banca]
            custo = custo + custo_professor

    return custo

def custo_orientadores(tabela,orientadores,composicao, professores):
    quantidade_bancas = len(orientadores)
    custo_interno = 0
    for banca in range(quantidade_bancas):
        orientador_banca = professores.index(orientadores[banca])
        custo_interno = custo_interno + tabela[orientador_banca, composicao[banca]]
    return custo_interno


# In[622]:


#Funções Ordenação
def dicionario_orientadores(composicao,quantidade_bancas,orientadores,orientandos):
    dict_Si = {}
    for i in range(quantidade_bancas):
        dict_Si["%s Banca %s, Orientando: %s" %(orientadores[i],i+1, orientandos[i])] = composicao[i]
    
    return dict_Si

def dic_orientandos_horarios(Sb,orientadores,orientandos):
    horarios = list(range(len(orientadores)))
    horarios_banca = []
    for horario in range(len(horarios)):
        horarios_banca.append(orientandos[Sb.index(horario)])
    return horarios_banca

def dic_orientadores_horarios(Sb,orientadores,orientandos):
    horarios = list(range(len(orientadores)))
    horarios_banca = []
    for horario in range(len(horarios)):
        banca = []
        banca.append(horario)
        banca.append(orientadores[Sb.index(horario)])
        banca.append(orientandos[Sb.index(horario)])
        horarios_banca.append(banca)

    return horarios_banca


# In[623]:


#Funções Heuristicas
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

def tabu_orientadores(disponibilidade, Si, BTmax, Lt, nvizinho, orientadores, professores):

    Sb = copy(Si)
    melhor_iter = 0
    qtd_swaps = 2
    T = np.zeros((Lt,qtd_swaps),dtype=np.int)

    tempo = timeit.default_timer()
    iter = 0

    while((iter - melhor_iter) < BTmax):
        iter = iter + 1
        lista = swap_orientadores(disponibilidade, Sb, T, nvizinho, qtd_swaps,orientadores, professores)
        Sv = lista[0]
        for i in reversed(range(Lt)):
            T[i] = T[i - 1]
        T[0,] = lista[1]
        if custo_orientadores(disponibilidade,orientadores,Sv, professores) < custo_orientadores(disponibilidade, orientadores, Sb, professores):
            Sb = Sv
            melhor_iter = copy(iter)
            if (custo_orientadores(disponibilidade, orientadores, Sb, professores) == 0):
                melhor_iter = iter+BTmax

    tempo = timeit.default_timer()- tempo
    lista = [Sb,tempo]

    return lista

def swap_orientadores(disponibilidade, Si, T, nvizinho, qtd_swaps, orientadores, professores):

    custo_best = custo_orientadores(disponibilidade, orientadores, Si, professores)
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
        if (custo_orientadores(disponibilidade,orientadores, Sv, professores) < custo_best):
            SBv = Sv
            custo_best = custo_orientadores(disponibilidade,orientadores, Sv, professores)

    lista = [SBv, v]

    return lista


# In[639]:


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

        if custo_real(Sv,professores,disponibilidade) < custo_real(Sb,professores,disponibilidade):
            Sb = copy(Sv)
            melhor_iter = copy(iter)
            if (custo_real(Sb,professores,disponibilidade) == 0):
                melhor_iter = iter+BTmax
    custo = custo_real(Sb,professores,disponibilidade)
    tempo = timeit.default_timer()- tempo
    lista = [Sb,tempo,custo]

    return lista

def swap_composicao(Si,professores,disponibilidade,composicao_banca,nvizinho,T):

    custo_best = custo_real(Si,professores,disponibilidade)
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
                
                if(Si[v[0,0],v[1,0]]==orientador[v[1,0]] or Si[v[0,0],v[1,0]]==Si[1,v[1,0]] 
                    or Si[v[0,1],v[1,1]]==orientador[v[1,1]] or Si[v[0,1],v[1,1]]==Si[0,v[1,1]]):
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
            
            if (custo_real(Sv,professores,disponibilidade) < custo_best):
                SBv = copy(Sv)
                custo_best = custo_real(SBv,professores,disponibilidade)

    lista = [SBv, v]
    

    return lista


# <H3>Importação de Dados e Parâmetros

# In[603]:


#Disponibilidade Professores
dados_df = pd.read_csv('Disponibilidade Professores.csv')
dados_df = dados_df.replace('Disponível',int(0))
dados_df = dados_df.replace('Insdisponível',int(1))

dados_geral = dados_df.values
disponibilidade = dados_geral[:, 2:len(dados_geral[0])]
quantidade_horarios = int(len(dados[0]))
quantidade_professores = int(len(dados[:, 1]))
professores = np.array(dados_geral[:,1]).tolist()
horarios = dados_df.axes[1][2:].tolist()

#Orientadores & Orientandos
orientadores_df = pd.read_csv('Orientadores_Bancas.csv')
orientadores = orientadores_df.values
orientadores = np.array(orientadores[:,1:len(orientadores[0])]).tolist()[0]
orientandos = orientadores_df.axes[1]
orientandos = orientandos.drop(orientandos[0])
quantidade_bancas = len(orientadores)


#Parametros Tabu
qtd_swaps = 2
BTmax = 1000
nvizinho = 5
Lt = 10


# <h3> Definir Orientadores por Horários

# In[605]:


#Busca em Trajetória - Si Orientadores
horarios_bancas = busca_trajetoria(dados_horarios,orientadores)
custo = custo_orientadores(disponibilidade,orientadores,horarios_bancas, professores)
print("Custo Orientadores Trajetória: ", custo)


#Busca Tabu - Si Orientadores
Si = copy(horarios_bancas)
horarios_bancas = tabu_orientadores(disponibilidade, Si,BTmax,Lt, nvizinho, orientadores, professores)
Sb_orientadores = horarios_bancas[0]
print("Custo Orientadores Tabu: ",custo_orientadores(disponibilidade,orientadores,Sb_orientadores, professores))

dic_orientadores = dic_orientadores_horarios(Sb_orientadores,orientadores,orientandos)
dic_alunos = dic_orientandos_horarios(Sb,orientadores,orientandos)

#print(dic_horarios)

dic_alunos = dic_orientandos_horarios(Sb,orientadores,orientandos)

#Preparação para Composicao
h_banca = []
for horario in range(len(horarios)):
    h_banca.append(orientadores[Sb_orientadores.index(horario)])
dic_horarios


# <h3>Definir Composição Bancas

# In[638]:


#----------Composicao Bancas Inicial-------

Si = copy(h_banca)
horarios = list(range(len(orientadores)))
avaliador1 = []
avaliador2 = []
for horario in range(len(horarios)):
	orientadores_possiveis = copy(professores)
	orientadores_possiveis.remove(professores[professores.index(Si[horario])])
	avaliador1.append(rd.sample(orientadores_possiveis,1)[0])
	orientadores_possiveis.remove(avaliador1[horario])
	avaliador2.append(rd.sample(orientadores_possiveis,1)[0])
composicao_banca = np.array([h_banca,avaliador1,avaliador2])
custo = custo_bancas(composicao_banca,professores,disponibilidade)
print("Custo Generico: ", custo)
custo = custo_real(composicao_banca,professores,disponibilidade)
print("Custo Real: ", custo)


# In[647]:


#Heurística de Composicao Bancas
BTmax = 10000
nvizinho = 40
Lt = 30

while(solucao == True):
	resultado_heuristica = tabu_composicao(composicao_banca,professores,disponibilidade,nvizinho,Lt,BTmax)
	agenda_bancas = resultado_heuristica[0]
	for i in range(len(agenda_bancas[0,:])):
		if (horarios_banca[i]==agenda_bancas[0,i] or horarios_banca[i]==agenda_bancas[1,i]):
			solucao = True
			break
		else:
			solucao = False
resultado_heuristica = tabu_composicao(composicao_banca,professores,disponibilidade,nvizinho,Lt,BTmax)
agenda_bancas = resultado_heuristica[0].tolist()
banca_completa = np.array([h_banca,agenda_bancas[0],agenda_bancas[1]])
banca_completa_df = {"Orientador":h_banca,"Prof_Banca 1": agenda_bancas[0], "Prof_Banca 2":agenda_bancas[1]}


# <h3>Resultados

# In[649]:


#print(custo_bancas(banca_completa,professores,disponibilidade))
print("Custo Bancas: ",custo_real(banca_completa,professores,disponibilidade))

banca_completa_df = {"Horarios":horarios,"Alunos":dic_alunos,"Orientador":h_banca,"Prof_Banca 1": agenda_bancas[0], "Prof_Banca 2":agenda_bancas[1]}
banca_completa_df = pd.DataFrame(banca_completa_df).set_index("Horarios")
banca_completa_df


# In[ ]:




