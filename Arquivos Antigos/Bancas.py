class Bancas(object):

    def __init__(self, banca, composicao, custo):
        self.__banca = [banca]
        self.__composicao = [composicao]
        self.__custo = [custo]



    def get_banca(self):
        return self.__banca

    def get_composicao(self,banca):
        return self.__composicao

    def get_custo(self,banca):
        return self.__custo