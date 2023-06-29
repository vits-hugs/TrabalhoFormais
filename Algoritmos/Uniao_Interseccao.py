from Objects.AFD import *
from Objects.AFND import *
from AFND_to_AFD import afnd_to_afd
import Readers.AFDReader as AFDReader
import copy

def union(afd1:AFD, afd2:AFD) -> AFD:
    afd1 = add_sufix(afd1, "1-")
    afd2 = add_sufix(afd2, "2-")

    # Transformação de AFD para AFND
    new_states = []
    for state in afd1.transition_table.values():
        new_states.append(N_State(state.name, state.transitions))
    for state in afd2.transition_table.values():
        new_states.append(N_State(state.name, state.transitions))
    
    # Adicionar estado novo e transição por epsilon para estados iniciais
    new_states.append(N_State('*', {'&':{afd2.initial_state_name, afd1.initial_state_name}}))

    new_transition_table = {}
    for s in new_states:
        new_transition_table[s.name] = s

    # Estados finais novos, união dos estados finais antigos
    new_finals = afd1.final_states.union(afd2.final_states)

    afnd = AFND('*', afd1.alphabet.union(afd2.alphabet), new_transition_table, new_finals)

    # Converção para afd
    return afnd_to_afd(afnd)

# Adiciona determinado sufixo a todos os estados do autômato
def add_sufix(afd:AFD, sufix):
    copy_afd = copy.deepcopy(afd)
    new_transitions = {}
    for name, state in copy_afd.transition_table.items():
        state.name = sufix + state.name
        new_transitions[state.name] = state
        for c, reach in state.transitions.items():
            state.transitions[c] = set([sufix + reach])
    copy_afd.transition_table = new_transitions

    copy_afd.initial_state_name = sufix + copy_afd.initial_state_name
    copy_afd.final_states = set([sufix + i for i in copy_afd.final_states])
    return copy_afd

def intersection(afd1:AFD, afd2:AFD) -> AFD:
    # Faz a união entre os autômatos
    union_afd = union(afd1, afd2)
    afd1 = add_sufix(afd1, "1-")
    afd2 = add_sufix(afd2, "2-")

    # Contrução dos novos estados finais, estados finais de ambos afd1 e afd2
    finals = set()
    for name in union_afd.transition_table.keys():
        has_1, has_2 = False, False
        for final in afd1.final_states:
            if (final + '/') in name or ('/' + final) in name:
                has_1 = True
        for final in afd2.final_states:
            if (final + '/') in name or ('/' + final) in name:
                has_2 = True
        if has_2 and has_1:
            finals.add(name)
    union_afd.final_states = finals
    return union_afd

if __name__ == "__main__":
    afd1 = AFDReader.read("AFND/inicia_com_a.afd")
    afd2 = AFDReader.read("AFND/termina_com_b.afd")
    intersection_afd = intersection(afd1, afd2)
    intersection_afd.generate_read_file("intersection.afd")
    print(intersection_afd)