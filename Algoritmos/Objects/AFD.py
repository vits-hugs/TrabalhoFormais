class D_State:
    def __init__(self, name: str, transitions: 'dict[str, str]' = {}, token_type: str = None):
        self.name = name
        self.transitions = transitions
        self.token_type = token_type

    def __getitem__(self, key):
        return self.transitions.get(key, None)
    
    def __setitem__(self,key,value):
        self.transitions[key] = value

class AFD:
    def __init__(self, initial_state_name: str, alphabet: 'set[str]',
                 transition_table: 'dict[str, D_State]' = {}, final_states={}):

        self.initial_state_name = initial_state_name
        self.alphabet = alphabet
        self.transition_table = transition_table
        self.final_states = final_states

    def remove_state(self, name:str):
        if name in self.final_states:
            self.final_states.remove(name)

        self.transition_table.pop(name)
        for state in self.transition_table.values():
            to_remove = []
            for c, s in state.transitions.items():
                if s == name:
                    to_remove.append(c)
            for i in to_remove:
                state.transitions.pop(i)

    def getToken(self, string, begin: int):
        reading_index = begin
        foward = begin
        token = None
        current_state_name = self.initial_state_name
        while current_state_name:

            current_state = self.transition_table[current_state_name]
            if current_state.token_type != None:
                foward = reading_index
                token = current_state.token_type

            if reading_index >= len(string):
                foward = reading_index + 1
                break

            char = string[reading_index]
            current_state_name = self.transition_table[current_state_name][char]
            reading_index += 1

        if foward == begin: foward += 1
        return token, foward
    
    def computeInput(self, string):
        current_state = self.initial_state_name
        for char in string:
            if char not in self.transition_table[current_state].transitions:
                return (False, 'Morto')
            
            current_state = self.transition_table[current_state].transitions[char]
        
        recognition = (current_state in self.final_states)
        return (recognition, current_state)

    def __str__(self):
        # Número de estados
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
            to_print.append(str((transition[0], transition[1], transition[2])))

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
                all_transitions += str(key) + ',' + str(char) + ',' + str(dest_state) + "\n"
        
        file = open(f"AFND/{name}", "w")
        file.write(states_number)
        file.write(initial_state)
        file.write(final_states)
        file.write(alphabet)
        file.write(all_transitions)
        file.close()
