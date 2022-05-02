def getNonTerminals(g):
    x = []
    for k,v in grammar.items():
        x = x + [k]
    return x

def getTerminals(g):
    x = []
    for k,v in grammar.items():
        for rule in v:
            arr = rule.split()
            for item in arr:
                if (item not in getNonTerminals()):
                    x = x + [item]
    
    x = list(set(x))

    return x

def firstFollow(nonTerminals, terminals, grammar):
    first = {}
    follow = {}
    nullable = set()
    for t in terminals:
        #print(t)
        first[t] = {t}
    
    while True:
        first_aux = first
        follow_aux = follow
        nullable_aux = nullable

        for k,v in grammar.items():
            rule_len = len(v)
            if (rule_len == 0) or v.issubset(nullable):
                nullable = nullable.union({k})
            for i in range(1, (rule_len+1)):
                if (i == 1) or 


""" def getFirst():

def getFollow():

def getFollowFirst():

def calculateFirstFollow(): """
        

def main():

    #dictionary
    grammar = { 
        "S" : {"S ; S", "id := E", "print( L )"}, #Regras são sets
        "E" : {"id", "num", "E + E", "( S , E )"},
        "L" : {"E", "L , E"}
    }


    first = {} #array of sets
    follow = {} #set
    nullable = set() #set

    nonTerminals = getNonTerminals(grammar)
    terminals = getTerminals(grammar)

    firstFollow(nonTerminals, terminals)

    #print(terminals)
    #print(nonTerminals)
    print(first)

if __name__ == "__main__":
    main()
