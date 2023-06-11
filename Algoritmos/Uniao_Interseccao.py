from Objects.AFD import *
from Objects.AFND import *
from AFND_to_AFD import afnd_to_afd
import Readers.AFDReader as AFDReader
import copy

def union(afd1:AFD, afd2:AFD) -> AFD:
    afd1 = add_sufix(afd1, "1-")
    afd2 = add_sufix(afd2, "2-")
    new_states = []
    for state in afd1.transition_table.values():
        new_states.append(N_State(state.name, state.transitions))
    for state in afd2.transition_table.values():
        new_states.append(N_State(state.name, state.transitions))
    
    new_states.append(N_State('*', {'&':{afd2.initial_state_name, afd1.initial_state_name}}))

    new_transition_table = {}
    for s in new_states:
        new_transition_table[s.name] = s

    new_finals = afd1.final_states.union(afd2.final_states)

    afnd = AFND('*', afd1.alphabet.union(afd2.alphabet), new_transition_table, new_finals)
    return afnd_to_afd(afnd)

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
    union_afd = union(afd1, afd2)
    afd1 = add_sufix(afd1, "1-")
    afd2 = add_sufix(afd2, "2-")
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
    q0 = D_State("q0", {"a":"q1"})
    q1 = D_State("q1", {"a":"q1"})
    afd1 = AFD("q0", {"a"}, {"q0":q0, "q1":q1}, {"q1"})
    q02 = D_State("q0", {"b":"q1"})
    q12 = D_State("q1", {"b":"q1"})
    afd2 = AFD("q0", {"b"}, {"q0":q02, "q1":q12}, {"q1"})
    union_afd = intersection(afd1, afd2)
    print(union_afd)