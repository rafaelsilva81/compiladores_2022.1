import re
from node import Node


class Selector():
    TKN_PATTERN = r'(MOVE|MEM|\+|\-|\*|\/)'

    #TABELA DE INSTRUÇÕES MAQUINA DE JOUETTE
    PATTERN_INSTRUCTIONS = {
        1: "TEMP r{i}",
        2: "ADD r{i} <- r{j} + r{k}",
        3: "MUL r{i} <- r{j} * r{k}",
        4: "SUB r{i} <- r{j} - r{k}",
        5: "DIV r{i} <- r{j} / r{k}",
        6: "ADDI r{i} <- r{j} + {c}",
        7: "ADDI r{i} <- r{j} + {c}",
        8: "ADDI r{i} <- r{j} + {c}",
        9: "SUBI r{i} <- r{j} - {c}",
        10: "LOAD r{i} <- M[r{j} + {c}]",
        11: "LOAD r{i} <- M[r{j} + {c}]",
        12: "LOAD r{i} <- M[r{j} + {c}]",
        13: "LOAD r{i} <- M[r{j} + {c}]",
        14: "STORE M[r{j} + {c}] <- r{i}",
        15: "STORE M[r{j} + {c}] <- r{i}",
        16: "STORE M[r{j} + {c}] <- r{i}",
        17: "STORE M[r{j} + {c}] <- r{i}",
        18: "MOVEM M[r{j}] <- M[r{i}]",
    }

    def __init__(self, tree) -> None:
        self.tree = tree
        self.i = 0
        self.leaves = tree.root.getLeaves()
        self.checkTree(self.leaves) #Checa a arvore começando das folhas

    #Checa a arvore de cima para baixo, começando das folhas
    def checkTree(self, itemArr):
        if (itemArr != []):
            for item in itemArr:
                self.findPattern(item) #Encontra o padrão
            self.getNewLayer(itemArr) #Busca uma nova camada (subindo na arvore)

    #Chama uma função para cada tipo de operação
    def findPattern(self, item):
        if(item.value == "+"):
            self.plus(item)
        elif(item.value == "-"):
            self.minus(item)
        elif(item.value == "*"):
            self.times(item)
        elif(item.value == "/"):
            self.division(item)
        elif(item.value == "MEM"):
            self.mem(item)
        elif(item.value == "MOVE"):
            self.move(item)
        elif(re.match(r'CONST.*?', item.value)):
            self.const(item)
        else:
            self.temp(item) #Caso padrão para TEMP ou FP
    
    #Obtem uma nova camada da arvore (subindo a arvore até chegar na raiz)
    def getNewLayer(self, itemArr):
        newArr = []
        for item in itemArr:
            if(item.father is not None):
                if (item.father not in newArr):
                    newArr.append(item.father)

        self.checkTree(newArr) #Checa a nova camada da arvore
    
    #Printa as instruções
    def printInstructions(self, patterns):
        a = 1 #Valores arbitrarios pros registradores
        b = 1
        c = 1
        patterns = patterns[::-1] #Inverte a matriz recebida (para organizar de baixo pra cima)
        for i in range(len(patterns)):
            node = patterns[i][0] #No atual
            option = patterns[i][1] #Padrao atual
            instruction = self.PATTERN_INSTRUCTIONS.get(option, "Padrão não encontrado") #Pega a instrução na tabela
            
            if (option == 1): #TEMP
                #ESSA OPERAÇÃO CRIA UM NOVO REGISTRADOR, MAS NÃO IMPRIME NADA
                b = a
                a += 1
            
            if (option in [2, 3, 4, 5]): # ADD, SUB, MUL e DIV
                print(i+1, instruction.format(i=b, j=node.left.getRawValue(a), k=b))
            

            if (option in [6, 7, 9]): # ADDI e SUBI
                aux1 = node.right.getRawValue(a) 
                aux2 = node.left.getRawValue(a+1)
                if (option == 6 or option == 9): #Depende se o const está na esquerda ou direita
                    print(i+1, instruction.format(i=b, j=aux2, c=aux1))
                else :
                    print(i+1, instruction.format(i=b, j=aux1, c=aux2))   
            
            if (option == 8): # ADDI Caso especial para CONST solto
                print(i+1, instruction.format(i=b, j=0, c=node.getRawValue(a)))
            
            if (option in [10, 11]): #LOAD dois primeiros casos
                child = node.getChildren()[0]
                aux1 = child.right.getRawValue(a) 
                aux2 = child.left.getRawValue(a+1)
                if (option == 10): #Depende se o const está na esquerda ou direita 
                    print(i+1, instruction.format(i=b, j=aux2, c=aux1))
                else :
                    print(i+1, instruction.format(i=b, j=aux1, c=aux2))  
            
            if (option == 12): #LOAD terceiro caso
                child = node.getChildren()[0]
                print(i+1, instruction.format(i=b, j=0, c=child.getRawValue(a)))

            if (option == 13): #LOAD quarto caso
                print(i+1, instruction.format(i=b, j=b, c=0))

            if (option in [14, 15]): #MOVE dois primeiros casos
                child = node.getChildren()[0].getChildren()[0]
                aux1 = child.right.getRawValue(a) 
                aux2 = child.left.getRawValue(a+1)
                if (option == 14): #Depende se o const está na esquerda ou direita
                    print(i+1, instruction.format(i=b, j=aux2, c=aux1))
                else :
                    print(i+1, instruction.format(i=b, j=aux1, c=aux2))  

            if (option == 16): #MOVE terceiro caso
                child = node.getChildren()[0].getChildren()[0]
                print(i+1, instruction.format(i=b, j=0, c=child.getRawValue(a)))

            if (option == 17): #MOVE quarto caso
                print(i+1, instruction.format(i=b, j=a, c=0))
            
            if (option == 18): #MOVEM
                print(i+1, instruction.format(i=b, j=a))

    """
        Funções para cada instrução possivel (MEM, MOVE, +, -, *, /, CONST, TEMP)
        Cada função cria a Tile (padrão) baseado nos padrões da arquitetura, atribuindo a todos os nós do padrão o mesmo padrão
        Define quais os nós são raizes de um padrão através do atributo .isUsed
        Define o numero do padrão baseado na tabela da arquitetura
    """
    def move(self, node: Node):
        pattern = 14
        children = node.getChildren()
        if (children[0] is not None):
            if (children[0].value == "MEM"):
                if children[0].pattern == 10:
                    tile = [node] + children[0].selectedTile
                    pattern = 14 #MOVE(MEM(+(TEMP, CONST)))
                    node.pattern = pattern
                    for n in children[0].selectedTile:
                        n.isUsed = False
                        n.selectedTile = tile
                    node.isUsed = True
                    node.selectedTile = tile
                elif(children[0].pattern == 11):
                    tile = [node] + children[0].selectedTile
                    pattern = 15 #MOVE(MEM(+(CONST, TEMP)))
                    node.pattern = pattern
                    for n in children[0].selectedTile:
                        n.isUsed = False
                        n.selectedTile = tile
                    node.isUsed = True
                    node.selectedTile = tile
                elif(children[0].pattern == 12):
                    tile = [node] + children[0].selectedTile
                    pattern = 16 #MOVE(MEM(CONST))
                    node.pattern = pattern
                    for n in children[0].selectedTile:
                        n.isUsed = False
                        n.selectedTile = tile
                    node.isUsed = True
                    node.selectedTile = tile
                elif(children[0].pattern == 13): #MOVE(MEM(), TEMP)
                    if (children[0] is not None and children[1].pattern == 13):
                        tile = [node, children[0], children[1]]                  
                        pattern = 18 #MOVE(MEM(), MEM())
                        node.pattern = pattern
                        node.selectedTile = tile
                        children[0].selectedTile = tile
                        children[1].selectedTile = tile
                        node.isUsed = True
                        children[0].isUsed = False
                        children[1].isUsed = False
                    else:
                        tile = [node, children[0]]
                        pattern = 17 #MOVE(MEM())
                        node.pattern = pattern
                        node.selectedTile = tile
                        children[0].selectedTile = tile
                        node.isUsed = True
                        children[0].isUsed = False
            

    def mem(self, node: Node):
        pattern = 13
        children = node.getChildren()
        if (children[0] is not None):
            if (children[0].value == "+"):
                if children[0].pattern == 6:
                    tile = [node, children[0], children[0].right]
                    pattern = 10 #MEM(+(TEMP, CONST))
                    node.selectedTile = tile
                    children[0].selectedTile = tile
                    children[0].right.selectedTile = tile
                    node.isUsed = True
                    children[0].isUsed = False
                    children[0].right.isUsed = False
                elif(children[0].pattern == 7):
                    tile = [node, children[0], children[0].left]
                    pattern = 11 #MEM(+(CONST, TEMP))
                    node.selectedTile = tile
                    children[0].selectedTile = tile
                    children[0].left.selectedTile = tile
                    node.isUsed = True
                    children[0].isUsed = False
                    children[0].left.isUsed = False
                node.pattern = pattern
            elif (re.match(r'CONST.*?', children[0].value)):
                tile = [node, children[0]]
                node.pattern = 12 #MEM(CONST))
                node.selectedTile = tile
                children[0].selectedTile = tile
                node.isUsed = True
                children[0].isUsed = False
            else:
                tile = [node]
                node.pattern = 13 #MEM(CONST))
                node.selectedTile = tile
                node.isUsed = True

    def times(self, node: Node): 
        children = node.getChildren()
        if(children[0] is not None and children[1] is not None):
            tile = [node]
            node.pattern = 3 #*(TEMP, TEMP)
            node.selectedTile = tile
            node.isUsed = True
    
    def division(self, node: Node):
        children = node.getChildren()
        if(children[0] is not None and children[1] is not None):
            tile = [node]
            node.pattern = 5 #/(TEMP, TEMP)
            node.selectedTile = tile
            node.isUsed = True

    def minus(self, node: Node):
        children = node.getChildren()
        if(children[1] is not None and re.match(r'CONST.*?', children[1].value)):
            tile = [node, children[1]]
            node.pattern = 9 #-(TEMP, CONST)
            node.selectedTile = tile
            node.isUsed = True
            children[1].selectedTile = tile
            children[1].isUsed = False
        elif(children[0] is not None and children[1] is not None):
            tile = [node]
            node.pattern = 4 #-(TEMP, TEMP)
            node.selectedTile = tile
            node.isUsed = True

    def plus(self, node: Node):
        children = node.getChildren()
        if (children[0] is not None and re.match(r'CONST.*?', children[0].value)):
            tile = [node, children[0]]
            node.pattern = 7 #+(CONST, TEMP)
            node.selectedTile = tile
            node.isUsed = True
            children[0].selectedTile = tile
            children[0].isUsed = False
        elif(children[1] is not None and re.match(r'CONST.*?', children[1].value)):
            tile = [node, children[1]]
            node.pattern = 6 #+(TEMP, CONST)
            node.selectedTile = tile
            node.isUsed = True
            children[1].selectedTile = tile
            children[1].isUsed = False
        elif(children[0] is not None and children[1] is not None):
            tile = [node]
            node.pattern = 2 #+(TEMP, TEMP)
            node.selectedTile = tile
            node.isUsed = True

    def const(self, node: Node):
        tile = [node]
        node.pattern = 8
        node.selectedTile = tile
        node.isUsed = True

    def temp(self, node: Node):
        tile = [node]
        node.pattern = 1
        node.selectedTile = tile
        node.isUsed = True