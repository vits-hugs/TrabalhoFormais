import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Readers import GRReader
from Objects import GR

def has_direct_non_determinism(value:str,other :str, terminais):
    for x in range(len(value)):
        if value[x] in terminais:
            if value[x] != other[x]:
                return False,x
        else:
            if x == 0:
                return False,x
            return True,x
    return False,x

def remove_ND_direto(grammar : GR.Grammar):
    new_productions = grammar.productions.copy()
    for head,production in grammar.productions.items():
        remove_list = []

        i = 0 
        tam = len(production)

        while i < len(production)-1:
            ver = production[i]
            for x in range(i+1, tam):
                b,pos = has_direct_non_determinism(ver,production[x],grammar.terminais)
                #cprint(f"{ver}|{production[x]} : {b}")
                
                if b:
                    prod = ver[:pos]
                    NT = head + "@"
                    prod.append(NT)
                
                    new_productions[head].append(prod)

                    ar_ver = ver[pos:]
                    ar_prod = production[x][pos:]

                    if NT in new_productions:
                        new_productions[NT].append(ar_ver)
                        new_productions[NT].append(ar_prod)
                    else:
                        new_productions[NT] = []
                        new_productions[NT].append(ar_ver)
                        new_productions[NT].append(ar_prod)
                       

                    remove_list.append(ver)
                    remove_list.append(production[x])

            i+=1        

        for item in remove_list:
            if item in new_productions[head]:
                new_productions[head].remove(item)


    grammar.productions = new_productions        
if __name__ == '__main__':
    
    grammar = GRReader.read("GR/FatoraDireto.gr")
    #grammar.add_productions()
    print(grammar)
    print('-'*30)
    remove_ND_direto(grammar)
    print(grammar)


