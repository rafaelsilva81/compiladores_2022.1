class Node():
    def __init__(self, key):
        self.value = key
        self.left = None
        self.right = None
        self.father = None
        self.isUsed = True #Determina se o nó é uma raiz de um padrão (subarvore)
        self.pattern = 9999 #Padrão de 1-18 que determina na tabelinha qual a instrução que será printada
        self.rawValue = None
        self.selectedTile = [] #Tile (padrão) desse nó
        
    def getChildren(self): #Retorna os filhos em uma tupla
        return (self.left, self.right)

    def printTree(self):
        self.printProcess("", self, False, True) #Inicia o print
        
    def printProcess(self, prefix, n, isLeft, isRoot=False): #Printa o nó atual e recursivamente printa os filhos
        if (n is not None):
            #Isso é para formatar a arvore no print
            if (isRoot):
                separator = "|   "
                combinator = "R --> "
            elif (isLeft):
                separator = "|   "
                combinator = "• --> "
            else:
                separator = "   "
                combinator = "\\ --> "
            print(prefix + combinator + n.value) 
            self.printProcess((prefix + separator), n.left, True) #Chamadas recursivas
            self.printProcess((prefix + separator), n.right, False)
    
    def getLeaves(self): #Retorna todas as folhas da arvore a partir do nó atual
        leafNodes = []
        if (self.left is None and self.right is None):
            leafNodes.append(self)
        else:
            if(self.left):
                leafNodes += (self.left.getLeaves())
            if(self.right):
                leafNodes += (self.right.getLeaves())
        return leafNodes

    def getRawValue(self, a): #Pega o valor bruto caso exista
        #Valor bruto seria em casos como TEMP i ou CONST 4, 
        # na inserção o valor bruto seria apenas "i" e "4"
        # permitindo printar as instruções mais facilmente
        if (self.rawValue is not None):
            return self.rawValue
        else: 
            return a