class N_State:

    def __init__(self, name: str, transitions: 'dict[str, set]' = {}, token_type: str = None):
        self.name = name
        self.transitions = transitions
        self.token_type = token_type


    def __getitem__(self, key: str):
        return self.transitions.get(key, set())


class AFND:
    def __init__(self, initial_state_name: str, alphabet: 'set[str]', transition_table: 'dict[str, N_State]' = {}, final_states = {}):
        self.initial_state_name = initial_state_name
        self.alphabet = alphabet
        self.transition_table = transition_table
        self.final_states = final_states

    def print(self):
        # Número de estados
        print(len(self.transition_table))

        # Estado inicial
        print(self.initial_state_name)

        # Estados finais
        end_states = []
        for _, state in self.transition_table.items():
            if state.token_type != None:
                end_states.append(state.name)
        print(','.join(end_states))

        # alphabeto
        print(','.join(self.alphabet))

        # Transições
        all_transitions = []
        for key, state in self.transition_table.items():
            for char, dest_state in state.transitions.items():
                all_transitions.append((key, char, dest_state))
        for transition in all_transitions:
            print(transition[0], transition[1], sep=',', end=',')
            print('-'.join(transition[2]))