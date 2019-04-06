from funcoes import *
from importar_csv import *
import numpy as np

print('Informacoes Base')
dados_horarios = importar_disponibilidade()
orientadores = importar_orientadores()

orientadores = np.array(orientadores[0]).tolist()
disponibilidade = dados_horarios[0]
dados_geral = dados_horarios[1]
quantidade_professores = dados_horarios[2]
quantidade_horarios = dados_horarios[3]
quantidade_bancas = len(orientadores)
professores = np.array(dados_geral[:,1]).tolist()

print(disponibilidade)
print('--------')
print(dados_geral)
print('--------')
print("bancas",quantidade_bancas)
print('--------')
print("Prof",quantidade_professores)
print('--------')
print("Horarios",quantidade_horarios)
print('--------')
print(orientadores)
print('--------')

print('Busca em Trajetória - Si')
composicao = busca_trajetoria(dados_horarios,orientadores)
custo = custo1(disponibilidade,orientadores,composicao, professores)

dict_Si = {}
for i in range(quantidade_bancas):
    dict_Si["%s Banca %s" %(orientadores[i],i+1)] = composicao[i]

print(dict_Si)
print(composicao)
print(custo)
print('--------')

print('Busca Tabu - Melhoria banca')
#Parametros
#-------------
Si = copy(composicao)
qtd_swaps = 2
BTmax = 1000
nvizinho = 5
Lt = 10
#-------------

tabu = tabu(disponibilidade, Si,BTmax,Lt, nvizinho, orientadores, professores)
print(tabu)
print(custo1(disponibilidade,orientadores,tabu[0], professores))
Sb = tabu[0]
dict_tabu = {}
for i in range(quantidade_bancas):
    dict_tabu["%s Banca %s" %(orientadores[i],i+1)] = composicao[i]

print('--------')

print('Conversão Horarios')

horarios = list(range(len(orientadores)))
horarios_banca = []
for horario in range(len(horarios)):
    banca = []
    banca.append(horario)
    banca.append(orientadores[Sb.index(horario)])
    horarios_banca.append(banca)

print(horarios_banca)