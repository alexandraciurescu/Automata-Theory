# CIURESCU IRINA ALEXANDRA
# GRUPA 142

# DFA

#am considerat starile ca fiind de forma q0, q1,..., q9

def citire():    #memoram datele despre dfa in dictionarul d
    f = open("lab2.in")
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



def emulate_dfa(d,str):
    for c in str:  #verificare - toate caracterele din sir sa fie din alfabet
        if c not in d['Sigma']:
            return 0

    for stare in d['States']:  #determin starea de start
        if ',s' in stare:
            ls=stare.split(',')
            starecurenta=ls[0]

    for c in str:
        ok=0
        #print(starecurenta)
        for actiune in d['Actions']:
            ls=actiune.split(';')
            if ls[1]==c and ls[0]==starecurenta:
                starecurenta=ls[2]
                ok=1
            if ok==1: break  #am gasit o actiune, deci nu mai cautam
        if ok==0:
          return 0

    s=starecurenta+",f"

    if s in d['States']:    #verificam daca starea in care am ajuns este un accept state
        return 1
    else:
        return 0


#print(citire())

d=citire()
print('Verificare alfabet: ',verificalfabet())
print('Verificare stari: ',verifstates())
print('Verificare actiuni: ',verifactions())

print(emulate_dfa(d,'0001100'))





