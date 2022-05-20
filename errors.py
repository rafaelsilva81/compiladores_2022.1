def incompTypes(expectedType, var, line):
     print("[LINHA " + str(line) + "] Erro => Tipos incompatíveis, tipo : esperado " + expectedType + " Na variável " + var)

def notDeclared(target, declaration, line):
    print("[LINHA " + str(line) + "] Erro => Variável/Função não declarada em : " + target + " = " + declaration)

def outOfScope(target, declaration, line):
    print("[LINHA " + str(line) + "] Erro => Variável/Função fora do escopo em : " + target + " = " + declaration)