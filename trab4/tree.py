import re 
from node import Node

class Tree():
    TKN_PATTERN = r'(MOVE|MEM|\+|\-|\*|\/)' #Padrão de "tokens"
    NTKN_PATTERN = r'\(|\)|\,' #Padrão de "não tokens" (TEMP, CONST e outros valores como FP etc...)
    def __init__(self): 
        self.root = None #Raiz da arvore
        self.scopes = [] #Lista de tuplas que representa os escopos

    def makeTree(self, str):
        txt = str.split() #Divide o input em espaços em branco
        tokens = re.findall(self.TKN_PATTERN, str) #Encontra os "tokens" (+, -, *, /, MEM, MOVE)
        currentDirection = "esq" #Inicia construção da arvore pela esquerda
        previous = None #Marca o node anterior
        aux = None #Nó atual
        self.node_path = [] #Enquanto construo a arvore eu faço um array do "caminho" da arvore que vai ser util mais na frente
        rawValue = None #Valor bruto (para casos de TEMP x ou CONST x)
        for i in range(len(txt)): #ITERANDO SOBRE A ENTRADA
            if (i < len(txt)):
                if(not re.match(self.NTKN_PATTERN, txt[i])): #Se for um não token
                    if (txt[i] == "CONST" or txt[i] == "TEMP"): 
                        #Essa parte junta valores como 
                        if (not re.match(self.NTKN_PATTERN, txt[i+1])):
                            txt[i] = txt[i] + " " + txt[i+1]
                            rawValue = txt[i+1]
                            txt.pop(i+1)
                        else: rawValue = txt[i]
                    
                    aux = Node(txt[i])
                    aux.rawValue = rawValue 

                    #Marca os escopos e os nodes passados
                    if (len(self.scopes) == 0):
                        self.root = aux
                        self.node_path.append(self.root)
                        previous = self.root    
                        
                    #Marca o nó pai e diz onde inserir o nó atual (esquerda ou direita)
                    elif(previous is not None):
                        aux.father = self.scopes[-1]
                        if(currentDirection == "dir"):
                            #depois de colocar um nó na direita volto a inserir nós a esquerda (padrão)
                            self.scopes[-1].right = aux
                            currentDirection = "esq"
                        elif(currentDirection == "esq"):
                            self.scopes[-1].left = aux

                        self.node_path.append(aux)
                        previous = aux

                    #Atualiza os escopos
                    if (txt[i] in tokens):
                        self.scopes.append(aux)

                elif(txt[i] == "("): pass #Parenteses a esquerda -> nada acontece
                elif(txt[i] == ")"):  #Parenteses a direita -> Volta ao escopo anterior
                    self.scopes.pop()
                    #self.printScopes()
                    if (len(self.scopes) >= 1):
                        previous = self.scopes[-1]
                elif(txt[i] == ","): #Virgula -> proximo nó está a direita
                    currentDirection = "dir"

    #Print pos-ordem
    def printPostorder(self, node):
        if node:
            self.printPostorder(node.left)
            self.printPostorder(node.right)
            print(node.value)

    #Printa os padrões (tile)
    def printTiles(self):
        tiles = []
        for n in self.node_path:
            if(n.isUsed):
                tiles.append(self.getTileVal(n.selectedTile))
        
        filtered = tiles
        print('\n'.join([' ==> '.join([str(cell) for cell in row]) for row in filtered]))
        self.calculateCost(filtered)

    #Função auxiliar para obter os valores dos nos de um padrão (tile)
    def getTileVal(self, tile):
        tile_v = []
        for t in tile:
            #if(t.value not in tile_v):
                tile_v.append(t.value)
        return tile_v

    #Função para calcular o custo da arvore
    def calculateCost(self, tileArray):
        cost = 0
        for tile in tileArray:
            if (tile[0] == "MOVE"): #CASO MOVE
                if(tile == ["MOVE", "MEM", "MEM"]): #Se o padrão for MOVE, MEM, MEM indica um MOVEM e o custo é somado em 2
                    cost+= 2
                else: cost += 1 #Do contrário o custo é 0
            elif(re.match(r'CONST.*?', tile[0])): #CASO CONST
                cost += 1
            elif(tile[0] == "+" or tile[0] == "-" or tile[0] == "*" or tile[0] == "/" or tile[0] == "MEM"): #CASO Operações bascas
                cost += 1
            else: #CASO TEMP ou outro registrador como FP
                cost+= 0 #Essa operação não tem custo
        print("=== CUSTO TOTAL: ", cost, " ===")

    #Pega os padrões no formato (node, numero_padrão)
    def getPatterns(self):
        res = []
        for n in self.node_path: #Verifica os nós utilizados, ou seja, as raizes dos padrões
            if(n.isUsed):
                res.append([n, n.pattern])
            
        return res