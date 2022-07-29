from selector import Selector
from tree import Tree
import os

if __name__ == "__main__":
    
    print("Legenda: \n R: Raiz \n •: Esquerda ou Folha unica \n \\: Direita \n")    
    # Para testes com todos os inputs dentro da pasta /inputs
    for file in os.listdir("./inputs"):
        if file.endswith(".txt"):
            path = os.path.join("./inputs", file)
            with open(path, encoding='utf8') as f:
                content = f.read()
            
            #if(file.startswith("t2")): #Para testar um arquivo especifico
                print("=== ARQUIVO:", file, " ===")
                print("=== ARVORE MONTADA:")
                t = Tree()
                t.makeTree(content) #Cria arvore
                t.root.printTree()
                print('\n')
                s = Selector(tree=t) #Cria o seletor, que já irá fazer a seleção
                print("=== PADRÕES SELECIONADOS:")
                t.printTiles() #Imprime os padrões (optimal tiling)
                print('\n')
                print("=== INSTRUÇÕES SELECIONADAS:")
                s.printInstructions(t.getPatterns()) #Imprime as instruções baseando-se nos padrões
                print('\n') 