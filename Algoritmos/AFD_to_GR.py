import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Readers import AFDReader
from Objects import AFD
from Objects import GR

def afd_to_gr(afd_file):
    afd = AFDReader.read(afd_file)
    
    initial_simbol = afd.initial_state_name
    terminais = afd.alphabet
    
    productions = {}
    # Formata para GR, cada transição de cada estado do automato.
    for state in afd.transition_table.items():
        if state[0] in afd.final_states:
            terminais_state = [transition[0] for transition in state[1].transitions.items()]
            productions[state[0]] = terminais_state + [transition[0] + transition[1] for transition in state[1].transitions.items()]

            # Cria uma nova cabeça de produção quando estado inicial é de aceitação
            if state[0] == afd.initial_state_name:
                initial_simbol = state[0] + '@'
                productions[state[0]+'@'] = [["&"],productions[state[0]]]

        else:
            productions[state[0]] = [transition[0] + transition[1] for transition in state[1].transitions.items()]
    
    grammar = GR.Grammar(initial_simbol, terminais, productions)

    return grammar

if __name__ == '__main__':
    print(afd_to_gr("AFND/afd.afd"))