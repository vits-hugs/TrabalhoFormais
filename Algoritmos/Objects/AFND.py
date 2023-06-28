from os import path
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

    def computeInput(self, string):
        current_states = [self.initial_state_name]
        next_states = []

        for char in string:
            for state in current_states:
                if char in self.transition_table[state].transitions:
                    next_states = next_states + (list(self.transition_table[state].transitions[char]))
        
            current_states = next_states.copy()
            next_states = []

        return current_states

    def __str__(self):
        to_print = []

        to_print.append(f"Número de estados = {len(self.transition_table)}")

        # Estado inicial
        to_print.append(f"Estado inicial = {self.initial_state_name}")

        # Estados finais
        to_print.append(f"Estados finais = {self.final_states}")

        # alphabeto
        to_print.append("Alfabeto = " + ','.join(self.alphabet))

        # Transições
        all_transitions = []
        for key, state in self.transition_table.items():
            for char, dest_state in state.transitions.items():
                all_transitions.append((key, char, dest_state))
        for transition in all_transitions:
            to_print.append(f"{transition[0]} -- {transition[1]} --> {'-'.join(transition[2])}")

        return '\n'.join(to_print)
    
    def generate_read_file(self, name):
        states_number = str(len(self.transition_table)) + "\n"
        initial_state = self.initial_state_name + "\n"

        final_states = ''
        for state in self.final_states:
            final_states += str(state) + ','
        final_states = final_states[:-1] + "\n"

        alphabet = ','.join(self.alphabet) + "\n"

        all_transitions = ''
        for key, state in self.transition_table.items():
            for char, dest_state in state.transitions.items():
                all_transitions += str(key) + ',' + str(char) + ',' + str('-'.join(dest_state)) + "\n"
        
        file = open(path.join("Gerados","Automatos",name), "w")
        file.write(states_number)
        file.write(initial_state)
        file.write(final_states)
        file.write(alphabet)
        file.write(all_transitions)
        file.close()
