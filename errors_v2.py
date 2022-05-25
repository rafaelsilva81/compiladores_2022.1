import sys

def impossibleOperation(var):
     print("Erro => Operação matemática impossivel na variável: " + var)
     #sys.exit()

def incompTypes(expectedType, var):
     print("Erro => Tipos incompatíveis, tipo esperado " + expectedType + " Na variável " + var)
     #sys.exit()

def notDeclared(target):
    print("Erro => Variável/Função não declarada : " + target)
    #sys.exit()

def outOfScope(target):
    print("Erro => Variável/Função fora do escopo em : " + target)
    #sys.exit()

def paramCountErr(func):
    print("Erro => A função " + func + " recebeu uma quantidade incorreta de parametros")
    #sys.exit()
    
def argIncompTypes(expectedType, argNum, func):
    print("Erro => Tipos incompatíveis no argumento " + str(argNum+1) + " da função " + func + ", Tipo esperado: " + expectedType)
    #sys.exit()