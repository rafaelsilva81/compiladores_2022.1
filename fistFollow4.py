
import re

grammar = {
    1: 'S->S;S',
    2: 'S->id:=E',
    3: 'S->print(L)',
    4: 'E->id',
    5: 'E->num',
    6: 'E->E+E',
    7: 'E->(S,E)',
    8: 'L->E',
    9: 'L->L,E'
} 


START_SYMBOL = 'S'
EPSILON = "ε"
firstSet = {}
followSet = {}

def getWholeWord(idx):
    rhs = getRHS(grammar[idx])
    pattern = re.compile("^[^A-Z\s]*")
    #print(rhs)
    #print(pattern)
    res= "".join(re.findall(pattern,rhs))
    return res

def firstOf(symbol, idx=0):
    if (symbol in firstSet):
        return firstSet[symbol]

    first = firstSet[symbol] = {}

    if (isTerminal(symbol)):
        s = getWholeWord(idx)
        first[s] = True
        return firstSet[symbol]

    productionsForSymbol = getProductionsForSymbol(symbol)
    for p in productionsForSymbol:
        production = getRHS(productionsForSymbol[p])

        for i in range(len(production)):
            productionSymbol = production[i]
            #print(productionSymbol)
            if (productionSymbol == EPSILON):
                #print("CAI AQUI")
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
    x = production.split('->')[0].replace(r'\s+', '')
    return x #production.split('->')[0]

def getRHS(production):
    x = production.split('->')[1].replace(r'\s+', '')
    return x #production.split('->')[1]
    
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

            firstOfFollow = firstOf(followSymbol, p)

            if (EPSILON not in firstOfFollow):
                merge(follow, firstOfFollow)
                break
            
            merge(follow, firstOfFollow, [EPSILON])
            followIndex+=1
    
    return follow

def getProductionsWithSymbol(symbol):
    productionsWithSymbol = {}
    for k in grammar:
        production = grammar[k]
        rhs = getRHS(production)
        if (rhs.find(symbol) != -1):
            productionsWithSymbol[k] = production
    
    return productionsWithSymbol

def isTerminal(symbol):
    if (symbol == EPSILON):
        return False
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

def printSet(name, set):
    print(' ', name)
    for k in set:
            s = "{ " + " | ".join(set[k]) + " }"
            print(' ', k, ':', s)

def main():

    #print(getWholeWord("S", 2))
    firstOf(START_SYMBOL, 0)
    #print("First : ", firstSet)

    followOf(START_SYMBOL)
    #print("Follow : ", followSet)

    print("  Grammar")
    for k in grammar:
        print(" ",grammar[k])
    print("\n")
    printSet("First", firstSet)
    print("\n")
    printSet("Follow", followSet)

if __name__ == "__main__":
    main()

