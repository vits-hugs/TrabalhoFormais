import sys
import os
from copy import deepcopy

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Readers import GRReader
from Objects import GR

def has_direct_non_determinism(value:str,other :str, terminais):
    if is_only_terminals(other,terminais):
        return False,-1
    for x in range(len(value)):
        if value[x] in terminais:
            if value[x] != other[x]:
                return False,x
        else:
            if x == 0:
                return False,x
            return True,x
    return False,x

def is_only_terminals(value: list,terminais):
    for v in value:
        if v not in terminais:
            return False
    return True

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
                #print(f"{ver}|{production[x]} : {b}")
                
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

    DCT = {} # Dicionario produções com Terminais
    for key,list_production in gr.productions.items():
        for production in list_production:
            #Considerando apenas 1 terminal no começo
            terminais,B = prod_Terminais(production,gr.terminais)
            if production[0] in gr.terminais:
                if key in DCT:
                    DCT[key].extend(terminais) #TODO por prod_terminais
                else:
                    
                    DCT[key] = terminais
            else:
                if key in DCT:
                   DCT.pop(key)
                break

    # Condição 2: Precisa começar uma produção com Não Terminal, se alguma outra produção possuir
    # NT no começo adiciona ele
    # Se nenhuma outra produção começa com NT e todas suas produções começam com terminal
    # Verificar se há intersecção entre o começo de suas produções e a produção em que ele está
    #  

    ret = True
    for key,production in gr.productions.items():
        if key not in DCT:
            problemas = find_problemas(production,gr.terminais,DCT)
            for prob in problemas:
                desfaz_indireto(prob,gr.productions[prob],production)
            #Se problemas foram encontrados
            if len(problemas) > 0:
                return False
    return ret 

#Acha NT que podem vir a gerar ND 
#Para não ter problemas os Terminais iniciais da produção + terminais iniciais do Não terminal
#devem ser diferentes dos resto das produções 

def find_problemas(productions,terminais,DCT : dict[str,list]):
    productions = deepcopy(productions)
    problemas = []
    for i in range(len(productions)-1):    

        #Função
        T_List,NT = prod_Terminais(productions[i],terminais)
        T_Lists = [T_List]
        if NT in DCT:
            T_Lists = create_Tlists(T_List,DCT[NT])
        if T_Lists == [[]]:
            problemas.append(NT)    
            continue

        for j in range(i+1,len(productions)): 
            OT_List,ONT = prod_Terminais(productions[j],terminais)
            OT_Lists = [OT_List]
                
            if ONT in DCT:
                OT_Lists = create_Tlists(OT_List,DCT[ONT])
                                
                if can_generate_ND(T_Lists,OT_Lists):
                    problemas.append(NT)
                    problemas.append(ONT)
            else:
               if can_generate_ND(T_Lists,OT_Lists):
                   problemas.append(NT)
      
    print(f"PROBLEMAS: {problemas}")
    return problemas


#Cria uma lista com começo de cada produção
def create_Tlists(T_list: list , prod_caracters): 
    T_lists = []
    for prod in prod_caracters:
        new = T_list.copy()
        new.extend(prod)
        T_lists.append(new)
    return T_lists

#Se pode haver ND entre 2 produções
def can_generate_ND(A_list:list[str],Other_list:list[str]):
    if Other_list == [[]]:
        return True
    for A in A_list:
        for O in Other_list:
            if O[:len(A)] == A:
                return True
    return False

#retorna terminais 
# Cuidar se haver somente terminais                    
def prod_Terminais(production,terminais):
    for i in range(len(production)):
        if production[i] not in terminais:
            return production[:i],production[i]
    return production,True

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


#FAZER PILHA PARA RETORNAR "MELHOR GRAMATICA"
def remove_ND(gr : GR.Grammar):
    pilha_gr = [deepcopy(gr)]
    while True:
        modificado = remove_ND_direto(gr)
        if modificado:
            pilha_gr.append(deepcopy(gr))
        possibleT = remove_ND_indireto(gr)
        if not modificado and  possibleT:
            break
        print(gr)
        
    return pilha_gr[-1]


if __name__ == '__main__':
    #REMOVER & da gramatica para simplificar
    grammar = GRReader.read("GR/Testes_Fatora/indireto2.gr")
    print(grammar)

    L = remove_ND(grammar)
    print("RESULTADO:")
    print(L)