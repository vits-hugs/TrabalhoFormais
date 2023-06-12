import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Objects import AFD

def read(s):
    text = open(s)

    N_estados = text.readline().rstrip()
    Estado_inicial = text.readline().rstrip()
    Estados_finais = {final for final in text.readline().rstrip().split(',')}
    alfabeto = {simbol for simbol in text.readline().rstrip().split(',')}

    # print(N_estados)
    # print(Estado_inicial)
    # print(Estados_finais)
    # print(alfabeto)

    transitions = {}
    x = 1
    while True:
        x = text.readline().rstrip().split(',')
        if x == ['']:
            break
        
        nome,char,estado_chegada = x 
        if nome in transitions:
            transitions[nome].transitions[char]= estado_chegada 
        else:    
            transitions[nome] = AFD.D_State(nome,{char:estado_chegada}) 
    text.close()

    return AFD.AFD(Estado_inicial, alfabeto, transitions, Estados_finais)

if __name__ == '__main__':
    print(read("AFND/afd.afd"))