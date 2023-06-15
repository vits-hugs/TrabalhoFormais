import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Readers import GRReader
from Objects import GR

def has_direct_non_determinismo(value:str,other :str, terminais):

    for x in range(len(value)):
        if value[x] in terminais:
            if value[x] != other[x]:
                return False
        else:
            if x == 0:
                return False
            return True

def remove_ND_direto(grammar : GR.Grammar):
    print(grammar.productions)
    for head,production in grammar.productions.items():
        for i in range(len(production)):

        
            ver = production[i]

            for x in range(i+1,(len(production)) ):
                b = has_direct_non_determinismo(ver,production[x],grammar.terminais)
                print(production, end=": ")
                print(b)


if __name__ == '__main__':
    
    grammar = GRReader.read("GR/direto.gr")
    remove_ND_direto(grammar)


