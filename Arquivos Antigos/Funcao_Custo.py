def custo_bancas(tabela_bancas, banca, composicao_bancas,professores_geral):

    custo = 0
    for professor in range(len(composicao_bancas)):
        custo_professor = professores_geral.count(composicao_bancas[professor])*professores_geral.count(composicao_bancas[professor])
        custo = custo + tabela_bancas[composicao_bancas[professor],banca]+custo_professor
    return custo