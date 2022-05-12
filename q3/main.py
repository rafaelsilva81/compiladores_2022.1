
import sys

class Parser:

    """ Observação : Estou usando `s` no lugar de `self`
    Isso é totalmente possível no python, ainda que não seja a melhor prática """

    def __init__(s):
        s.idx = 0 #Index de leitura
        s.lparen = 0
        s.rparen = 0
        s.grammar = {
            1: 'S->S;S',
            2: 'S->id := E',
            3: 'S->print(L)',
            4: 'E->id',
            5: 'E->num',
            6: 'E->E + E',
            7: 'E->(S,E)',
            8: 'L->E',
            9: 'L->L,E'
        }

    def checkSyntax(s, userInput):
        s.row = userInput
        s.tokenArr = userInput.split(" ")
        s.maximum = len(s.tokenArr) - 1
        s.tokenArr.append(" ")
        s.checkStateS()
    
    #Função para os estados de S
    def checkStateS(s):
        if (s.testOK()):
            print("Sucesso")
        #Teste para S -> id := E
        elif(s.tokenArr[s.idx] == "id"):
            if((s.idx+2) > s.maximum):
                print("Erro Sintático")
            else:
                if(s.tokenArr[s.idx+1] == ":="):
                    s.idx+=2
                    s.checkStateE()
                else:
                    if(s.tokenArr[s.idx-1] == ";" or s.tokenArr[s.idx-1] == "("):
                        s.lparen+=1
                        s.idx+=2
                        s.checkStateE()
                    else:
                        print("Erro Sintático")
        #Teste para S -> print(L)
        elif(s.tokenArr[s.idx] == "print"):
            if((s.idx+2) > s.maximum):
                print("Erro Sintático")
            else:
                if(s.tokenArr[s.idx+1] == "("):
                    s.lparen += 1
                    s.idx += 2
                    s.checkStateL()
                else:
                    if(s.tokenArr[s.idx-1] == ";" or s.tokenArr[s.idx-1] == "("):
                        s.lparen += 1
                        s.idx+=2
                        s.checkStateL()
                    else:
                        print("Erro Sintático")
        #Teste para S -> S ; S
        elif(s.tokenArr[s.idx] == ";"):
            s.idx += 1
            s.checkStateS()
        #Teste para L -> L,E com S -> print(L)
        elif(s.tokenArr[s.idx] == "," and ((s.tokenArr[s.idx-1] == "id") or ((s.tokenArr[s.idx-1] == "num")))):
            if(s.idx+1 > s.maximum):
                print("Erro Sintático")
            else:
                s.idx+=1
                s.checkStateE()
        #Teste para E -> (S,E)
        elif(s.tokenArr[s.idx] == ")" and ((s.tokenArr[s.idx-1] == "id") or ((s.tokenArr[s.idx-1] == "num")))):
            s.rparen += 1
            s.idx+=1
            s.checkStateS()
        #Erro cabuloso
        else :
            print("Erro Sintático")

    #Função para os estados de E
    def checkStateE(s):
        if(s.testOK()):
            print("Sucesso")
        #Teste para E -> E + E com E sendo um id
        elif(s.tokenArr[s.idx] == "id" and s.tokenArr[s.idx+1] == "+"):
            if((s.idx+2) > s.maximum):
                print("Erro Sintático")
            else:
                s.idx += 2
                s.checkStateE()
        #Teste para E -> E + E com E sendo um numero
        elif(s.tokenArr[s.idx] == "num" and s.tokenArr[s.idx+1] == "+"):
            if((s.idx+2) > s.maximum):
                print("Erro Sintático")
            else:
                s.idx += 2
                s.checkStateE()
        #Teste para apenas E -> id
        elif(s.tokenArr[s.idx] == "id"):
            s.idx += 1
            s.checkStateS()
        #Teste para apenas E -> num
        elif(s.tokenArr[s.idx] == "num"):
            s.idx += 1
            s.checkStateS()
        #Teste para E -> (S, E)
        elif(s.tokenArr[s.idx] == "("):
            if(s.idx+1 > s.maximum):
                print("Erro Sintático")
            else:
                s.lparen += 1
                s.idx += 1
                s.checkStateS()
        #Teste para E -> L,E
        elif(s.tokenArr[s.idx] == "," and ((s.tokenArr[s.idx-1] == "id") or ((s.tokenArr[s.idx-1] == "num")))):
            if(s.idx+1 > s.maximum):
                print("Erro Sintático")
            else:
                s.idx += 1
                s.checkStateE()
        #Teste para E -> L,E com L dentro do print
        elif(s.tokenArr[s.idx] == ")" and ((s.tokenArr[s.idx-1] == "id") or ((s.tokenArr[s.idx-1] == "num")))):
            s.rparen += 1
            s.idx += 1
            s.checkStateS()
        #Erro cabuloso
        else:
            print("Erro Sintático")
    
    #Função para checar os estados de L
    def checkStateL(s):
        if(s.testOK()):
            print("Sucesso")
        #Teste para L -> L,E
        elif(s.tokenArr[s.idx] == "," and ((s.tokenArr[s.idx-1] == "id") or ((s.tokenArr[s.idx-1] == "num")))):
            if(s.idx+1 > s.maximum):
                print("Erro Sintático")
            else:
                s.idx+=1
                s.checkStateE()
        #Caso onde L -> E
        #Se tiver algum erro, vai cair nos erros do checkStateE()
        else:
            s.checkStateE()
    

    #Função para determinar se o input está finalizado e se ele é aceito pela gramática
    def testOK(s):
        if(s.idx > s.maximum and s.lparen == s.rparen):
            return True
        else:
            return False

def main():
    while True:
        p = Parser()
        x = input("> ")
        if (x == "$"):
            sys.exit()
        else:
            p.checkSyntax(x)
            #print(p.tokenArr)

if __name__ == "__main__":
    main()

