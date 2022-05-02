

grammar = {
    1: 'S -> S ; S',
    2: 'S -> id := E',
    3: 'S -> "print( L )',
    4: 'E -> id',
    5: 'E -> num',
    6: 'E -> E + E',
    7: 'E -> ( S , E )',
    8: 'L -> E',
    9: 'L -> L , E'
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
                first[EPSILON] = true
                break
        
            firstOfNonTerminal = firstOf(productionSymbol)

            if (EPSILON not in firstOfNonTerminal):
                merge(first, firstOfNonTerminal)
                break
            
            merge(first, firstOfNonTerminal, [EPSILON])

    return first

def getProductionsForSymbol(symbol):
    productionsForSymbol = {}
    for k,v in grammar.items():
        if(v[0] == symbol):
            productionsForSymbol[k] = grammar[k]
def main():


    buildFirstSets(grammar)
    print(firstSet)

    buildFollowSets(grammar)
    print(followSet)

if __name__ == "__main__":
    main()

