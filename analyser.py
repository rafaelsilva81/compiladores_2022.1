import re #regex
import pprint #prettyprint
import uuid #ids aleatórios
import itertools #ferramentas de iteraçao
import os #ferramentas do sistema operacional

from errors import impossibleOperation, incompTypes, notDeclared, outOfScope, returnIncompTypes
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
        """ FORMATO DAS ESTRUTURAS DE DADOS:
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

        self.hasError = False
        self.declaredVariables = {}
        self.declaredScopes = {}
        self.currentScope = 'global'
        self.previousScope = 'global'
        
        #Inicialização de escopos
        globalScopeDetails = {} 
        globalScopeDetails['type'] = 'VOID'
        globalScopeDetails['reachableScopes'] = [self.GLOBALSCOPE]
        self.declaredScopes[self.GLOBALSCOPE] = globalScopeDetails

    def showScopesAndVariables(self):
        print("\n Variáveis declaradas : ")
        pprint.pprint(self.declaredVariables, sort_dicts=False) #Pretty print
        print("\n Escopos declarados : ")
        pprint.pprint(self.declaredScopes, sort_dicts=False)
        print("\n")

    def openBlock(self, line):
        uid = "BLOCK_"+str(uuid.uuid4())[:5] #id aleatorio para o bloco
        self.changeScope(uid)
        if(len(line) > 1):
            self.checkLine(line[1:])

    #Recebe uma linha já identificada como return
    def returnStatement(self, line):
        scope = self.currentScope
        while (re.match(r'IF_.*?', scope) or re.match(r'BLOCK_.*?', scope) or re.match(r'ELSE_.*?', scope)):
            #O escopo atual é um bloco ou if ou else
            reachable = self.declaredScopes[self.currentScope]['reachableScopes']
            idx = reachable.index(scope)
            scope = self.declaredScopes[self.currentScope]['reachableScopes'][idx+1]
        
        expectedType = self.declaredScopes[scope]['type']
        ids = self.getIdsFromDeclaration(line)
        primitives = self.getPrimitivesFromDeclaration(line)
        if (len(ids) > 0):
            for i in ids:
                self.checkId(vartype=expectedType, id=i, isReturn=True)
        if (len(primitives) > 0):
            for p in primitives:
                self.checkPrimitive(vartype=expectedType, prim=p, isReturn=True)

    #Recebe uma linha já identificada como um ELSE
    def elseStatement(self, line):
        uid = "ELSE_"+str(uuid.uuid4())[:5] #id aleatorio pro escopo
        self.changeScope(scope=uid)
        
    #Recebe uma linha já identificada como um IF ou ELSE IF
    def ifStatement(self, line):
        ids = self.getIdsFromDeclaration(line)
        for i in ids:
            if i not in self.declaredScopes and i not in self.declaredVariables: #checar se as condições do if sao declaradas
                notDeclared(i)
                self.hasError = True
        uid = "IF_"+str(uuid.uuid4())[:5] #id aleatorio
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
    def changeScope(self, scope, scopetype='VOID'):
        previousReachable = self.declaredScopes[self.currentScope]['reachableScopes']
        newScopeDetails = {}
        newScopeDetails['type'] = scopetype
        newScopeDetails['reachableScopes'] = [scope] + previousReachable
        self.declaredScopes[scope] = newScopeDetails
        aux = self.previousScope
        self.previousScope = self.currentScope
        self.currentScope = scope
        #print("Fui para: ", self.currentScope) 
        #print("Antes estava em:", self.previousScope)

    #Fecha o escopo
    def closeScope(self):
        aux = self.currentScope
        reachable = self.declaredScopes[self.currentScope]['reachableScopes']
        idx = reachable.index(aux)
        self.currentScope = reachable[idx+1]
        self.previousScope = aux
        #idx = self.declaredScopes[self.currentScope]['reachableScopes'].index(aux)
        #print("Sai de: ", self.previousScope) 
        #print("Agora estou em:", self.currentScope)

    #Recebe uma linha que já foi identificada como uma atribuição de uma variável já criada
    def attributeVariable(self, line):
        var = line[0]
        ids = self.getIdsFromDeclaration(line)
        primitives = self.getPrimitivesFromDeclaration(line)
        #Encontrar o escopo adequado
        reachable = self.declaredScopes[self.currentScope]['reachableScopes']
        selected = ""
        for r in reachable:
            if r in self.declaredVariables[var]:
                selected = r
                break

        if (selected == ""):
            outOfScope(var)
            self.hasError = True
        else: 
            vartype = self.declaredVariables[var][selected]

            if (len(ids) > 1):
                for i in range(len(ids)):
                    if (i != 0):
                        self.checkId(vartype=vartype, id=ids[i])
            if (len(primitives) > 0):
                for i in range(len(primitives)):
                    self.checkPrimitive(vartype=vartype, prim=primitives[i])           

    #Recebe uma linha que já foi reconhecida como uma chamada de função / id bruto
    #formato --> getNome(); ou b;
    def rawId(self, line):
        #NÃO É NECESSÁRIO CHECAR OS ARGUMENTOS DA CHAMADA DE FUNÇÃO
        if (line[0] not in self.declaredScopes):
            if (line[0] not in self.declaredVariables):
                    notDeclared(line[0])
                    self.hasError = True

    #Recebe uma linha que já foi identificada como uma função
    #Formato --> (VARINT ID(func) LPAREN ID(a) COMMA ID(b) RPAREN LBRACKET)
    def functionDeclaration(self, line):
        ids = self.getIdsFromDeclaration(line)
        var = ids[0]
        declaration = []
        vartype = line[0]
        self.changeScope(scope=var, scopetype=vartype) #Usa o primeiro ID da linha como referencia do novo escopo
        if (len(ids) > 0):
            declaration = line[line.index('LPAREN')+1:line.index('RPAREN')]
            i = (list(g) for _, g in itertools.groupby(declaration, key='COMMA'.__ne__))
            declaration = [a + b for a, b in itertools.zip_longest(i, i, fillvalue=[])]
            for d in declaration:
                self.variableDeclaration(d)
                
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
                    self.hasError = True
            if (ids != []):
                for i in ids:
                    self.checkId(vartype, i)
            if (primitives != []):
                for p in primitives:
                    self.checkPrimitive(vartype, p)
        vardetails = {}
        vardetails[self.currentScope] = vartype
        if (var in self.declaredVariables):
            d1 = self.declaredVariables[var]
            d1.update(vardetails)
        else:
            self.declaredVariables[var] = vardetails

    #Recebe um ID e um TIPO que estão sendo usados em uma declaração
    #Checa se esse id existe, e se os tipos são compativeis     
    def checkId(self, vartype, id, isReturn=False):
        #print("Checando se", id, "é do tipo", vartype)
        if id in self.declaredVariables:
            flag = False
            received = self.declaredVariables[id] #Isso é um dicionario dentro de outro dicionario
            reachable = self.declaredScopes[self.currentScope]['reachableScopes']
            for key, value in received.items(): #Iterando dentro de todos os escopos possiveis para a variavel
                for r in reachable: #Iterando pelos escopos possiveis alcancaveis
                    if r == key: #Variavel esta dentro dos escopos alcancaveis
                        if value == vartype:
                            flag = True
            if (flag is False):
                if (isReturn): returnIncompTypes(vartype)
                else: incompTypes(vartype)
                self.hasError = True
        elif(id in self.declaredScopes):
            received = self.declaredScopes[id]
            expectedType = received['type']
            if (vartype != expectedType):
                if (isReturn): returnIncompTypes(vartype)
                else: incompTypes(vartype)
                self.hasError = True
        elif(id not in self.declaredScopes and id not in self.declaredVariables): 
            notDeclared(id)
            self.hasError = True
        else:
            outOfScope(id)
            self.hasError = True
    
    def checkPrimitive(self, vartype, prim, isReturn=False):
        #Transformar primitivo em tipo
        received_type = self.VARTYPES[self.PRIMITIVES.index(prim)]
        if (received_type != vartype):
            if(isReturn):
                returnIncompTypes(vartype)
                self.hasError = True
            else:
                incompTypes(vartype)
                self.hasError = True

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
        if (self.hasError is False): print("SUCESSO!")

    def checkLine(self, line):
        if (self.hasError):
            pass
        # TESTE 0 : Linha em branco
        elif (line == []): 
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
                ids = self.getIdsFromDeclaration(line)
                if (len(ids) > 0 and 'COMMA' in line):
                    """ CASO 2.1:
                        - Há vários IDs na linha
                        = Há virgulas na linha
                        - Há multiplas atribuições na mesma linha (formato int a, b, c = 10) 
                    -> DECLARAÇÃO E ATRIBUIÇÃO DE MULTIPLAS VARIAVEIS """
                    vartype = line[0]
                    declaration = line[line.index('ASSIGN'):line.index('SEMICOLON')]
                    ids = self.getIdsFromDeclaration(line)
                    for i in ids:
                        definition = [vartype, i] + declaration
                        self.variableDeclaration(definition)
                else:
                    """ CASO 2.2:
                        - Há apenas uma atribuiçao
                    -> DECLARAÇÃO E ATRIBUIÇÃO DE UNICA VARIAVEL """  
                    self.variableDeclaration(line, assign=True)

            else:
                """ CASO 3:
                    - Não há atribuição
                    - Assumindo que não há erros lexicos e semanticos
                -> DECLARAÇÃO DE VARIAVEL SEM ATRIBUIÇÃO """
                self.variableDeclaration(line)
        # TESTE 2 : Há uma chamada para um IF
        elif (line[0] == 'IF' and 'LBRACKET' in line and 'LPAREN' in line and 'RPAREN' in line):
            self.ifStatement(line)
        # TESTE 3 : Há uma chamada para um ELSE
        elif ('ELSE' in line and 'LBRACKET' in line):
            if (line[1] == 'IF'):
                """ CASO 1:
                -> IF ELSE """
                self.ifStatement(line)
            else:
                """ CASO 2:
                -> ELSE PURO """
                self.elseStatement(line)
        # TESTE 4 : O primeiro caractere da linha é uma CHAVE FECHANDO
        elif (line[0] == 'RBRACKET'):
            #Isso indica o fechamento do escopo atual
            self.closeScope() #Volta ao escopo anterior
        # TESTE 5 : O primeiro caractere da linha é um ID
        elif (re.match(r'ID\(.*?\)', line[0])):
            if ('ASSIGN' in line and line[0] in self.declaredVariables):
                """ CASO 1:
                    - Há atribuição
                -> ATRIBUIÇÃO DE VALOR A VARIAVEL JA DECLARADA"""
                self.attributeVariable(line)
            else:
                """ CASO 2:
                    - O primeiro valor da linha é um escopo declarado
                -> CHAMADA DE FUNÇÃO/ID BRUTO """
                self.rawId(line)
        # TESTE 6 : Retorno de função
        elif ('RETURN' in line):
            self.returnStatement(line)
        # TESTE 7 : Chave como primeiro item da linha
        elif (line[0] == 'LBRACKET'):
            #BLOCO
            self.openBlock(line)
            
def main():

    # Para testes com todos os inputs dentro da pasta /inputs
    for file in os.listdir("./inputs"):
        if file.endswith(".txt"):
            path = os.path.join("./inputs", file)
            with open(path, encoding='utf8') as f:
                content = f.readlines()
            print("TESTE DO ARQUIVO:", file)
            s = Semantic()
            s.semanticTest(content)
            print("\n")
            # s.showScopesAndVariables() #Para mostrar escopos e variaveis (opcional)
    
    """
    # Para testes com um unico input
    with open('./inputs\1.txt', encoding='utf8') as f:
        content = f.readlines()
    
    s.semanticTest(content)
    # s.showScopesAndVariables() #Para mostrar escopos e variaveis (opcional)
    """
    

if __name__ == "__main__":
    main()