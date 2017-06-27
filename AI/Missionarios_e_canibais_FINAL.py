"""
### Sistema Especialista para solução do problema Missionários e Canibais, capaz de resolver o problema para ###
### N Missionários, N Canibais e k vagas no barco.                                                           ###

                 - Trabalho de Conclusão da disciplina de Inteligência Artificial -
                     # Criado e desenvolvido por Ângelo de Carvalho Paulino #
"""

#Importar as libraries itertools, random e os.
from itertools import product
from random import shuffle
from os import system

#Definindo a classe Operadores, responsável pelas funções de somar e subtrair "vetores de estado" e outras funções.
class Operadores():
    #Definindo o magic method "+" para possibilitar a soma entre estados e ações.
    def __add__(self, acao):
        return [(i+j) for i,j in zip(self.estado,acao)]

    # Definindo o magic method "-" para possibilitar a soma entre estados e ações.
    def __sub__(self, acao):
        return [(i-j) for i,j in zip(self.estado,acao)]

    #Gera todas as ações possíveis ("vetores operadores") para o conjunto de informações: nº de missionários, nº de canibais e capacidade do barco.
    def gera_acoes_possiveis(self):
        self.acoes_possiveis = [[i,j,1] for i,j in product(list(range(self.capacidade_barco+1)), repeat=2) if i+j<=self.capacidade_barco and i+j!=0]

    #Executa uma operação de soma ou subtração de um "vetor de estado" com um "vetor operador".
    def aplica_operacao(self,operador):
        if self.sinal == "+":
            return self+operador
        elif self.sinal == "-":
            return self-operador

    #Verifica se uma determinada operação levaria a um estado já visitado.
    def checa_repetido(self, operador):
        return True if self.aplica_operacao(operador) in self.anteriores else False

    #Aplica uma operação e seta o estado do objeto Estados para o novo estado.
    def grava_estado(self, operador):
        self.estado = self.aplica_operacao(operador)

    #Armazena um estado já visitado em uma lista de estados visitados (self.anteriores).
    def grava_estado_anterior(self):
        self.anteriores.append(self.estado)

    #Checa se o estado final foi alcançado.
    def checa_final(self):
        return True if self.estado == [0,0,0] else False

    #Realiza a mudança do sinal a ser aplicado ao operador
    def troca_sinal(self):
        if self.sinal == "+":
            self.sinal = "-"
        elif self.sinal == "-":
            self.sinal = "+"

    #Verifica se uma determinada jogada é legal
    def checa_legal(self,operador,outra_margem):
        movimento = self.aplica_operacao(operador)
        outra = outra_margem.aplica_operacao(operador)
        return True if movimento[0] in range(self.missionarios+1)\
                       and movimento[1] in range(self.canibais+1)\
                       and movimento[2] in range(self.posicao_barco+1)\
                       and (movimento[0] >= movimento[1] or movimento[0] == 0) \
                       and ((outra[0] >= outra[1] or outra[0] == 0)) else False

#Definindo a classe Jogo, responsável pela busca no espaço de estados.
class Jogo():
    def jogo_padrao(self,outra_margem):
        self.gera_acoes_possiveis()
        operacoes = self.acoes_possiveis
        iteracoes = 0
        shuffle(operacoes) #Esta operação é importante pois, uma vez que as ações possíveis são geradas automaticamente,
        # pode ser que alguma sequência de operações não permita chegar a um resultado. Assim, a cada iteração a
        # sequência é (em tese) alterada.
        outra_margem.troca_sinal()
        global sequencia_resposta
        sequencia_resposta = []
        while self.solucao_encontrada == False and iteracoes < len(self.acoes_possiveis)**3:
            for operador in operacoes:
                if self.checa_legal(operador,outra_margem) and not self.checa_repetido(operador):
                    self.grava_estado(operador)
                    self.grava_estado_anterior()
                    self.troca_sinal()
                    outra_margem.grava_estado(operador)
                    outra_margem.grava_estado_anterior()
                    outra_margem.troca_sinal()
                    sequencia_resposta.append(operador)

                if self.checa_final():
                    seq_resposta_formatada = [(i[0], j[1]) for i, j in zip(sequencia_resposta, sequencia_resposta)]
                    print("\nSolução encontrada!! Segue a sequência das operações à partir da margem inicial do rio:"
                          "\n{0}\nEm apenas {1} iteração(ões).".format(seq_resposta_formatada,iteracao))
                    self.solucao_encontrada = True
                    break
            iteracoes += 1

#Definindo a classe Estados, responsável criação dos respectivos objetos.
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

#Função que dá a formatação correta para a sequência de passos.
def imprime_resposta():
    print("\nSiga estes passos:\n")
    r = 2
    for i in sequencia_resposta:
        if r % 2 == 0:
            print("Passo {}:".format(int(r / 2)))
            print("Ida: {0} missionario(s) e {1} canibal(is)".format(i[0], i[1]))
        else:
            print("Volta: {0} missionario(s) e {1} canibal(is)\n".format(i[0], i[1]))
        r += 1
    print("\n")

#Função que coleta entrada de dados do usuário (pergunta/resposta).
def entradas_usuario():
    dados_ok = False
    while dados_ok == False:
        try:
            print("\nSugestão de jogo: 3 missionários, 3 canibais, barco com capacidade para 2 pessoas.\n")
            missionarios = canibais = int(input("Qual é a quantidade de missionários? (A quantidade de canibais será igual)\n"))
            capacidade_barco = int(input("Qual é a capacidade do barco?\n"))
            dados_ok = True
            return missionarios,canibais,capacidade_barco
        except:
            input("Valores informados incorretamente! Tente novamente inserindo apenas números inteiros e pressionando enter!")
            system("CLS")

#Função que verifica se o usuário deseja jogar novamente.
def repetir():
    dados_ok = False
    while dados_ok == False:
        try:
            repetir = input("\nDeseja jogar novamente? Digite \"s\" ou \"n\"\n").lower()
            if repetir == "s":
                dados_ok = True
                return True
            elif repetir == "n":
                dados_ok = True
                return False
        except:
            input("Valores informados incorretamente! Tente novamente inserindo apenas números inteiros e pressionando enter!")
            system("CLS")

#Função principal do jogo, que inicializa as variáveis e interage com o usuário.
def jogar():
    novo_jogo = True
    while novo_jogo == True:
        system("CLS")
        inicio = Estados([0, 0, 0], 0)
        print("\n### Sistema Especialista para solução do problema \"Missionários e Canibais\", capaz de ###\n"
              "### resolver o problema para N Missionários, N Canibais e k vagas no barco.           ###\n")
        print("- Trabalho de Conclusão da disciplina de Inteligência Artificial -\n")
        print("# Criado e desenvolvido por Ângelo de Carvalho Paulino #\n")
        dados = entradas_usuario()
        missionarios, canibais, capacidade_barco = dados
        global iteracao
        iteracao = 0
        while inicio.solucao_encontrada==False:
            inicio = Estados([missionarios,canibais,1],capacidade_barco)
            fim = Estados([0,0,0],2)
            inicio.jogo_padrao(fim)
            iteracao += 1
            if iteracao == missionarios**3:
                print(" Limite de tentativas excedido. Talvez a travessia não seja possível para os dados informados.")
                break
        if inicio.solucao_encontrada == True:
            imprime_resposta()
        novo_jogo = repetir()

#Define a função princinpal do programa como sendo a função "jogar()" e a chama para dar início ao jogo.
if __name__ == "__main__":
    jogar()