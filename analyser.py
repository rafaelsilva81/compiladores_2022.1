import re
import pprint
from errors import incompTypes, notDeclared, outOfScope
from lexical.lexer import tokenize #Importação do analisador léxico trabalho 01

""" 
    Classe para tratamento de Erros semanticos
    Essa classe ASSUME que não há nenhum erro léxico ou sintático nos Tokens
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
                    'returnType' : 'VARINT',
                    'parameters' : ['VARINT', 'VARINT']
                }
            }

        """
        self.lineCount = 0
        self.previousScope = "global" #Define o escopo anterior
        self.currentScope = "global" #Define o escopo atual
        self.declaredVariables = {}
        self.declaredFunctions = {}

    def semanticTest(self, content):
        self.lineCount = 1
        for line in content:
            self.checkLine(tokenize(line))
            self.lineCount += 1

    def getValType(self, declaration):
        x = re.findall(r'(NUMBER|WORD)', ''.join(declaration))
        return x

    #Entrada : VARTYPE esperado e array de VARVALUES recebidos
    def checkCompatibleType(self, expectedType, receivedValues, var_id):
        for received in receivedValues:
            if (self.VALCOMB[expectedType] != received):
                incompTypes(expectedType, var_id, self.lineCount)
                return False
        return True

    def checkIds(self, declaredType, ids, var_id):
        if (ids != []):
            #Checar variaveis atribuidas a outra variavel (exemplo : int x = a + b;)
            #Esse bloco do código irá checar se essa invocação de a e b é correta   
            for i in ids:
                #Iterar sobre os ids encontrados na declaração da variável
                if(i not in self.declaredVariables): 
                    #Variável não declarada
                    notDeclared(var_id, i, self.lineCount)
                    return False
                elif(self.declaredVariables[i]['scope'] != self.currentScope and self.declaredVariables[i]['scope'] != self.previousScope): 
                    #Variaveis em escopos diferentes
                    outOfScope(var_id, i, self.lineCount)
                    return False
                elif(self.VALCOMB[declaredType] != self.VALCOMB[self.declaredVariables[i]['type']]):
                    #A variavel declarada tem tipos incompativeis com a variavel que lhe foi atribuida
                    incompTypes(self.VALCOMB[declaredType], var_id, self.lineCount)
                    return False
        return True
                    
    def getId(self, tokenArr):
        x = re.findall(r'ID\([A-Za-z]+[A-Za-z0-9#]*\)', ''.join(tokenArr))
        return x

    # Entrada : array de tokens
    # Essa função checa a linha, decidindo o que deve ser feito em seguida
    def checkLine(self, tokenArr):
        # CASO 1 --> LINHA VAZIA
        if (tokenArr == []): return
        # CASO 1 --> DECLARAÇÃO DE NOVO VARTYPE (var ou funcao)
        if (tokenArr[0] in self.VARTYPES): #Uma variável foi declarada

            # ------- Casos onde o ID é uma função ----------- #
            if ('LBRACKET' in tokenArr): #Abertura de chaves encontrada, a linha é uma função

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
        elif(self.getId(tokenArr) != []): #A linha possui um ou mais IDS
            #A linha não possui a abertura de uma função nem uma definição de tipo
            if(('LBRACKET' not in tokenArr) and ('VARINT' not in tokenArr) and ('VARSTRING' not in tokenArr)): 
                # ------- Casos onde a chamada é um retorno de função ----------- #
                if ('RETURN' in tokenArr):
                    scope = self.currentScope
                    if (scope != 'global'):
                        func = self.declaredFunctions[scope]
                        functionType = func['type'] #Pega o tipo esperado do escopo atual
                        ids = self.getId(tokenArr) #Obter todos os ids da linha
                        self.checkIds(functionType, ids, scope)

    def addDeclaredVariable(self, line):
        declaredType = line[0] #Tipo declarado
        var_id = line[1] #Id da variável
        declaration = line[3:] #Declaração
        var_detail = {'type': declaredType, 'scope':self.currentScope} #Detahes da variável
        ids = self.getId(declaration) #Obter os ids dentro da declaração
        if (ids != []): #A variavel é declarada como outra variável (exemplo : int x = a;)
            
            valType = self.getValType(declaration)
            self.checkCompatibleType(declaredType, valType, var_id)

            self.checkIds(declaredType, ids, var_id)
            
            self.declaredVariables[var_id] = var_detail
        
        elif (('NUMBER' in declaration) or ('WORD' in declaration)):
                #A variável declarada como um id e algum valor (exemplo : int x = a + 2;)
                valType = self.getValType(declaration)
                x = self.checkCompatibleType(declaredType, valType, var_id)
                if(x is True): 
                    self.declaredVariables[var_id] = var_detail 
        else:
            #Variável declarada, sem valor atriubido (exemplo : int x;)
            self.declaredVariables[var_id] = var_detail

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
    
if __name__ == "__main__":
    main()