
import re

grammar = {
    1: 'S -> S;S',
    2: 'S -> id:=E',
    3: 'S -> print(L)',
    4: 'E -> id',
    5: 'E -> num',
    6: 'E -> E+E',
    7: 'E -> (S,E)',
    8: 'L -> E',
    9: 'L -> L,E'
}


START_SYMBOL = 'S'
EPSILON = "ε"
firstSet = {}
followSet = {}

def buildFirstSets(grammar):
  firstSet = {}
  buildSet(firstOf)

def firstOf(symbol):
    if (symbol in firstSet):
        return firstSet[symbol]

    first = firstSet[symbol] = {}

    if (isTerminal(symbol)):
        first[symbol] = True
        return firstSet[symbol]

    productionsForSymbol = getProductionsForSymbol(symbol)
    for p in productionsForSymbol:
        production = getRHS(productionsForSymbol[p])
        
        for i in range(len(production)):
            productionSymbol = production[i]

            if (productionSymbol == EPSILON):
                first[EPSILON] = True
                break
        
            firstOfNonTerminal = firstOf(productionSymbol)

            if (EPSILON not in firstOfNonTerminal):
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
    return production.split('->')[0].replace(r'\s+', '')

def getRHS(production):
    return production.split('->')[1].replace(r'\s+', '')

def buildFollowSets(grammar):
    followSet = {}
    buildSet(followOf)

def followOf(symbol):
    if (symbol in followSet):
        return followSet[symbol]

    follow = followSet[symbol] = {}

    if (symbol == START_SYMBOL):
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

            firstOfFollow = firstOf(followSymbol)

            if (EPSILON not in firstOfFollow):
                merge(follow, firstOfFollow)
                break
            
            merge(follow, firstOfFollow, [EPSILON])
            followIndex+=1
    
    return follow

def buildSet(builder):
    for k in grammar:
        builder(grammar[k][0])

def getProductionsWithSymbol(symbol):
    productionsWithSymbol = {}
    for k in grammar:
        production = grammar[k]
        rhs = getRHS(production)
        if (rhs.find(symbol) != -1):
            productionsWithSymbol[k] = production
    
    return productionsWithSymbol

def isTerminal(symbol):
    isNonTerminal = re.match(r"[A-Z]", symbol) #Checa se é não terminal
    return not bool(isNonTerminal) #Retorna invertendo o booleano

def merge(destination, origin, exclude = []):
    for key in origin:
        if (key not in exclude):
            destination[key] = origin[key]

def printSet(name, set):
    print(' ', name)
    for k in set:
        for item in set[k]:
            print(' ', k, ':', item)

def main():


    buildFirstSets(grammar)
    print("First : ", firstSet)

    buildFollowSets(grammar)
    print("Follow : ", followSet)

    printSet("First", firstSet)
    printSet("Follow", followSet)

if __name__ == "__main__":
    main()

