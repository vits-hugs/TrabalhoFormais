from Objects.AFND import *
from Objects.AFD import *
import Readers.AFNDReader as AFNDReader

def afnd_to_afd(non_det_automata: AFND):

    episilon_states = get_epsilon_states(non_det_automata)

    new_transition_table = {}
    initial = non_det_automata.initial_state_name

    initial_episilon = episilon_states[initial]
    episilon_reach = [i.name for i in initial_episilon]

    undiscovered = [set(episilon_reach)]

    new_initial_tuple = to_tuple(episilon_reach)
    done = {new_initial_tuple : True}

    while(len(undiscovered) > 0):
        crt = undiscovered[0]
        transitions = {}
        for c in non_det_automata.alphabet:
            reach = set()
            for s in crt:
                for s_episilon in episilon_states.get(s, set()):
                    episilon_reach = s_episilon.transitions.get(c, set())
                    reach = reach.union(set(episilon_reach))

            reach_name = to_tuple(reach)

            if not reach_name in done:
                done[reach_name] = True
                undiscovered.append(reach)
            
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
    print(afd)

            
def to_tuple(state_set:'set[str]'):
    state_list = list(state_set)
    state_list.sort()
    return tuple(state_list)


def get_epsilon_states(non_det_automata: AFND) -> 'list[N_State]':
    new_states = {}

    for _, state in non_det_automata.transition_table.items():
        episilon_state = [state]
        if not '&' in state.transitions:
            continue

        #  BFS
        done = {}
        to_check = list(state.transitions['&'])
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
    q0 = N_State("q0", {"a":{"q1"},
                        "b":{"q0", "q1"},
                        "&":{"q1"}})
    q1 = N_State("q1", {"&":{"q2"}})
    q2 = N_State("q2", {"a":{"q1"},
                        "b":{"q0"},
                        "&":{"q2"}})
    afnd = AFND("q0", {'a', 'b'}, {"q0":q0, "q1":q1, "q2":q2}, {"q1"})
    res = afnd_to_afd(afnd)
    print(afnd)

    test = AFNDReader.read("AFND/epsilon.afnd")
    test.print()

    afnd_to_afd(test)
        
            

