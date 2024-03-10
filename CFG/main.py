# CIURESCU IRINA ALEXANDRA
# GRUPA 142

# CFG

def citire():
    f = open("fisier2.txt")
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


def validaterules():
    for regula in d['Rules']:   #verific ca regulile sa contina "->"
        poz=regula.find('-')
        if regula[poz+1]!='>':
            return 0

        var=regula[:poz]  #verific variabila din stanga sagetii
        if var not in d['Vars'] and var+',*' not in d['Vars']: return 0

        string=regula[poz+2:]   #verific ca dupa sageata sa am variabile si/sau terminale
        ls=string.split(',')
        for sir in ls:
            if 'A'<=sir[0]<='Z':
                if sir not in d['Vars'] and sir+',*' not in d['Vars']:
                    return 0
            elif 'a'<=sir[0]<='z':
                if sir not in d['Sigma']:
                    return 0
    return 1


def validarestart():
    ct=0
    for var in d['Vars']:
        if var[len(var)-2:]==',*':
            ct+=1
    if ct==1: return 1
    else: return 0


def find_start():
    #gasim variabila de start
    for var in d['Vars']:
        if var[len(var)-2:]==',*':
            start=var[:len(var)-2]
    return start


def transform_string(string,start):
    pozitie = string.find(start)  #caut variabila din sirul start in string
    pozitiefinala = pozitie + len(start) - 1
    string2 = string[pozitiefinala + 1:]  #subsirul aflat imediat dupa aparitia lui start in string

    for regula in d['Rules']:   #aplicam prima regula pe care o gasim
        poz = regula.find('-')
        if regula[:poz] == start:
            poz = regula.find('>')
            poz1 = regula.find(',')
            if(poz1==-1):
                output=regula[poz+1:]
            else:
                  ls=regula[poz+1:].split(',')
                  output =''.join(ls)  #daca din regula -> mai multe variabile si/sau terminale - le punem pe toate, eliminand virgulele

            string = string[:pozitie] + output + string2  #inlocuim in string subsirul start conform regulii gasite
            #print(string)
            break

    start='-'
    for v in d['Vars']:  #determinam noua variabila pe care vrem sa o inlocuim in variabila start
        if(v[len(v)-1]=='*'): v=v[:len(v)-2]
        poz=string.find(v)
        if poz!=-1:
            start=v
            break
    if start=='-':
        return string

    return transform_string(string,start)



#print(citire())
d=citire()

print("Validate rules:",validaterules())
print("Validate start:",validarestart())


string='COMMANDROOM'
start=find_start()
print(transform_string(string,start))
