from Objects.AFND import *
from Objects.AFD import *
import Readers.AFNDReader as AFNDReader

def afnd_to_afd(non_det_automata: AFND) -> AFD:
    # Cálcular estados*
    episilon_states = get_epsilon_states(non_det_automata)

    new_transition_table = {}
    initial = non_det_automata.initial_state_name

    initial_episilon = episilon_states[initial]
    episilon_reach = [i.name for i in initial_episilon]

    undiscovered = [set(episilon_reach)]

    new_initial_tuple = to_tuple(episilon_reach)
    done = {new_initial_tuple : True}
    # BFS modificado para estados * apartir do novo estado inicial
    while(len(undiscovered) > 0):
        crt = undiscovered[0]
        transitions = {}
        for c in non_det_automata.alphabet:
            reach = set()
            for s in crt:
                s_state = non_det_automata.transition_table[s]
                episilon_reach = s_state.transitions.get(c, set())
                episilon_reach_full = set()
                # Para cada estado alcançado por c, adicionar estado* ao estado que é atingido
                for i in episilon_reach:
                    names = set([s.name for s in episilon_states[i]])
                    episilon_reach_full.update(names)
                reach = reach.union(set(episilon_reach_full))

            # Tupla para hash (dicionário) 
            reach_name = to_tuple(reach)

            if not reach_name in done:
                done[reach_name] = True
                undiscovered.append(reach)

            # Criando strings para nomes dos estados criados
            transitions[c] = '/'.join(reach_name)

        crt_tuple = to_tuple(undiscovered[0])
        new_transition_table[crt_tuple] = transitions
        undiscovered.pop(0)

    # Criando tabela de nomes e determinando estados finais
    new_final = set()
    names_dict = {}
    for s, _ in new_transition_table.items():
        names_dict[s] = '/'.join(s)
        for original_state in s:
            if original_state in non_det_automata.final_states:
                new_final.add(names_dict[s])


    d_states = [D_State(names_dict[name], transitions) for name, transitions in new_transition_table.items()]
    d_states_dict = {}
    for d in d_states:
        d_states_dict[d.name] = d

    afd = AFD(names_dict[new_initial_tuple], non_det_automata.alphabet, d_states_dict, new_final) 
    if '' in afd.transition_table.keys():
        afd.remove_state('')
    return afd

# Tuplas ordenadas para hash table
def to_tuple(state_set:'set[str]'):
    state_list = list(state_set)
    state_list.sort()
    return tuple(state_list)

# Cálculo dos estados*
def get_epsilon_states(non_det_automata: AFND) -> 'list[N_State]':
    new_states = {}

    for _, state in non_det_automata.transition_table.items():
        episilon_state = [state]
        #  BFS
        done = {}
        to_check = list(state.transitions.get('&', []))
        while(len(to_check) > 0):
            i = non_det_automata.transition_table[to_check[0]]
            to_check.pop(0)
            if not i.name in done:
                done[i.name] = True
                episilon_state.append(i)
                to_check += list(i.transitions.get('&', set()))
            

        new_states[state.name] = set(episilon_state)

    return new_states



if __name__ == "__main__":
    from os import path
    PATH_TO_AFND = path.join("Testes","AFD","epsilon.afnd")
    AFD_FILENAME = "AFD_de_AFND"
    AFND = AFNDReader.read(PATH_TO_AFND)
    AFD = afnd_to_afd(AFND)
    print(AFD)
    AFD.generate_read_file(AFD_FILENAME)        
            

