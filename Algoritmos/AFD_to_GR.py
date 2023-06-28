""""
Algoritmo de conversão de AFD para GR (afd_to_gr)
Entrada: Objeto AFD
Saida: Objeto GR
"""

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Readers import AFDReader
from Objects import AFD
from Objects import GR

def afd_to_gr(afd: AFD):
    initial_simbol = afd.initial_state_name
    terminais = afd.alphabet
    productions = {}

    # Formata para GR, cada transição de cada estado do automato.
    for state in afd.transition_table.items():
        
        # Encontra as transições para estado final do automato
        final_state_transition = []
        for transition_state, state_destiny in state[1].transitions.items():
            if state_destiny in afd.final_states:
                final_state_transition.append(transition_state)

        # se tiver transições para o estado final incorpora na gramática
        if final_state_transition:
                productions[state[0]] = final_state_transition + [transition[0] + transition[1] for transition in state[1].transitions.items()]
        else:
            productions[state[0]] = [transition[0] + transition[1] for transition in state[1].transitions.items()]

        # Cria uma nova cabeça de produção quando estado inicial é de aceitação
        if state[0] == afd.initial_state_name and state[0] in afd.final_states:
            initial_simbol = state[0] + '@'
            productions[state[0]+'@'] = [["&"],productions[state[0]]]

    grammar = GR.Grammar(initial_simbol, terminais, productions)
    return grammar

if __name__ == '__main__':
    afd = AFDReader.read("AFND/afd_1.afd")
    print(afd_to_gr(afd))