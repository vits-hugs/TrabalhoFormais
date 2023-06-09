import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Objects import AFND

def read(s):
    text = open(s)

    N_estados = text.readline().rstrip()
    Estado_inicial = text.readline().rstrip()
    Estados_finais = text.readline().rstrip().split(',')
    alfabeto = set(text.readline().rstrip().split(','))
    if '&' in alfabeto:
        alfabeto.remove('&')

    transitions = {}
    x = 1
    while True:
        x = text.readline().rstrip().split(',')
        if x == ['']:
            break
        # Estado que nao chega em nenhum outro
        if len(x) == 1:
            transitions[x[0]] = AFND.N_State(x[0], {})
            continue
        
        nome,char,estado_chegada = x 
        estado_chegada = set(estado_chegada.split('-'))
        if nome in transitions:
            transitions[nome].transitions[char]= estado_chegada 
        else:    
            transitions[nome] = AFND.N_State(nome,{char:estado_chegada}) 
    text.close()

    return AFND.AFND(Estado_inicial,alfabeto,transitions,set(Estados_finais))

if __name__ == '__main__':
    print(read("Testes/AFD/epsilon.afnd"))