from Objects.AFD import *
from Objects.AFND import *
from AFND_to_AFD import afnd_to_afd
import Readers.AFNDReader as AFNDReader
import copy

def get_min(afd:AFD) -> AFD:
    # Remover mortos
    remove_deads(afd)
    # Dividir estados em finais e não finais
    non_final = [state for name,state in afd.transition_table.items() if not name in afd.final_states]
    final = [state for name,state in afd.transition_table.items() if name in afd.final_states]
    crt_equivalents = [final, non_final]
    crt_equivalents_reverse = get_reversed_equivalents(crt_equivalents)

    changed = True
    while changed:
        changed = False
        # Criar novos grupos para cada (G, C, E), ou seja, Grupo(G) por C chega no estado E
        for c in afd.alphabet:
            new_equivalents = {}
            for index, equis in enumerate(crt_equivalents):
                for state in equis:
                    reach_state = state.transitions.get(c, None)
                    reach = crt_equivalents_reverse.get(reach_state, None)
                    new_equis = new_equivalents.get((index, c, reach), [])
                    new_equis.append(state)
                    new_equivalents[(index, c, reach)] = new_equis
            if len(new_equivalents) != len(crt_equivalents):
                # Caso mudanças não aconteçam, loop para
                changed = True

            new_equivalents = list(new_equivalents.values())
            crt_equivalents = new_equivalents
            crt_equivalents_reverse = get_reversed_equivalents(crt_equivalents)

    # Criando automato novo sem estados equivalentes
    initial = afd.initial_state_name
    crt_equivalents.pop(crt_equivalents_reverse[initial])
    new_states = [copy.deepcopy(afd.transition_table[initial])] + [copy.deepcopy(i[0]) for i in crt_equivalents]
    final_states = set([i.name for i in new_states if i.name in afd.final_states])
    transitions = {}
    for i in new_states:
        transitions[i.name] = i
    min_afd = AFD(initial, afd.alphabet, transitions, final_states)
    return min_afd

# Tabela de estados equivalentes invertida para acesso em tempo constante
def get_reversed_equivalents(crt_equivalents: list[list[D_State]]):
    reversed = {}
    for index, i in enumerate(crt_equivalents):
        for state in i:
            reversed[state.name] = index
    return reversed

def remove_deads(afd:AFD):
    # bfs
    done = {}
    to_test = list(afd.final_states)
    while len(to_test) != 0:
        crt = to_test[0]
        to_test.pop(0)
        if not crt in done:
            done[crt] = True
            for state in afd.transition_table.values():
                for c in afd.alphabet:
                    if crt in state.transitions.get(c, []):
                        to_test.append(state.name)

    to_remove = set(afd.transition_table.keys()) - set(done.keys())
    for i in to_remove:
        afd.remove_state(i)
if __name__ == "__main__":
    from os import path 
    AFND_PATH = path.join("Testes","AFD","min_afnd_test.afnd")
    AFD_MINIMIZADO_FILENAME = "AFD_minimizado"
    afnd = AFNDReader.read(AFND_PATH)
    afd = afnd_to_afd(afnd)
    print(afd)
    afd_minimizado = get_min(afd)
    print("-"*30)
    print(afd_minimizado)
    afd_minimizado.generate_read_file(AFD_MINIMIZADO_FILENAME)