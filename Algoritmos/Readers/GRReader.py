import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Objects.GR import Grammar

def read(s):
    with open(s) as text:

        productions = {}
        Terminais = set()
        first = text.readline()
        if '->' not in first:
            Terminais = set(first.rstrip().replace(' ','').split(','))
            first = text.readline()

        line  = first.rstrip().replace(' ','').split('->')
        
        inital_simbol = line[0]
        while True:
            if line == ['']:
                break

            productions[line[0]] = list(map(list,line[1].split('|')))
            line = text.readline().rstrip().replace(' ','').split('->')
    #Close Text

    NTerminais = productions.keys()
    if Terminais != set():
        new_production = {}
        for key,value in productions.items():
            new_production[key] = []
            for production in value:
                new_production[key].append(treat_production(production,Terminais.union(NTerminais)))
        productions = new_production
    else:
        for production_array in productions.values():
            for production in production_array:
                [Terminais.add(x) for x in production]

    
    Terminais.difference_update(productions.keys())
    Terminais.difference_update('&')
    return Grammar(inital_simbol,Terminais,productions)

#LookAhead do tamanho da maior produção
def treat_production(production: list,Simbolos : set):
    max_look_ahead = max([len(simbol) for simbol in Simbolos])
    lookAhead = max_look_ahead
    new_production = []
    i = 0
    while i < len(production):
        substr = ''.join(production[i:i+lookAhead])
        if substr in Simbolos.union('&'):
            new_production.append(substr)
            i+=lookAhead   
            lookAhead = max_look_ahead    
            continue
        lookAhead -= 1        
        if lookAhead <=0:
            raise Exception(f"Produção {production} a partir de {substr} em [{i}] não pode ser resolvido (definição não encontrada)") 
            
    return new_production


if __name__ == '__main__':
    print(read("GR/test_caracter.gr"))