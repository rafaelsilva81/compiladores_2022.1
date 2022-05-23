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

        """ 
            Formatos
            declaredVariables = {
                'ID(a)' : {
                    type : 'VARINT',
                    scope : 'global'
                },
                'ID(nome)' : {
                    type : 'VARINT',
                    scope : 'main'
                }
            }

            declaredFunctions = {
                'ID(somar)' : {
                    'type' : 'VARINT',
                    'parameters' : ['VARINT', 'VARINT']
                }
            }

        """
        self.ignoreRbrackets = 0
        self.lineCount = 0
        self.previousScope = "global" #Define o escopo anterior
        self.currentScope = "global" #Define o escopo atual
        self.declaredVariables = {}
        self.declaredFunctions = {}

    def semanticTest(self, content):
        self.lineCount = 1
        for line in content:
            #print(tokenize(line))
            self.checkLine(tokenize(line))
            self.lineCount += 1

    def getIds(self, declaration):
        x = re.findall(r'ID\([A-Za-z]+[A-Za-z0-9#]*\)', ''.join(declaration))
        return x
        
    # Entrada : array de tokens
    # Essa função checa a linha, decidindo o que deve ser feito em seguida
    def checkLine(self, tokenArr):
        # CASO 1 --> LINHA VAZIA
        if (tokenArr == []): return
        # CASO 1 --> DECLARAÇÃO DE NOVO VARTYPE (var ou funcao)
        if (tokenArr[0] in self.VARTYPES): #Um vartype foi declarado no começo da linha

            # ------- Casos onde o ID é uma função ----------- #
            if ('LBRACKET' in tokenArr and ('MATH_OP' not in tokenArr or 'ASSIGN' not in tokenArr)): 
                #Abertura de chaves encontrada
                #Não ha atribuição ou operação matematica linha é uma função
                self.previousScope = self.currentScope #Define o antigo escopo
                self.currentScope = tokenArr[1] #Definição do escopo atual
    
                
                lparen_idx = tokenArr.index('LPAREN')
                rparen_idx = tokenArr.index('RPAREN')
                funcionArguments = tokenArr[lparen_idx+1:rparen_idx] #Pega apenas o que está entre os parenteses
                if ('COMMA' in funcionArguments):
                    comma_idx = funcionArguments.index('COMMA')
                    parameters = [funcionArguments[0:comma_idx], funcionArguments[comma_idx+1:len(funcionArguments)]]
                else:
                    parameters = [funcionArguments]
                
                paramTypes = []
                if parameters != [[]]: #Se a função tiver parametros
                    for parameter in parameters:
                        paramTypes.append(parameter[0])
                        self.addDeclaredVariable(parameter)
                
                
                functionDetails = {'type' : tokenArr[0], 'parameters': paramTypes}
                self.declaredFunctions[tokenArr[1]] = functionDetails
            # ------- Casos onde o ID é um valor ------------- #
            elif ('ASSIGN' in tokenArr): #Variável ja inicializada na mesma linha da declaração (formato VAR ID ASSIGN VALUE)
                self.addDeclaredVariable(tokenArr)
            else: #Variável não inicializada
                self.addDeclaredVariable(tokenArr)
        # CASO 2 --> FECHAMENTO DE UM ESCOPO (de uma funcao)
        elif(tokenArr[0] == 'RBRACKET'): #Fechamento do escopo
            aux = self.currentScope
            self.currentScope = self.previousScope
            self.previousScope = aux
        # CASO 3 --> CHAMADA DE VARTYPE JÁ DEFINIDA (var ou func)
        elif(self.getIds(tokenArr) != []): #A linha possui um ou mais IDS
            #A linha não possui a abertura de uma função nem uma definição de tipo
            if(('LBRACKET' not in tokenArr) and ('VARINT' not in tokenArr) and ('VARSTRING' not in tokenArr)): 
                ids = self.getIds(tokenArr) #Obter todos os ids
                functions = self.getFunctions(ids)
                variables = self.getVariables(ids)
                # Checar se algum dos ids é uma variavel/função não declarada
                for i in ids:
                    if i not in functions and i not in variables:
                        notDeclared(i, self.lineCount)
                # Caso existe alguma função, obter os argumentos enviados dessa função
                if functions != []:
                    for f in functions:
                        self.checkFunctionArguments(f, tokenArr)
                if variables != []:
                    for v in variables:
                        var_scope = self.declaredVariables[v]['scope']
                        if (var_scope != self.currentScope and var_scope != 'global'):
                            outOfScope(v, self.lineCount)
                # ------- Casos onde a chamada é um retorno de função ----------- #

    def addDeclaredVariable(self, line):
        declaredType = line[0] #Tipo declarado
        var_id = line[1] #Id da variável
        declaration = line[3:] #Declaração
        var_detail = {'type': declaredType, 'scope':self.currentScope} #Detahes da variável
        ids = self.getIds(declaration) #Obter os ids dentro da declaração
        if (ids != []): #A variavel é declarada como outra variável (exemplo : int x = a;)
            
            if (('NUMBER' in declaration) or ('WORD' in declaration)):
                #A variável declarada como um id e algum valor (exemplo : int x = a + 2;)
                if((declaredType == 'VARINT' and 'WORD' in declaration)): # VARINT declarada recebeu uma string (incompativel)
                    incompTypes(expectedType='VARINT', var=var_id, line=self.lineCount)

            #Checar variaveis atribuidas a outra variavel (exemplo : int x = a + b;)
            #Esse bloco do código irá checar se essa invocação de a e b é correta   
            for i in ids:
                #Iterar sobre os ids encontrados na declaração da variável
                if(i not in self.declaredVariables): 
                    #Variável não declarada
                    notDeclared(i, self.lineCount)
                elif(self.declaredVariables[i]['scope'] != self.currentScope and self.declaredVariables[i]['scope'] != self.previousScope): 
                    #Variaveis em escopos diferentes
                    outOfScope(var_id, self.lineCount)
                elif(self.VALCOMB[declaredType] != self.VALCOMB[self.declaredVariables[i]['type']]):
                    #A variavel declarada tem tipos incompativeis com a variavel que lhe foi atribuida
                    incompTypes(self.VALCOMB[declaredType], var_id, self.lineCount)
            self.declaredVariables[var_id] = var_detail
        
        elif (('NUMBER' in declaration) or ('WORD' in declaration)):
                #A variável declarada como um id e algum valor (exemplo : int x = a + 2;)
                if((declaredType == 'VARINT' and 'WORD' in declaration)): # VARINT declarada recebeu uma string (incompativel)
                    incompTypes('VARINT', var_id, self.lineCount)
                else:
                    self.declaredVariables[var_id] = var_detail 
        else:
            #Variável declarada, sem valor atriubido (exemplo : int x;)
            self.declaredVariables[var_id] = var_detail

    """ Função auxiliar que recebe um array de ids
    e retorna todos ids que representam uma função declarada """
    def getFunctions(self, idArr):
        functions = []
        for varid in idArr:
            if varid in self.declaredFunctions:
                functions.append(varid)
        return functions

    """ Função auxiliar que recebe um array de ids
    e retorna todos ids que representam uma variável declarada """
    def getVariables(self, idArr):
        variables = []
        for varid in idArr:
            if varid in self.declaredVariables:
                variables.append(varid)
        return variables

    def checkFunctionArguments(self, function, line):
        func_idx = line.index(function) #Pega o index de onde está o id da função na linha
        declaration = line[func_idx+2:line.index('RPAREN')+1] #Pega a declaração do caractere seguinte ao ID da função até o primeiro ')'
        aux = declaration
        if ('LPAREN' in declaration):
            idx = declaration.index('LPAREN')
            declaration = declaration[:idx]
        received_ids = self.getIds(declaration)
        received_params = [s for s in declaration if s in received_ids or s == 'NUMBER' or s == 'WORD']
        expected_params = self.declaredFunctions[function]['parameters']
        for i in range(len(expected_params)):
            if received_params[i] in received_ids: #Se o argumento se trata de um ID
                if (received_params[i] in self.declaredFunctions):
                    self.checkFunctionArguments(received_params[i], aux)
                    received_params[i] = self.declaredFunctions[received_params[i]]['type'] #Transformar o id no tipo dele
                     #Se trata de uma funcao
                else:
                    scope = self.declaredVariables[received_params[i]]['scope']
                    if (scope != self.currentScope and scope != 'global'):
                        outOfScope(received_params[i], self.lineCount)
                    received_params[i] = self.declaredVariables[received_params[i]]['type'] #Transformar o id recebido no tipo dele
            else: #O argumento recebido não é um ID
                if (received_params[i] == 'WORD'):
                    received_params[i] = "VARSTRING" #Obter tipo de acordo
                elif(received_params[i] == 'NUMBER'):
                    received_params[i] = "VARINT"
            
            if received_params[i] != expected_params[i]:
                argIncompTypes(expected_params[i], i, function, self.lineCount)

            if ((len(received_params)) != len(expected_params)):
                paramCountErr(function, self.lineCount)
            


def main():
    separated = []
    content = []
    s = Semantic()
    with open('input.txt', encoding='utf8') as f:
        content = f.readlines()
    
    s.semanticTest(content)

    print("\n Variáveis declaradas : ")
    pprint.pprint(s.declaredVariables, sort_dicts=False) #Pretty print
    print("\n Funções declaradas : ")
    pprint.pprint(s.declaredFunctions, sort_dicts=False)
    
    print("\n  SUCESSO!")
if __name__ == "__main__":
    main()