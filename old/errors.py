import sys


def incompTypes(expectedType, var, line):
     print("[LINHA " + str(line) + "] Erro => Tipos incompatíveis, tipo esperado " + expectedType + " Na variável " + var)
     sys.exit()

def notDeclared(target, line):
    print("[LINHA " + str(line) + "] Erro => Variável/Função não declarada : " + target)
    sys.exit()

def outOfScope(target, line):
    print("[LINHA " + str(line) + "] Erro => Variável/Função fora do escopo em : " + target)
    sys.exit()

def paramCountErr(func, line):
    print("[LINHA " + str(line) + "] Erro => A função " + func + " recebeu uma quantidade incorreta de parametros")
    sys.exit()
    
def argIncompTypes(expectedType, argNum, func, line):
    print("[LINHA " + str(line) + "] Erro => Tipos incompatíveis no argumento " + str(argNum+1) + " da função " + func + ", Tipo esperado: " + expectedType)
    sys.exit()