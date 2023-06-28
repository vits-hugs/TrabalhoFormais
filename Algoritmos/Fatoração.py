import sys
import os
from copy import deepcopy

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
    modificado = False 
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
                    modificado = True
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
    return modificado

#Gerar D_Direto 
# Verifica se não fica infinito 
def remove_ND_indireto(gr: GR.Grammar):
    # Condição 1: Gerar uma lista dos NTs cujas produções começam somente com Terminais

    DST = {} # Dicionario de S
    for key,list_production in gr.productions.items():
        for production in list_production:
            #Considerando apenas 1 terminal no começo
            if production[0] in gr.terminais:
                if key in DST:
                    DST[key].append(production[0])
                else:
                    DST[key] = [production[0]]
            else:
                if key in DST:
                   DST.pop(key)

    print(DST)

    # Condição 2: Precisa começar uma produção com Não Terminal, se alguma outra produção possuir
    # NT no começo adiciona ele
    # Se nenhuma outra produção começa com NT e todas suas produções começam com terminal
    # Verificar se há intersecção entre o começo de suas produções e a produção em que ele está
    #  
    ret = True
    for key,production in gr.productions.items():
        if key not in DST:
            problemas = find_problemas(production,gr.terminais,DST)
            for prob in problemas:
                ret = False
                desfaz_indireto(prob,gr.productions[prob],production)
    return ret 

#Acha NT que podem vir a gerar ND 
def find_problemas(productions,terminais,DST):
    problemas = []
    for i in range(len(productions)-1):    
        c = prod_Terminais(productions[i],terminais)
        
        for j in range(i+1,len(productions)): 
            if c == []: # começa com NT 
                other = prod_Terminais(productions[j],terminais)
                if other == []:
                    problemas.append(productions[j][0])
                    problemas.append(productions[i][0])

                if productions[i][0] in DST:
                    if other in DST[productions[i][0]]:
                        problemas.append(productions[i][0])
    
    print(f"PROBLEMAS: {problemas}")
    return problemas
 
#retorna terminais                    
def prod_Terminais(production,terminais):
    for i in range(len(production)):
        if production[i] not in terminais:
            return production[:i]
        

#Desfaz determinismo indireto
def desfaz_indireto(prob,prob_production_list,production_list):
    remover = []
    for i in range(len(production_list)):
        if prob == production_list[i][0]:
            remover.append(i)
            for x in prob_production_list:
                nova =  x.copy()
                nova.extend(production_list[i][1:])

                production_list.append(nova)
    for x in remover:
        production_list[x] = 'APAGAR'
    
    while 'APAGAR' in production_list:
        production_list.remove('APAGAR')
    print(production_list)


def remove_ND(gr : GR.Grammar):
    print(grammar)
    print('-'*30)
    while True:
        modificado = remove_ND_direto(grammar)
        old_grammar = deepcopy(grammar)

        possibleT = remove_ND_direto(grammar)
        if not modificado and  possibleT:
            print(old_grammar)
            break
     
        print(grammar)



if __name__ == '__main__':
    #REMOVER & da gramatica para simplificar
    grammar = GRReader.read("GR/ProfFatoraIndireto.gr")
    # remove_ND_direto(grammar)
    # print(grammar)
    # possibleTerminals(grammar)


    remove_ND(grammar)