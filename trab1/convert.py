####### DEFINIÇÃO DE VARIAVEIS GLOBAIS ############################
EPSILON = "ε"

#NFA montado para testes
estado_inicial = 0
estados_finais = [4]
nfa = {
    0: {EPSILON: [1,2]},
    1: {EPSILON : [3]},
    2: {"a" : [3]},
    3: {"a": [4]},
    4: {},
}
#####################################################################

# Retorna um array com o alfabeto utilizado para construir o NFA (Removendo EPSILON)
def getAlphabet():
    a = []
    for key, value in nfa.items():
        for k, v in value.items():
            if k not in a:
                a.append(k)

    if EPSILON in a:
        a = list(filter((EPSILON).__ne__, a))

    return a


# Input : um estado 'state' e um caractere 'char'
# Output : um conjunto de estados do NFA que são alcançáveis por 'state' através de 'char'
def edge(state, char):
    r = []
    trans = nfa.get((state))
    if trans is not None:
        for key, value in trans.items():
            if key == char:
                r = r + value
    return r


# Input : um conjunto de estados 'stateSet'
# Output : um conjunto de estados do NFA que são alcançáveis por cada um dos estados em 'stateSet' através de 'char'
def closure(stateSet):
    #print("INICIO CLOSURE COM STATESET = ", stateSet)
    t = stateSet
    while True:
        t_aux = t
        for state in t_aux:
            edg = edge(state, EPSILON)
            t = t_aux
            for e in edg:
                if e not in t:
                    t.append(e)
            #print(t_aux, "--", state, "--", edg, "--", t)
        if (t == t_aux):
            break
    
    #print("------------------- FIM CLOSURE --------------")
    return t


# Input : um conjunto de estados 'stateSet' e um caractere 'c'
# Output : um novo conjunto de estados alcançáveis através do caractere 'c' em união com a closure do estado
def DFAEdge(stateSet, c):
    t = []
    for state in stateSet:
        edg = edge(state, c)
        clr = closure(edg)
        #print(state, c, edg, clr)
        for cl in clr:
            t.append(cl)
    
    return t

#Função auxiliar para converter uma lista em string
#Listas nao podem ser keys de um dicionario em python, entao isso foi necessario
def arrToString(arr):
    return '[' + ','.join(map(str,arr)) + ']'

#Funçao que converte o NFA em DFA
def convertDfa():
    states = []
    states.insert(0,[])
    states.insert(1, closure([estado_inicial]))
    trans = {}
    d = []

    j = 0
    p = 2
    while j < p:
        for c in getAlphabet():
            d = DFAEdge(states[j], c)
            #print(d)
            flag = False
            for i in range(p):
                if (d == states[i]):
                    #print(states[i])
                    trans[(j, c)] = i
                    flag = True
                    break
            if flag == False:
                #print("Caindo aq")
                states.insert(p, d)
                trans[(j, c)] = p
                p += 1
        j += 1
    
    #print(states)
    #print(trans)
    generateDFA(states, trans)
    
#Função que gera o DFA assim como os estados finais e estado inicial
def generateDFA(states, trans):
    dfa = {}
    dfa_inicial = arrToString(closure([estado_inicial]))
    dfa_finais = []
    for s in states:
        if (s != []): #Ignorar o estado vazio de erro
            for k1, k2 in trans:
                if (k1 != 0): #Ignorar estado vazio de erro
                    #print(k1, k2)
                    if (states[k1] == s):
                        if (states[trans[(k1, k2)]] != []): #Ignorar estado de transiao de erro
                            dfa[(arrToString(s), k2)] = states[trans[(k1, k2)]]
    
    for s1 in states:
        for s2 in s1:
            if s2 in estados_finais and arrToString(s1) not in dfa_finais:
                dfa_finais.append(arrToString(s1))
    
    print("DFA CONVERTIDO!")
    print("Naovo estado inicial : ", dfa_inicial)
    print("Novos estados finais : ", dfa_finais)  
    print("Transicoes finais : ")
    makeLegible(dfa)

#Função auxiliar para deixar o DFA mais legivel após conversao
def makeLegible(dfa):
    for k, v in dfa:
        print(k, "--",v,"-->",dfa[k,v])
    
def main():
    #print("EDGE:", edge(2, EPSILON))
    #print("CLOSURE:", closure([4]))
    #print(getAlphabet())
    #print("DFAEdge :", DFAEdge([2,3], "a"))
    convertDfa()

if __name__ == "__main__":
    main()
