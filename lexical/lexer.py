import re

"""
    ANALISADOR LÉXICO DA LINGUAGEM A
    TRANSFORMA A ENTRADA DO USUARIO EM TOKENS VÁLIDOS
"""
tokens = {
    "LBRACKET" : r"(\{)",
    "RBRACKET" : r"(\})",
    "RPAREN" : r"(\))",
    "LPAREN" : r"(\()",
    "SEMICOLON" : r"(\;)",
    "COMMA" : r"(\,)",
    "ELSE" : r"(else)",
    "IF" : r"(if)",
    "RETURN" : r"(return)",
    "VARSTRING" : r"(string)",
    "VARINT" : r"(int)",
    "WORD" : r"(\"[A-Za-z0-9!@#$%():.,;^{}'=+\-/_\*\]\[\&\|\\ ]*\")",
    "BOOLEAN_OP" : r"(\<|\>|\>\=|\<\=|\=\=|\!\=|\!|\&\&|\|\|)",
    "ASSIGN" : r"(\=)",
    "MATH_OP" : r"(\+|\-|\/|\*|\%)",
    "ID" : r"([A-Za-z]+[A-Za-z0-9]*)",
    "NUMBER" : r"([0-9]+)"
}

def getFullRe():
    keys = list(tokens)
    r = r''
    for i in range(len(keys)):
        if (i != 0 and i != len(keys)):
            r = r+'|'+tokens.get(keys[i])
        else : r = r + tokens.get(keys[i])

    #print(r)
    return r

def getTokenMatch(singleInput):
    if (singleInput == '') : return ''
    for k,v in tokens.items():
        x = re.match(v, singleInput)
        if x: return k
    
    return 'ERRO'

def tokenize(inputString):
    tokenArr = []
    inputArray = splitInput(inputString)
    for userInput in inputArray:
            t = getTokenMatch(userInput)
            if (t == 'ID'):
                t = 'ID('+userInput+')' #Modificado para esse trabalho
            tokenArr = tokenArr + [t]

    no_whitespace = [s for s in tokenArr if s.strip()]
    return no_whitespace #modificado para esse trabalho

def splitInput(inputString):
    x = re.split(getFullRe(), inputString)
    y = []
    for match in x:
        if (match is not None and match != ''):
            y = y + [match]
    
    res = map(str.strip, y)
    #print(y)
    return res

def main():
    line = ""
    print("Analisador Léxico da Lingugem A - Desenvolvido por Rafael Galdino da Silva")
    print("use 'exit' para sair")
    while True:
        line = input(" A >> ")
        if (line == 'exit') : 
            print("Finalizando...")
            break
        print(tokenize(line))
    #print(getSingleToken('if(a==10)'))

if __name__ == "__main__":
    main()
