from itertools import product
from random import shuffle

class Operadores():
    #Definindo o magic method "+" para possibilitar a soma entre estados e ações
    def __add__(self, acao):
        return [(i+j) for i,j in zip(self.estado,acao)]

    # Definindo o magic method "-" para possibilitar a soma entre estados e ações
    def __sub__(self, acao):
        return [(i-j) for i,j in zip(self.estado,acao)]

    #Gera todas as ações possíveis para o conjunto de informações: nº de missionários, nº de canibais e capacidade do barco.
    def gera_acoes_possiveis(self):
        self.acoes_possiveis = [[i,j,1] for i,j in product(list(range(self.capacidade_barco+1)), repeat=2) if i+j<=self.capacidade_barco and i+j!=0]

    def aplica_operacao(self,operador):
        if self.sinal == "+":
            return self+operador
        elif self.sinal == "-":
            return self-operador

    def checa_repetido(self, operador):
        return True if self.aplica_operacao(operador) in self.anteriores else False

    def grava_estado(self, operador):
        self.estado = self.aplica_operacao(operador)

    def grava_estado_anterior(self):
        self.anteriores.append(self.estado)

    #Verificar se uma determinada jogada é legal
    def checa_legal(self,operador,outra_margem):
        movimento = self.aplica_operacao(operador)
        outra = outra_margem.aplica_operacao(operador)
        return True if movimento[0] in range(self.missionarios+1)\
                       and movimento[1] in range(self.canibais+1)\
                       and movimento[2] in range(self.posicao_barco+1)\
                       and movimento[0] >= movimento[1] \
                       and ((outra[0] >= outra[1] or outra[0] == 0) or movimento[2] == 0) else False

                        # and (outra[0] >= outra[1] or outra[0] == 0) else False

    def checa_final(self):
        return True if self.estado == [0,0,0] else False

    def troca_sinal(self):
        if self.sinal == "+":
            self.sinal = "-"
        elif self.sinal == "-":
            self.sinal = "+"

class Jogo():
    def jogo_padrao(self,outra_margem):
        self.gera_acoes_possiveis()
        operacoes = self.acoes_possiveis
        iteracoes = 0
        shuffle(operacoes)
        outra_margem.troca_sinal()
        #print("Ações possíveis: {0}\nInício definido: {1}".format(self.acoes_possiveis,self.inicio))
        seq = []
        while self.solucao_encontrada == False and iteracoes < 300:
            for operador in operacoes:
                if self.checa_legal(operador,outra_margem) and not self.checa_repetido(operador):
                    self.grava_estado(operador)
                    self.grava_estado_anterior()
                    self.troca_sinal()
                    outra_margem.grava_estado(operador)
                    outra_margem.grava_estado_anterior()
                    outra_margem.troca_sinal()
                    seq.append(operador)
                    #print("Operador({3}): {1}; Estado margem: {0}; Outra margem: {2}".format(self.estado,operador,outra_margem.estado,self.sinal))

                if self.checa_final():
                    print("\nResultado encontrado!! Segue a sequência dos estados da margem inicial:")
                    print(seq)
                    self.solucao_encontrada = True
                    break
            iteracoes += 1

class Estados(Operadores,Jogo):
    def __init__(self, estado, capacidade_barco=2):
        self.estado = self.inicio = estado
        self.anteriores = []
        self.missionarios = estado[0]
        self.canibais = estado[1]
        self.posicao_barco = estado[2]
        self.capacidade_barco = capacidade_barco
        self.acoes_possiveis = []
        self.solucao_encontrada = False
        self.grava_estado_anterior()
        self.sinal = "-"

inicio = Estados([0,0,0],3)
missionarios = canibais = 3#int(input("Qual é a quantidade de missionários?\n"))
capacidade_barco = 2#int(input("Qual é a capacidade do barco?\n"))
iteracao = 0

while inicio.solucao_encontrada==False:
    inicio = Estados([missionarios,canibais,1],capacidade_barco)
    fim = Estados([0,0,0],2)
    inicio.jogo_padrao(fim)
    iteracao += 1
    if iteracao == 300:
        print(" A travessia não é possível para os dados inseridos.")
        break

#[[1,1,1],[1,0,1],[0,2,1],[0,1,1],[2,0,1],[1,1,1],[2,0,1],[0,1,1],[0,2,1],[0,1,1],[0,2,1]]