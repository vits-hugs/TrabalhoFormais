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

#Gerar D_Direto 
# Verifica se não fica infinito 
def gera_ND_indireto(gr: GR.Grammar):
    algo = False
    problemas = []
    for head,production in grammar.productions.items():
        for prod in production:
            if prod[0] not in grammar.terminais:
                problemas.append(prod[0])
    problemas = list(set(problemas))
    print(f"problemas : {problemas}")
    problemas.remove('C')
    for head,production in grammar.productions.items():
        for prob in problemas:
            if prob != head:
                algo = desfaz_indireto(prob,grammar.productions[prob],production)

    return algo
def desfaz_indireto(prob,sub,production):
    bosta = False
    new_prod = production.copy()
    for prod in production:
        
        rm = False
        for i in range(len(prod)):
            if prod[i] == prob:
                bosta = True 
                for x in range(len(sub)):
                   
                    resp = prod[:i]
                    resp.extend(sub[x])
                    resp.extend(prod[i+1:])
                    new_prod.append(resp)
                rm = True
        if rm: 
            new_prod.remove(prod)
    production.clear()
    production.extend(new_prod)
    return bosta

def remove_ND(gr : GR.Grammar):
    print(grammar)
    print('-'*30)
    bosta = True 
    for x in range(2):
        remove_ND_direto(grammar)
                
        print(grammar)

        bosta = gera_ND_indireto(grammar)
        print(grammar)



if __name__ == '__main__':
    #REMOVER & da gramatica para simplificar
    grammar = GRReader.read("GR/ProfFatoraIndireto.gr")
    #grammar.add_productions()
    # print(grammar)
    # print('-'*30)
    # remove_ND_direto(grammar)
    # print(grammar)

    # gera_ND_indireto(grammar)
    # print(grammar)

    remove_ND(grammar)