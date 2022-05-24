import re
import pprint
from errors import argIncompTypes, incompTypes, notDeclared, outOfScope, paramCountErr
from lexical.lexer import tokenize #Importação do analisador léxico trabalho 01

""" 
    Classe para tratamento de Erros semanticos
    Essa classe ASSUME que não há nenhum erro léxico ou sintático no input do usuário
"""
class Semantic():

    VARTYPES = ['VARINT', 'VARSTRING'] #Define os tipos de variáveis diponíveis
    VALTYPES = ['NUMBER', 'WORD']
    VALCOMB = {
        'VARINT' : 'NUMBER',
        'VARSTRING' : 'WORD'
    } #Define os tipos de valor disponível, ligado com os tipos correspondentes

    def __init__(self):
        self.currentScope = 'global'
        self.previousScope = 'global'
    

    #Quebrar pontos e virgulas
    def breakLine(self, content):
        result = []
        for line in content:
            result += re.split('(.*?;)',line)
        return result

    def semanticTest(self, content):
        content = self.breakLine(content)
        for line in content:
            #print(tokenize(line))
            self.checkLine(tokenize(line))

    def checkLine(self, line):
        # TESTE 0 : Linha em branco
        if (line == []): return
        # TESTE 1 : O primeiro caractere da linha é um TIPO (String ou Int)
        elif (line[0] in self.VARTYPES):
            
            if('SEMICOLON' not in line and 'LBRACKET' in line and 'LPAREN' in line and 'RPAREN' in line and 'ASSIGN' not in line):
                """ CASO 1:
                    - Não há ponto e virgula
                    - Há chave abrindo
                    - Há parenteses abrindo e fechando
                    - Não há atribuição
                -> DECLARAÇÃO DE FUNÇÃO """
                print('declaracao de funcao')
                print(line)
            
            elif('ASSIGN' in line):
                """ CASO 2:
                    - Há uma atribuição
                -> DECLARAÇÃO E ATRIBUIÇÃO DE VARIAVEL """
                print('declaracao e atribuicao')
                print(line)

            else:
                """ CASO 3:
                    - Não há atribuição
                    - Assumindo que não há erros lexicos e semanticos
                -> DECLARAÇÃO DE VARIAVEL SEM ATRIBUIÇÃO """
                print('declaracao sem atribuicao')
                print(line)
        # TESTE 2 : O primeiro caractere da linha é um ID
        elif (re.match(r'ID\(.*?\)', line[0])):
            print("a")
def main():
    s = Semantic()
    with open('input.txt', encoding='utf8') as f:
        content = f.readlines()
    
    s.semanticTest(content)
    
    print("\n  SUCESSO!")

if __name__ == "__main__":
    main()