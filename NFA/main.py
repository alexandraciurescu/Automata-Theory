# CIURESCU IRINA ALEXANDRA
# GRUPA 142

#NFA

# Pentru epsilon am folosit 'e'

def citire():
    f = open("epsilon.in")
    d={}
    for linie in f:
        linie = linie.rstrip("\n")
        if linie[0] != '#':
            if linie[0] == '[' and linie[len(linie) - 1] == ']':
                cheie=linie[1:len(linie)-1]
                d[cheie]=[]
            else:
                d[cheie].append(linie)
    return d


def verificalfabet():
    ok=0
    for cheie in d:
        if cheie == "Sigma":
            ok = 1
            break
    if ok == 0:
        return 0
    else:
      if len(d["Sigma"])==0:
         return 0
      else:
         return 1


def verifstates():
    ok=s=t=0
    for cheie in d:
        if cheie=="States":
            ok=1
            break
    if ok==0:
        return 0
    else:
       if len(d["States"])<2:
        return 0
       else:
           for stare in d['States']:
             if len(stare)==4:
               if stare[3]=='s':
                   s=s+1
               if stare[3]=='f':
                   t=t+1
           if t>=1 and s==1:
               return 1
           else:
               return 0



def verifactions():
    ok = 0
    for cheie in d:
        if cheie == "Actions":
            ok = 1
            break
    if ok == 0:
        return 0
    else:
        ok=1
        for actiune in d['Actions']:
            ls=actiune.split(";")
            sirs1=ls[0]+",s"
            sirf1=ls[0]+",f"
            sirs2 = ls[2] + ",s"
            sirf2 = ls[2] + ",f"
            if not((ls[0] in d['States'] or sirs1 in d['States'] or sirf1 in d['States'])  and ls[1] in d['Sigma']
                   and (ls[2] in d['States'] or sirs2 in d['States'] or sirf2 in d['States'])):
               ok=0
        return ok



#generam matricea drumurilor
def RoyWarshall(matrice,n):
    for k in range(1, n+1):
        for i in range(1, n+1):
            for j in range(1, n+1):
                if matrice[i][k] and matrice[k][j]:
                    matrice[i][j] = 1


#generam toate drumurile dintre stari cu epsilon-tranzitii
def drumuri(d, matrice, n):
    # generam matricea de adiacenta asociata NFA-ului pentru epsilon-tranzitii
    for actiune  in d['Actions']:
        if actiune[3]=='e':
            ls=actiune.split(";")
            i=int(ls[0][1])
            j=int(ls[2][1])
            matrice[i][j]=1
    #print(matrice)
    RoyWarshall(matrice,n)
    #print(matrice)


#detemrinam multimea starilor finale
def starifinale(s,stari_finale):
    for s in d['States']:
        if s[3:] == 'f':
            stari_finale.add(int(s[1:2]))


def emulate_nfa(d,matrice,n,stari_finale,str):
   #verificam daca cuvantul contine doar caractere din alfabet
    for c in str:
        if c not in d['Sigma']:
            return 0

    #adaug starea initiala in starile curente
    stari_curente=set()
    for s in d['States']:
        if s[3:]=='s':
            stari_curente.add(int(s[1:2]))

    #precum si starile in care ajugem prin epsilon-tranzitii
    stari_epsilon=set()
    for x in stari_curente:
        for j in range(1, n + 1):
            if matrice[x][j]==1:
                stari_epsilon.add(j)
    for x in stari_epsilon:
        stari_curente.add(x)

    for c in str:
        #determinam multimea starilor accesibile din starile curente cu caracterul c
        stari_noi = set()
        for actiune in d['Actions']:
            if actiune[3]==c:
                ls = actiune.split(";")
                i = int(ls[0][1])
                j = int(ls[2][1])
                if i in stari_curente:
                    stari_noi.add(j);

        #starile curente vor fi acum starile in care s-a ajuns cu caracterul c
        stari_curente=set()
        for x in stari_noi:
            stari_curente.add(x)

        #aplicam si epsilon-tranzitiile pentru starile curente
        for x in stari_noi:
            for j in range(1, n + 1):
                if matrice[x][j]==1:
                    stari_curente.add(j);


    #verificam daca printre starile curente dupa parcurgerea completa a sirului se afla una din starile finale
    for x in stari_curente:
        if x in stari_finale:
            return 1
    return 0

#print(citire())
d=citire()

print("Verificare alfabet: ",verificalfabet())
print("Verificare actiuni: ",verifactions())
print("Verificare stari: ",verifstates())


n = len(d['States'])
matrice = [[0] * (n + 1) for _ in range(n + 1)]
drumuri(d,matrice,n)

stari_finale=set()
starifinale(d,stari_finale)
#print(stari_finale)


# teste pentru NFA fara epsilon-tranzitii (fisier de intrare noepsilon.in)
""" 
print(emulate_nfa(d,matrice,n,stari_finale,'ab'))  #1
print(emulate_nfa(d,matrice,n,stari_finale,'aba')) #0
print(emulate_nfa(d,matrice,n,stari_finale,'abab')) #1
print(emulate_nfa(d,matrice,n,stari_finale,'ad')) #0
print(emulate_nfa(d,matrice,n,stari_finale,'nuchichi')) #0
print(emulate_nfa(d,matrice,n,stari_finale,'a')) #1
print(emulate_nfa(d,matrice,n,stari_finale,'dausu')) #0
"""

# teste pentru NFA cu epsilon-tranzitii (fisier de intrare epsilon.in)
# (a|b)*ac
print(emulate_nfa(d,matrice,n,stari_finale,'aaaac'))  #1
print(emulate_nfa(d,matrice,n,stari_finale,'cabcc')) #0
print(emulate_nfa(d,matrice,n,stari_finale,'ac')) #1
print(emulate_nfa(d,matrice,n,stari_finale,'bbbbac')) #1
print(emulate_nfa(d,matrice,n,stari_finale,'abbbbbc')) #0
