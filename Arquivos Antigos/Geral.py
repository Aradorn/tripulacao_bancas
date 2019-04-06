import pandas as pd
import random
import numpy as np

dados_df = pd.read_csv('Questionario Bancas.csv')
dados_df = dados_df.replace('Posso',int(0))
dados_df = dados_df.replace('Não Posso',int(100))
dados_df = dados_df.replace('Impossível',int(1000))

dados = dados_df.values
dados = dados[:,2:len(dados[0])]

quantidade_bancas = int(len(dados[0]))
quantidade_professores = int(len(dados[:,1]))

print('Bancas', quantidade_bancas)
print('Professores', quantidade_professores)

solucao_inicial = []
randBinList = lambda n: [randint(0,1) for b in range(1,n+1)]
for professor in range(quantidade_professores):
    linha = []
    for banca in range(quantidade_bancas):
        linha.append(random.randint(0,1))
    solucao_inicial.append(linha)
solucao_inicial = np.array(solucao_inicial)

print(solucao_inicial)

print(solucao_inicial[2,3])
print(sum(solucao_inicial[:,3]))

for banca in range(quantidade_bancas):
    for professor in range(quantidade_professores):
        if(sum(solucao_inicial[:,banca])<3):
            solucao_inicial[professor,banca] = 1
        elif (sum(solucao_inicial[:,banca])>3):
            solucao_inicial[professor,banca] = 0

print(solucao_inicial)
print(dados)

valor = []
for banca in range(quantidade_bancas):
    linha = []
    for professor in range(quantidade_professores):
        linha.append(solucao_inicial[professor,banca]*dados[professor,banca])
    valor.append(linha)
valor = np.array(valor)
soma1 = sum(valor)
custo_inicial = sum(soma1)

print(valor)
print("soma1",soma1, "soma2", custo_inicial)


