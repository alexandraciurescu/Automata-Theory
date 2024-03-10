# CIURESCU IRINA ALEXANDRA
# GRUPA 142

# PDA
# Pentru epsilon am folosit caracterul 'e'

#citire pda
def citire():
    f = open("fpda.in")
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


#validare tranformari pda
def validate_trans(d):
    for trans in d['Trans']:
        ls=trans.split(',')
        if ls[0] not in d['States'] and ls[0]+',f' not in d['States'] and ls[0]+',s' not in d['States']:
            return 0
        if ls[1] not in d['Sigma']:
            return 0
        if ls[2] not in d['Gama'] or ls[3] not in d['Gama']:
            return 0
        if ls[4] not in d['States'] and ls[4] + ',f' not in d['States'] and ls[4] + ',s' not in d['States']:
            return 0
    return 1


#detemrinam multimea starilor finale
def StariFinale(d,stari_finale):
    for s in d['States']:
        if s[3:] == 'f':
            stari_finale.append((int(s[1:2]),""))


def emulate_pda(d,stari_finale,str):
   #verificam daca cuvantul contine doar caractere din alfabet
    for c in str:
        if c not in d['Sigma']:
            return 0

    #memorez "stiva" sub forma unui sir de caractere
    #consideram varful stivei primul element al sirului

    #adaug starea initiala in starile curente sub forma (stare, stiva), stiva fiind vida initial
    stari_curente=[]
    for s in d['States']:
        if s[3:]=='s':
            stari_curente.append((int(s[1:2]),""))

    #adaug si starile in care ajungem prin epsilon-tranzitii
    stari_epsilon=[]
    for x in stari_curente:
       stari_aux=[]  #lista in care memoram starile vizitate si necercetate tot sub forma (stare, stiva)
       stari_aux.append(x)
       while len(stari_aux)!=0:
           y=stari_aux[0]
           stari_aux.pop(0)

           #cautam toate starile in care se poate ajunge cu epsilon-tranzitii din starea y[0]
           for t in d["Trans"]:    #printre tranzitiile date
               ls=t.split(',')
               i=int(ls[0][1:])
               if i==y[0]:
                j=int(ls[4][1:])
                if ls[1]=='e':   # am gasit o epsilon-tranzitie si trebuie sa analizam separat fiecare tip

                    # tranzitie de tipul i e e e j -> mergem in j fara sa modificam stiva
                   if ls[2]=='e' and ls[3]=='e' and (j, y[1]) not in stari_epsilon:
                       stari_epsilon.append((j,y[1]))
                       stari_aux.append((j, y[1]))

                    # tranzitie de tipul i e e X j -> -> mergem in j doar adaugand la stiva pe X
                   if ls[2]=='e' and ls[3]!='e' and (j, ls[3]+y[1]) not in stari_epsilon:
                       stari_epsilon.append((j,ls[3]+y[1]))
                       stari_aux.append((j, ls[3]+y[1]))

                    # tranzitie de tipul i e X e j -> -> mergem in j doar daca in varful stivei se afla X pe care il eliminam de pe stiva
                   if ls[2]!='e' and ls[3]=='e' and len(y[1])>0:
                       if y[1][0]==ls[2] and (j, y[1][1:]) not in stari_epsilon:
                           stari_epsilon.append((j,y[1][1:]))
                           stari_aux.append((j, y[1][1:]))

                    # tranzitie de tipul i e X Y j -> -> mergem in j doar daca in varful stivei se afla X pe care il eliminam si il adaugam pe stiva pe Y
                   if ls[2]!='e' and ls[3]!='e' and len(y[1])>0:
                       if ls[2]==y[1][0] and (j, ls[3] + y[1][1:]) not in stari_epsilon:
                           stari_epsilon.append((j,ls[3]+y[1][1:]))
                           stari_aux.append((j, ls[3] + y[1][1:]))


    #adaugam la starile curente starile in care am ajuns prin epsilon-tranzitii
    for x in stari_epsilon:
        if x not in stari_curente:
            stari_curente.append(x)

    #pentru fiecare caracter din sirul dat
    for c in str:
        # determinam multimea starilor accesibile din starile curente cu caracterul c
        stari_noi = []
        for y in stari_curente:
                # cautam toate starile in care se poate ajunge cu simbolul c dintr-o stare curenta y[0]
                for t in d["Trans"]:
                    ls = t.split(',')
                    i = int(ls[0][1:])  # starea initiala i
                    if i == y[0]:
                        j = int(ls[4][1:])  # starea finala j
                        if ls[1] == c:
                            # tranzitie de tipul i c e e j
                            if ls[2] == 'e' and ls[3] == 'e' and (j, y[1]) not in stari_noi:
                                stari_noi.append((j, y[1]))
                            # tranzitie de tipul i c e X j
                            if ls[2] == 'e' and ls[3] != 'e' and (j, ls[3] + y[1]) not in stari_noi:
                                stari_noi.append((j, ls[3] + y[1]))
                            # tranzitie de tipul i c X e j
                            if ls[2] != 'e' and ls[3] == 'e'  and len(y[1])>0:
                                if y[1][0] == ls[2] and (j, y[1][1:]) not in stari_noi:
                                    stari_noi.append((j, y[1][1:]))
                            # tranzitie de tipul i c X Y j
                            if ls[2] != 'e' and ls[3] != 'e' and len(y[1])>0:
                                if ls[2] == y[1][0] and (j, ls[3] + y[1][1:]) not in stari_noi:
                                    stari_noi.append((j, ls[3] + y[1][1:]))

        #starile curente vor fi acum starile in care s-a ajuns cu caracterul c
        stari_curente=[]
        for x in stari_noi:
            if x not in stari_curente:
                stari_curente.append(x)

        #aplicam si epsilon-tranzitiile pentru starile curente obtinute
        stari_epsilon = []
        for x in stari_curente:
            stari_aux = []
            stari_aux.append(x)
            while len(stari_aux) != 0:
                y = stari_aux[0]
                stari_aux.pop(0)
                for t in d["Trans"]:
                    ls = t.split(',')
                    i = int(ls[0][1:])
                    if i == y[0]:
                        j = int(ls[4][1:])
                        if ls[1] == 'e':
                            if ls[2] == 'e' and ls[3] == 'e' and (j, y[1]) not in stari_epsilon:
                                stari_epsilon.append((j, y[1]))
                                stari_aux.append((j, y[1]))
                            if ls[2] == 'e' and ls[3] != 'e' and (j, ls[3] + y[1]) not in stari_epsilon:
                                stari_epsilon.append((j, ls[3] + y[1]))
                                stari_aux.append((j, ls[3] + y[1]))
                            if ls[2] != 'e' and ls[3] == 'e' and len(y[1])>0:
                                if y[1][0] == ls[2] and (j, y[1][1:]) not in stari_epsilon:
                                    stari_epsilon.append((j, y[1][1:]))
                                    stari_aux.append((j, y[1][1:]))
                            if ls[2] != 'e' and ls[3] != 'e' and len(y[1])>0:
                                if ls[2] == y[1][0] and (j, ls[3] + y[1][1:]) not in stari_epsilon:
                                    stari_epsilon.append((j, ls[3] + y[1][1:]))
                                    stari_aux.append((j, ls[3] + y[1][1:]))

        #adaugam la starile curente toate starile in care am ajuns prin epsilon-tranzitii
        for x in stari_epsilon:
            if x not in stari_curente:
                stari_curente.append(x)


    # verificam daca printre starile curente dupa parcurgerea completa a sirului se afla una din starile finale
    #print(stari_curente)
    for x in stari_curente:
        if x in stari_finale:
            return 1
    return 0


d=citire()
#print(d)
print("Validare tranzitii: ",validate_trans(d))
stari_finale=[]
StariFinale(d,stari_finale)


# Teste pentru fpda.in -> a^i b^j c^k unde i=j sau i=k
print("aaabbbccc: ",emulate_pda(d,stari_finale,"aaabbbccc"))
print("aabbcc: ",emulate_pda(d,stari_finale,"aabbcc"))
print("abbcc: ",emulate_pda(d,stari_finale,"abbcc"))
print("b: ",emulate_pda(d,stari_finale,"b"))
print("aabb: ",emulate_pda(d,stari_finale,"aabb"))
print("aaabbcc: ",emulate_pda(d,stari_finale,"aaabbcc"))


#Teste pentru fpda1.in -> siruri w w^r formate din 0 si 1
"""
print("001100: ",emulate_pda(d,stari_finale,"001100"))
print("00100100: ",emulate_pda(d,stari_finale,"00100100"))
print("0000: ",emulate_pda(d,stari_finale,"0000"))
print("10011000: ",emulate_pda(d,stari_finale,"10011000"))
print("01: ",emulate_pda(d,stari_finale,"01"))
print("0101010: ",emulate_pda(d,stari_finale,"0101010"))
"""