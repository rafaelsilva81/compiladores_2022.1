
import sys

class Parser:

    """ Observação : Estou usando `s` no lugar de `self`
    Isso é totalmente possível no python, ainda que não seja a melhor prática """

    def __init__(s):
        s.idx = 0 #Index de leitura
        s.lparen = 0
        s.rparen = 0 #rparen também conta para o colchete fechando "]"
        s.grammar = {
            1: 'S-> B $',
            2: 'B-> id P',
            3: 'B-> id ( E ]',
            4: 'P-> ɛ',
            5: 'P-> ( E )',
            6: 'E-> B',
            7: 'E-> B , E',
        }

    def checkSyntax(s, userInput):
        s.row = userInput
        s.tokenArr = userInput.split(" ")
        s.maximum = len(s.tokenArr) - 1
        s.tokenArr.append(" ")
        s.analyseSyntax()
    
    #Função para os estados de S
    def analyseSyntax(s):
        if (s.testOK()):
            print("Sucesso")
        elif(s.tokenArr[s.idx] == "id" and s.tokenArr[s.idx+1] == "("):
            if((s.idx+2) > s.maximum):
                print("Erro Sintático")
            else:
               s.lparen+=1
               s.idx+=2
               s.analyseSyntax()
        elif(s.tokenArr[s.idx] == "]" and s.tokenArr[s.idx+1] == ","):
            if((s.idx+2) > s.maximum):
                print("Erro Sintático")
            else:
                s.rparen+=1
                s.idx+=2
                s.analyseSyntax()
        elif(s.tokenArr[s.idx] == ")" and s.tokenArr[s.idx+1] == "]"):
            s.rparen = s.rparen + 2
            s.idx = s.idx + 2
            s.analyseSyntax()
        elif(s.tokenArr[s.idx] == "id"):
            if((s.idx == 0)):
                s.idx+=1
                s.analyseSyntax()
            elif(s.tokenArr[s.idx-1] == "," or s.tokenArr[s.idx-1] == "("):
                s.idx +=1
                s.analyseSyntax()
        elif(s.tokenArr[s.idx] == ")" and (s.tokenArr[s.idx-1] == "id" or s.tokenArr[s.idx-1] == ")" or s.tokenArr[s.idx-1] == "]")):
            s.rparen += 1
            s.idx += 1
            s.analyseSyntax()
        elif(s.tokenArr[s.idx] == "]"):
            if(s.tokenArr[s.idx-1] == "," or s.tokenArr[s.idx-1] == "("):
                print("Erro Sintático")
            else:
                s.rparen += 1
                s.idx += 1
                s.analyseSyntax()
        elif(s.tokenArr[s.idx] == ","):
            s.idx += 1
            s.analyseSyntax()
        else:
            print("Erro Sintático")

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

