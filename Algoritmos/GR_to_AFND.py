import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Readers import GRReader
from Objects import AFND
from Objects import GR

def gr_to_afnd(afd_file):
    grammar = GRReader.read(afd_file)

    alphabet = grammar.terminais
    initial_state = grammar.initial_symbol
    new_final_state = '__final_state_'
    final_states = {new_final_state}

    if ['&'] in grammar.productions[grammar.initial_symbol]:
        final_states.add(grammar.initial_symbol)

    transition_table = {}
    
    states = [production[0] for production in grammar.productions.items()]
    for state in states:
        transition_state = {}

        for production in grammar.productions[state]:
            if production[0] not in transition_state:
                transition_state[production[0]] = set()

            if len(production) > 1:     
                transition_state[production[0]].add(production[1])
            else:
                transition_state[production[0]].add(new_final_state)

        transition_table[state] = AFND.N_State(state, transition_state)
    
    transition_table[new_final_state] = AFND.N_State(new_final_state, {})
    
    afnd = AFND.AFND(initial_state, alphabet, transition_table, final_states)

    return afnd

if __name__ == '__main__':
    from os import path 
    GRAMMAR_PATH = path.join("Testes","GR","regular.gr")
    AFND_FILENAME = "AFND_de_GR" 
    
    AFND = gr_to_afnd(GRAMMAR_PATH)
    print(AFND)
    AFND.generate_read_file(AFND_FILENAME)