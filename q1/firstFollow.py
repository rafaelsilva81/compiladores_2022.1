

import re

#Gramatica antiga
'''grammar = {
    1: 'S->S;S',
    2: 'S->id := E',
    3: 'S->print(L)',
    4: 'E->id',
    5: 'E->num',
    6: 'E->E + E',
    7: 'E->(S,E)',
    8: 'L->E',
    9: 'L->L,E'
}'''

grammar = {
    1: 'S-> B $',
    2: 'B-> id P',
    3: 'B-> id ( E ]',
    4: 'P-> ɛ',
    5: 'P-> ( E )',
    6: 'E-> B',
    7: 'E-> B , E',
}

START_SYMBOL = 'S'
EPSILON = "ɛ"
firstSet = {}
followSet = {}

def getWholeWord(symbol, idx):
    rhs = getRHS(grammar[idx])
    pattern = re.compile("[^A-Z\s]")
    word_idx = rhs.find(symbol) #Index de onde o symbolo foi encontrado
    res = symbol
    for x in range(word_idx, len(rhs)):
        try:
            a = rhs[x+1]
        except IndexError:
            #print("deu erro nesse : ", rhs)
            return res #a palavra inteira passou
        m = bool(re.match(pattern,a)) #Checar se o próximo caractere é um caractere maiusculo
        if (not m):
            break
        else:
            res = res + rhs[x+1]
    return res
    
def buildFirstSets(grammar):
  firstSet = {}
  buildSet(firstOf)

def firstOf(symbol, idx = 0):
    if (symbol in firstSet):
        return firstSet[symbol]

    first = firstSet[symbol] = {}

    if (isTerminal(symbol)):
        s = getWholeWord(symbol, idx)
        first[s] = True
        return firstSet[symbol]

    productionsForSymbol = getProductionsForSymbol(symbol)
    for p in productionsForSymbol:
        production = getRHS(productionsForSymbol[p])

        for i in range(len(production)):
            productionSymbol = production[i]
            if (productionSymbol == EPSILON):
                first[EPSILON] = True
                break
        
            firstOfNonTerminal = firstOf(productionSymbol, p)
            if (EPSILON not in firstOfNonTerminal):
                #print("Eu cai nessa parte do codigo")
                merge(first, firstOfNonTerminal)
                break
            
            merge(first, firstOfNonTerminal, [EPSILON])

    return first

def getProductionsForSymbol(symbol):
    productionsForSymbol = {}
    for k in grammar:
        if(grammar[k][0] == symbol):
            productionsForSymbol[k] = grammar[k]
    
    return productionsForSymbol

def getLHS(production):
    x = production.split('->')[0].replace(" ", '')
    return x #production.split('->')[0]

def getRHS(production):
    x = production.split('->')[1].replace(" ", '')
    return x #production.split('->')[1]
    
def buildFollowSets(grammar):
    followSet = {}
    buildSet(followOf)

def followOf(symbol, idx = 0):
    if (symbol in followSet):
        return followSet[symbol]

    follow = followSet[symbol] = {}

    if (symbol == START_SYMBOL):
        #print("To caindo aqui")
        follow['$'] = True

    productionsWithSymbol = getProductionsWithSymbol(symbol)
    for p in productionsWithSymbol:
        production = productionsWithSymbol[p]
        rhs = getRHS(production)

        symbolIndex = rhs.find(symbol)
        followIndex = symbolIndex + 1

        while True:
            if (followIndex == len(rhs)): 
                lhs = getLHS(production)
                if (lhs != symbol):
                    merge(follow, followOf(lhs))
                break
            
            followSymbol = rhs[followIndex]
            firstOfFollow = firstOf(followSymbol, p)
            
            if (EPSILON not in firstOfFollow):
                merge(follow, firstOfFollow)
                break
            
            merge(follow, firstOfFollow, [EPSILON])
            followIndex+=1
    
    return follow

def buildSet(builder):
    for k in grammar:
        builder(grammar[k][0], 0)

def getProductionsWithSymbol(symbol):
    productionsWithSymbol = {}
    for k in grammar:
        production = grammar[k]
        rhs = getRHS(production)
        if (rhs.find(symbol) != -1):
            productionsWithSymbol[k] = production
    
    return productionsWithSymbol

def isTerminal(symbol):
    #print("Checking if ", symbol, " is a terminal")
    isNonTerminal = re.match(r'[A-Z]', symbol) #Checa se é não terminal
    #print(symbol, " Is a terminal? : ", not bool(isNonTerminal))
    return not bool(isNonTerminal) #Retorna invertendo o booleano

def merge(destination, origin, exclude = []):
    for key in origin:
        #print("Exclude this > ",exclude)
        #print("This is origin > ", origin)
        #print("This is destination > ", destination)
        if (key not in exclude):
            destination[key] = origin[key]

        #print("This is the end > ", destination)

def printFirstSet():
    print("  ===== FIRST ===============")
    set = firstSet
    for k in set:
            if(not isTerminal(k)):
                s = " " + "   ".join(set[k]) + " "
                print(' ', k, ':', s)

def printGrammar():
    print("  ===== GRAMÁTICA ===============")
    for k in grammar:
        print(" ",grammar[k])


def printFollowSet():
    print("  ===== FOLLOW ===============")
    set = followSet
    for k in set:
            s = "  " + "  ".join(set[k]) + "  "
            print(' ', k, ':', s)


def main():


    buildFirstSets(grammar)
    #print("First : ", firstSet)

    buildFollowSets(grammar)
    #print("Follow : ", followSet)

    
    printGrammar()
    printFirstSet()
    printFollowSet()

if __name__ == "__main__":
    main()

