#Ciurescu Irina Alexandra
#Stoinea Maria Miruna
#grupa 142

def citire(fisier): #citirea si memorarea datelor LA-ului in dictionarul d
    f = open(fisier)
    d={}
    for linie in f:
        linie = linie.rstrip("\n")
        if linie[0] != '#' :
            if linie[0] == '[' and linie[len(linie) - 1] == ']':
                cheie=linie[1:len(linie)-1]
                d[cheie]=[]
            else:
                d[cheie].append(linie)
    print(d)
    return d


#validare tranformari LA
def validate_trans(d):
    if 'e' in d['Sigma']: return 0
    for trans in d['Trans']:
        ls=trans.split(',')
        if ls[0] not in d['States'] and ls[0]+',f' not in d['States'] and ls[0]+',s' not in d['States'] and ls[0]+',s,f' not in d['States']:
            return 0
        if ls[1] not in d['Sigma']:
            return 0
        if ls[2] not in d['Gama'] :
            return 0
        if ls[3] not in d['States'] and ls[3]+',f' not in d['States'] and ls[3]+',s' not in d['States'] and ls[3]+',s,f' not in d['States']:
            return 0
        if ls[4] not in d['Gama'] or ls[5] not in d['Gama']:
            return 0
        if ls[6]!='1' and ls[6]!='0': return 0
    return 1


def emulate_la(string,fisier):
    d=citire(fisier)
    if validate_trans(d) == 0:
        print("nu")
        return 0
    #cautam starea de start si starile finale si le memoram
    stari_finale=[]
    start=''
    for stare in d["States"]:
        #print(stare)
        if stare[2:]==',s,f':
            start = stare[:(len(stare) - 4)]
            stari_finale.append(stare[:(len(stare) - 4)])
            continue
        if stare[len(stare)-1]=='s':
            start=stare[:(len(stare)-2)]
            continue
        if stare[len(stare)-1]=='f':
            stari_finale.append(stare[:(len(stare)-2)])
            continue


    lista=[]
    #print('start:',start)
    #print('finale:',stari_finale)
    stare_curenta=start
    for c in string: #pentru fiecare caracter din sirul dat
      #print(stare_curenta)
      for trans in d['Trans']:
        ls=trans.split(',') #pt fiecare tranzitie, vom memora datele conform exemplului din ex1
        si=ls[0]           #(si,a1,s1)->(sf,a2,a3)
        a1=ls[1]
        s1=ls[2]
        sf=ls[3]
        a2=ls[4]
        a3= ls[5]
        b= ls[6]   #b poate fi 0 sau 1 (1->verifica apartenta lui s1 la lista si 0->verifica absenta)
        if si==stare_curenta and a1==c:
            # tranzitie de forma: si a1 e sf e e 0 -> trecem in starea sf fara a face modificari
            if s1=='e' and a2=='e' and a3=='e':
                stare_curenta=sf
                break
            if b=='1': #'1' -> aplicam tranzitia doar daca s1 exista in lista

                # tranzitie de forma: si a1 e sf e a3 1
                if s1=='e' and a2=='e':
                    if a3!='e' and a3 not in lista:
                        lista.append(a3)
                    stare_curenta=sf
                    break

                # tranzitie de forma: si a1 e sf a2 a3 1
                if s1 == 'e' and a2 != 'e':
                    if a2 in lista:
                        poz=lista.index(a2)
                        lista.pop(poz)
                    if a3!='e' and a3 not in lista:
                        lista.append(a3)
                    stare_curenta = sf
                    break

                # tranzitie de forma: si a1 s1 sf e a3 1
                if s1 != 'e' and a2 == 'e':
                    if s1 in lista:
                        if a3!='e' and a3 not in lista:
                            lista.append(a3)
                        stare_curenta = sf
                        break

                # tranzitie de forma: si a1 s1 sf a2 a3 1
                if s1 != 'e' and a2 != 'e':
                        if s1 in lista:
                            if a2 in lista:
                                poz = lista.index(a2)
                                lista.pop(poz)
                            if a3!='e' and a3 not in lista:
                                lista.append(a3)
                            stare_curenta = sf
                            break

            if b == '0':  # '0'   ->  aplicam tranzitia indiferent daca s1 este sau nu in lista
                # tranzitie de forma: si a1 e sf e a3 0
                if s1 == 'e' and a2 == 'e':
                    if a3!='e' and a3 not in lista:
                        lista.append(a3)
                    stare_curenta = sf
                    break

                # tranzitie de forma: si a1 e sf a2 a3 0
                if s1 == 'e' and a2 != 'e':
                    if a2 in lista:
                        poz = lista.index(a2)
                        lista.pop(poz)
                    if a3!='e' and a3 not in lista:
                        lista.append(a3)
                    stare_curenta = sf
                    break

                # tranzitie de forma: si a1 s1 sf e a3 0
                if s1 != 'e' and a2 == 'e':
                    if a3!='e' and a3 not in lista:
                        lista.append(a3)
                    stare_curenta = sf
                    break

                # tranzitie de forma: si a1 s1 sf a2 a3 0
                if s1 != 'e' and a2 != 'e':
                    if a2 in lista:
                        poz = lista.index(a2)
                        lista.pop(poz)
                        if a3!='e' and a3 not in lista:
                            lista.append(a3)
                        stare_curenta = sf
                        break


    if stare_curenta in stari_finale: #conditia de accept
        return 1
    else: return 0

#d=citire("la2.in")

# siruri de forma aaaaa...abbbbbbb sau bbbbb...baaa...a (a+b+ sau b+a+)
print(emulate_la("bbbaaa","la.in"))

# siruri formate din caracterele a si b care contin numar par de litere 'b'
print(emulate_la("aabbaabbaaaaabb","la2.in"))