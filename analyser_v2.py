import re
import pprint
import uuid

from black import Line
from errors_v2 import argIncompTypes, impossibleOperation, incompTypes, notDeclared, outOfScope, paramCountErr
from lexical.lexer import tokenize #Importação do analisador léxico trabalho 01

""" 
    Classe para tratamento de Erros semanticos
    Essa classe ASSUME que não há nenhum erro léxico ou sintático no input do usuário
"""
class Semantic():
    GLOBALSCOPE = 'global'
    VARTYPES = ['VARINT', 'VARSTRING'] #Define os tipos de variáveis diponíveis
    PRIMITIVES = ['NUMBER', 'WORD']
    RELATION = {
        'VARINT' : 'NUMBER',
        'VARSTRING' : 'WORD'
    } #Define os tipos de valor disponível, ligado com os tipos correspondentes

    def __init__(self):
        """
            declaredVariables = {
                ID(a): {
                    ID(main) : 'VARSTRING',
                    ID(fun) : 'VARINT'
                }
            }

            declaredScopes = {
                ID(scopename): {
                    'type' : 'VARINT'
                    'reachableScopes': [array of reachable scopes]
                }
            }
        """
        self.declaredVariables = {}
        self.declaredScopes = {}
        self.currentScope = 'global'
        self.previousScope = 'global'
        self.scopeBracket = 0
        
        #Inicialização de escopos
        globalScopeDetails = {} 
        globalScopeDetails['type'] = 'VOID'
        globalScopeDetails['reachableScopes'] = [self.GLOBALSCOPE]
        self.declaredScopes[self.GLOBALSCOPE] = globalScopeDetails

    
    #Recebe uma linha já identificada como um ELSE
    def elseStatement(self, line):
        uid = "ELSE_"+str(uuid.uuid4())[:3]
        self.changeScope(scope=uid)
        
    #Recebe uma linha já identificada como um IF
    def ifStatement(self, line):
        ids = self.getIdsFromDeclaration(line)
        for i in ids:
            if i not in self.declaredScopes and i not in self.declaredVariables:
                notDeclared(i)
        uid = "IF_"+str(uuid.uuid4())[:3]
        self.changeScope(scope=uid)

    #Retorna todos os primitivos (NUMBER, WORD) de uma declaração
    def getPrimitivesFromDeclaration(self, declaration):
        p = []
        for token in declaration:
            if token == 'WORD' or token == 'NUMBER':
                p.append(token)
        return p

    #Retorna todos os IDS de uma declaração
    def getIdsFromDeclaration(self, declaration):
        x = re.findall(r'ID\(.*?\)', ''.join(declaration))
        return x
    
    #Muda o escopo
    def changeScope(self, scope=str(uuid.uuid4())[:3], scopetype='VOID'):
        #print(self.previousScope + " -> " + self.currentScope + " -> " + scope)
        previousReachable = self.declaredScopes[self.currentScope]['reachableScopes']
        newScopeDetails = {}
        newScopeDetails['type'] = scopetype
        newScopeDetails['reachableScopes'] = [scope] + previousReachable
        self.declaredScopes[scope] = newScopeDetails
        self.previousScope = self.currentScope
        self.currentScope = scope
        #print(self.previousScope + " > " + self.currentScope)

    def closeScope(self):
        aux = self.currentScope
        self.currentScope = self.previousScope
        self.previousScope = aux
       
    #Recebe uma linha que já foi identificada como uma função
    #Formato --> (VARINT ID(func) LPAREN ID(a) COMMA ID(b) RPAREN LBRACKET)
    def functionDeclaration(self, line):
        ids = self.getIdsFromDeclaration(line)
        self.changeScope(scope=ids[0], scopetype=line[0]) #Usa o primeiro ID da linha como referencia do novo escopo

    #Recebe uma linha que já foi identificada como uma declaração de variável
    #assign == True --> variavel declarada e atribuida
    #assign == False --> variavel declarada sem atribuicao
    #Formato --> (VARINT ID(a) ASSIGN NUMBER SEMICOLON)
    def variableDeclaration(self, line, assign=False):
        var = self.getIdsFromDeclaration(line)[0] 
        vartype = line[0]
        if (assign):
            declaration = line[line.index('ASSIGN')+1:line.index('SEMICOLON')]
            ids = self.getIdsFromDeclaration(declaration)
            primitives = self.getPrimitivesFromDeclaration(declaration)
            if (vartype == 'VARSTRING'):
                if ('MATH_OP' in line):
                    impossibleOperation(var)
            if (ids != []):
                for i in ids:
                    self.checkIdForVariable(vartype, var, i)
            if (primitives != []):
                for p in primitives:
                    self.checkPrimitiveForVariable(vartype, var, p)
        vardetails = {}
        vardetails[self.currentScope] = vartype
        if (var in self.declaredVariables):
            d1 = self.declaredVariables[var]
            d1.update(vardetails)
        else:
            self.declaredVariables[var] = vardetails

    #Recebe um ID e um TIPO que estão sendo usados em uma declaração
    #Checa se esse id existe, e se os tipos são compativeis     
    def checkIdForVariable(self, vartype, var, id):
        if id in self.declaredVariables:
            if (self.currentScope in self.declaredVariables[id]):
                received_type = self.declaredVariables[id][self.currentScope]
            elif(self.GLOBALSCOPE in self.declaredVariables[id]):
                received_type = self.declaredVariables[id][self.currentScope]
        elif (id in self.declaredScopes):
            received_type = self.declaredScopes[id]
        else: 
            notDeclared(id)
        if (received_type != vartype):
                print(received_type)
                incompTypes(vartype, var)
    
    def checkPrimitiveForVariable(self, vartype, var, prim):
        #Transformar primitivo em tipo
        received_type = self.VARTYPES[self.PRIMITIVES.index(prim)]
        if (received_type != vartype):
            incompTypes(vartype, var)

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
        if (line == []): 
            pass
        # TESTE 1 : O primeiro caractere da linha é um TIPO (String ou Int)
        elif (line[0] in self.VARTYPES):
            
            if('SEMICOLON' not in line and 'LBRACKET' in line and 'LPAREN' in line and 'RPAREN' in line and 'ASSIGN' not in line):
                """ CASO 1:
                    - Não há ponto e virgula
                    - Há chave abrindo
                    - Há parenteses abrindo e fechando
                    - Não há atribuição
                -> DECLARAÇÃO DE FUNÇÃO """
                self.functionDeclaration(line)
            
            elif('ASSIGN' in line and 'SEMICOLON' in line):
                """ CASO 2:
                    - Há uma atribuição
                -> DECLARAÇÃO E ATRIBUIÇÃO DE VARIAVEL """
                self.variableDeclaration(line, assign=True)

            else:
                """ CASO 3:
                    - Não há atribuição
                    - Assumindo que não há erros lexicos e semanticos
                -> DECLARAÇÃO DE VARIAVEL SEM ATRIBUIÇÃO """
                self.variableDeclaration(line)
        # TESTE 2 : Há uma chamada para um IF
        elif (line[0] == 'IF' and 'LBRACKET' in line and 'LPAREN' in line and 'RPAREN' in line):
            #self.scopeBracket += 1
            self.ifStatement(line)
        # TESTE 3 : Há uma chamada para um ELSE
        elif (line[0] == 'ELSE' and 'LBRACKET' in line):
            #self.scopeBracket += 1
            self.elseStatement(line)
        # TESTE 4 : O primeiro caractere da linha é uma CHAVE FECHANDO
        elif (line[0] == 'RBRACKET'):
            #Isso indica o fechamento do escopo atual
            self.closeScope() #Volta ao escopo anterior
        # TODO TESTE 5 : O primeiro caractere da linha é um ID
        elif (re.match(r'ID\(.*?\)', line[0])):
            if ('ASSIGN' in line):
                print('todo')
                """ CASO 1:
                    - Há atribuição
                -> ATRIBUIÇÃO DE VALOR A VARIAVEL JA DECLARADA"""
                #self.attributeVariable(Line)
            
def main():
    s = Semantic()
    with open('input.txt', encoding='utf8') as f:
        content = f.readlines()
    
    s.semanticTest(content)
    
    print("\n Variáveis declaradas : ")
    pprint.pprint(s.declaredVariables, sort_dicts=False) #Pretty print
    print("\n Escopos declarados : ")
    pprint.pprint(s.declaredScopes, sort_dicts=False)

    print("\nSUCESSO!")

if __name__ == "__main__":
    main()