#----------Composicao Inicial-------

Si = copy(horarios_banca)
horarios = list(range(len(orientadores)))
avaliador1 = []
avaliador2 = []

for horario in range(len(horarios)):
	orientadores_possiveis = copy(professores)
	orientadores_possiveis.remove(professores[professores.index(Si[horario])])
	print(orientadores_possiveis)
	avaliador1.append(rd.sample(orientadores_possiveis,1)[0])
	print(avaliador1)
	orientadores_possiveis.remove(avaliador1[horario])
	print(orientadores_possiveis)
	avaliador2.append(rd.sample(orientadores_possiveis,1)[0])

composicao_banca = np.array([horarios_banca,avaliador1,avaliador2])
custo = custo_bancas(composicao_banca,professores,disponibilidade)
#print(custo)

#------------------------------------

nvizinho = 5
Lt = 10
BTmax = 1000

solucao = True
while(solucao == True):
	resultado_heuristica = tabu_composicao(composicao_banca,professores,disponibilidade,nvizinho,Lt,BTmax)
	agenda_bancas = resultado_heuristica[0]
	for i in range(len(agenda_bancas[0,:])):
		if (horarios_banca[i]==agenda_bancas[0,i] or horarios_banca[i]==agenda_bancas[1,i]):
			solucao = True
			break
		else:
			solucao = False

c = np.array([composicao_banca[0],agenda_bancas[0],agenda_bancas[1]])
resultado_heuristica = tabu_composicao(c,professores,disponibilidade,nvizinho,Lt,BTmax)