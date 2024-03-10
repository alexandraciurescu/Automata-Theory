#Ciurescu Irina Alexandra
#Stoinea Maria Miruna
#grupa 142

#citirea datelor din fisierul 'cfg.in' care contine gramatica necesara validarii comenzilor
def task(fisier): #stocam datele de intrare din fisierul dat ca CFG intr-un dictionar
    sectiuni = {}
    with open(fisier) as f:
        linie=f.readline()
        linie=linie.rstrip("\n")
        ct=0
        while linie!="":
            if linie[0]=='[' and linie[-1]==']':
                if ct!=0:
                    sectiuni[cheie]=sectiune
                cheie = linie[1:len(linie) - 1]
                ct+=1
                sectiune=[]
            else:
                sectiune.append(linie)
            linie = f.readline()
            linie = linie.rstrip("\n")
    sectiuni[cheie]=sectiune
    ls=[]
    if "Rules" in sectiuni:
        for r in sectiuni["Rules"]:
            ls2 = r.split("->")
            m=ls2[1].split(",")
            ls.append((ls2[0],m))
        sectiuni["Rules"]=ls
    return sectiuni
def load_sections(fisier): #functie necesara pentru validarera sectiunilor din fisierul de intrare
    sectiuni=task(fisier)
    if "Vars" not in sectiuni:
        return []
    if "Sigma" not in sectiuni:
        return []
    if "Rules" not in sectiuni:
        return []
    ls=[]
    for sectiune in sectiuni:
        ls.append(sectiune)
    if len(ls)!=3:
        return []
    return ls

def load_vars(fisier): #functie necesara pentru validarea variabilelor din fisierul de intrare
    sectiuni=task(fisier)
    if "Vars" not in sectiuni:
        return []
    ls=[]
    for v in sectiuni["Vars"]:
        var=v.split(",")
        ls.append(var[0])
        if var[0].islower()!=0:
            return []
    return ls

def load_sigma(fisier): #functie necesara pentru validarea terminalelor din fisierul de intrare
    sectiuni=task(fisier)
    if "Sigma" not in sectiuni:
        return []
    ls=[]
    for l in sectiuni["Sigma"]:
        ls.append(l)
    return ls

def load_start(fisier): #validare si stocare variabila de start
    sectiuni=task(fisier)
    if "Vars" not in sectiuni:
        return []
    if len(sectiuni["Vars"])==0:
        return []
    if len(sectiuni["Vars"])==1:
        if sectiuni["Vars"][0][-1:]!="*":
            return []
        else:
            return [sectiuni["Vars"][0]]
    lsS=[]
    for var in sectiuni["Vars"]:
        if var[-1]=='*':
            lsS.append(var[:-2])
    if len(lsS)!=1:
        return []
    return lsS[0]

def load_rules(fisier): #validare reguli
    sectiuni=task(fisier)
    if "Rules" not in sectiuni:
        return []

    for regula in sectiuni["Rules"]:
        if regula[0] not in load_vars(fisier):
            return []
        for cuv in regula[1]:
            if cuv not in sectiuni["Sigma"] and cuv not in load_vars(fisier):
                return []
    return sectiuni["Rules"]

def recursiv_CFG(d,prop,index):
    ls=[]
    ok=0
    for i in range(index,len(d["Rules"])):
        rg=d["Rules"][i]
        s=rg[0]
        reg="".join(rg[1])
        if s in prop: #verificam daca o anumita regula trebuie aplicata
            ok=1
            prop_nou=prop
            prop_nou=prop_nou.replace(s,reg)
            var=recursiv_CFG(d, prop_nou,i+1)
            if len(var)>1:
                ls+=var
            else:
                ls.extend(var)
        i+=1
    if ok==0:
        for var in d["Vars"]:
            if var in prop:
                return []
        return [prop] #in cazul in care nu se mai aplica nicio regula, vom returna un singur string
    else:
        return ls #altfel returnam lista cu celelalte stringuri
def CFG(fisier,prop): #functie care returneaza toate stringurile pe care le poate genera o anumita gramatica data sub forma unui fisier de intrare
    if load_sections(fisier) == [] or load_sigma(fisier) == [] or load_vars(fisier) == [] or load_rules(fisier) == []:
        return -1
    d = task(fisier)
    return recursiv_CFG(d,prop,0)
print(CFG("cfg.in","COMMAND"))
comenzi=CFG("cfg.in","COMMAND")


def citire(fisier):  #citire fisier 'la.in' care contine datele automatului LA
    f = open(fisier)
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


def validare_comenzi(d,comenzi):
    ok=1
    for com in d['Sigma']:
        if com not in comenzi:
            print("Comanda invalida...")
            ok=0
            break
    if ok==1: print("Comenzile sunt valide:)")

def AfisareVecini(s):   #necesar pentru comanda 'LOOK' a jocului
    # Stocam intr-un dictionar descrierile camerelor si afisam descrierea camerelor respective
    descrieri = {"throneroom": "Throne Room:  The command center of the castle.",
                 "wizardsstudy": "Wizard’s Study:  A room teeming with mystical artifacts.",
                 "secretexit": "Secret Exit:  The hidden passage that leads out of the Castle of Illusions.",
                 "pantry": "Pantry:  A storage area for the Kitchen.",
                 "library": "Library:  A vast repository of ancient and enchanted texts.",
                 "treasury": "Treasury:  A glittering room overflowing with gold and gemstones.",
                 "armoury": "Armoury:  A chamber filled with antiquated weapons and armour.",
                 "kitchen": "Kitchen:  A room packed with peculiar ingredients.",
                 "diningroom": "Dining Room:  A room with a large table filled with an everlasting feast.",
                 "entrancehall": "Entrance Hall:  The grand foyer of the Castle of Illusions."
                 }
    print('Descriere:')
    print(descrieri[s])

    print("Vecini:")
    for trans in d['Trans']:
        ls = trans.split(',')
        si = ls[0]
        a1 = ls[1]
        sf = ls[3]
        if s==si:
            if 'go' in a1: print(sf)

def emulate_la():
    lista=[]
    stare_finala="secretexit"
    stare_curenta=input("Dati camera din care vreti sa plecati: ")
    ok=1
    while stare_curenta!=stare_finala and ok==1:
      c=input("Dati comanda: ")
      for trans in d['Trans']:
        ls=trans.split(',') #stocam elementele din tranzitie dupa forma data exemplu la ex1 cu LA-ul
        si=ls[0]
        a1=ls[1]           #(si,a1,s1)->(sf,a2,a3)
        s1=ls[2]
        sf=ls[3]
        a2=ls[4]
        a3= ls[5]
        b= ls[6]   #b poate fi 0 sau 1, 1 daca verificam existenta lui s1 in lista respectiv 0 pt inexistenta
        if si==stare_curenta and a1==c:
            ok1=1
            if a1=="look":
                AfisareVecini(si)
            if a1=="inventory":
                print("Item-uri disponibile: ")
                if len(lista)>0:
                    print(lista)
                else:
                    print("Lista vida")
            # tranzitie de forma: si a1 e sf e e 1 -> trecem in starea sf fara a face modificari
            if s1=='e' and a2=='e' and a3=='e':
                print("Tranzitie: ", trans)
                stare_curenta=sf
                break
            if b=='1': #'1' -> aplicam tranzitia doar daca s1 exista in lista
                # tranzitie de forma: si a1 e sf e a3 1
                if s1=='e' and a2=='e':
                    print("Tranzitie: ", trans)
                    if a3!='e' and a3 not in lista:
                        lista.append(a3)
                    stare_curenta=sf
                    break

                # tranzitie de forma: si a1 e sf a2 a3 1
                if s1 == 'e' and a2 != 'e':
                    print("Tranzitie: ", trans)
                    if a2 in lista:
                        poz=lista.index(a2)
                        lista.pop(poz)
                    if a3!='e' and a3 not in lista:
                        lista.append(a3)
                    stare_curenta = sf
                    break

                # tranzitie de forma: si a1 s1 sf e a3 1
                if s1 != 'e' and a2 == 'e':
                    print("Tranzitie: ", trans)
                    if s1 in lista:
                        if a3!='e' and a3 not in lista:
                            lista.append(a3)
                        stare_curenta = sf
                        break

                # tranzitie de forma: si a1 s1 sf a2 a3 1
                if s1 != 'e' and a2 != 'e':
                        print("Tranzitie: ", trans)
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
                    print("Tranzitie: ", trans)
                    if a3!='e' and a3 not in lista:
                        lista.append(a3)
                    stare_curenta = sf
                    break

                # tranzitie de forma: si a1 e sf a2 a3 0
                if s1 == 'e' and a2 != 'e':
                    print("Tranzitie: ", trans)
                    if a2 in lista:
                        poz = lista.index(a2)
                        lista.pop(poz)
                    if a3!='e' and a3 not in lista:
                        lista.append(a3)
                    stare_curenta = sf
                    break

                # tranzitie de forma: si a1 s1 sf e a3 0
                if s1 != 'e' and a2 == 'e':
                    print("Tranzitie: ", trans)
                    if a3!='e' and a3 not in lista:
                        lista.append(a3)
                    stare_curenta = sf
                    break

                # tranzitie de forma: si a1 s1 sf a2 a3 0
                if s1 != 'e' and a2 != 'e':
                    print("Tranzitie: ", trans)
                    if a2 in lista:
                        poz = lista.index(a2)
                        lista.pop(poz)
                        if a3!='e' and a3 not in lista:
                            lista.append(a3)
                        stare_curenta = sf
      if ok1 == 0:
        print("Comanda gresita!")
      if stare_curenta == stare_finala:
        print("Am ajuns in starea finala:D")
        break
      ok=input('Continuati 0 (nu) / 1 (da): ')




d=citire("la.in")
comenzi=CFG("cfg.in","COMMAND")
validare_comenzi(d,comenzi)
emulate_la()