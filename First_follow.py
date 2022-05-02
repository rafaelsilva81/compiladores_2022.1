count, n = 0
calc_first = {}
calc_follow = {}
m = 0
production = {}
f = [] 
first = []
k = 0
ck = ''
e = 0


def findFirst(c, q1, q2):
    if c.isupper() == False:
        first[n+1] = c
    
    for j in range(count):
        if production[j][0] == c:
            if production[j][2] == '#':
                if production[q1][q2] == '\0':
                    first[n+1] = '#'
                elif production[q1][q2] != '\0' and (q1 != 0 or q2 != 0):
                    findFirst(production[q1][q2], q1, (q2+1))
                else:
                    first[n+1] = '#'
            elif production[j][2].isupper() == False:
                first[n+1] = production[j][2]
            else:
                findFirst(production[j][2], j, 3)


def follow(c):
    if production[0][0] == c:
        f[m+1] = '$'
    
    for i in range(10):
        for j in range(2,10):
            if production[i][j] == c:
                if production[i][j+1] != '\0':
                    followFirst(production[i][j+1], i, (j+2))
                if production[i][j+1] == '\0' and c != production[i][0]:
                    follow(production[i][0])


def followFirst(c, c1, c2):
    if c.isupper == False:
        f[m+1] = c
    else:
        j = 1
        for i in range(count):
            if calc_first[i][0] == c:
                break
        while calc_first[i][j] != '!':
            if calc_first[i][j] != '#':
                f[m+1] = calc_first[i][j]
            else:
                if production[c1][c2] == '\0':
                    follow(production[c1][0])
                else:
                    followFirst(production[c1][c2], c1, c2+1)
            j += 1
    
def main():
    jm = 0
    km = 0
    i, choice =0 
    c = ''
    ch = ''
    count = 8
    point1 = 0
    point2 = 0
    xxx = 0
    done = []
    ptr = -1

    production[0] = "E=TR"
    production[1] = "R=+TR"
    production[2] = "R=#"
    production[3] = "T=FY"
    production[4] = "Y=*FY"
    production[5] = "Y=#"
    production[6] = "F=(E)"
    production[7] = "F=i"


    for k in range(count):
        for kay in range(100):
            calc_first[k][kay] = '!'
    
    for k in range(count):
        c = production[k][0]
        point2 = 0
        xxx = 0

        

     