class D_State:
    def __init__(self, name: str, transitions: 'dict[str, str]' = {}, token_type: str = None):
        self.name = name
        self.transitions = transitions
        self.token_type = token_type

    def __getitem__(self, key):
        return self.transitions.get(key, None)

class AFD:
    def __init__(self, initial_state_name: str, alphabet: 'set[str]',
                 transition_table: 'dict[str, D_State]' = {}, final_states={}):

        self.initial_state_name = initial_state_name
        self.alphabet = alphabet
        self.transition_table = transition_table
        self.final_states = final_states

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
            #if char not in self.alphabet and char not in config.WHITESPACES:
                # raise CharNotInalphabet(char)
            current_state_name = self.transition_table[current_state_name][char]
            reading_index += 1

        if foward == begin: foward += 1
        return token, foward

    def __str__(self):
        # Número de estados
        to_print = []
        to_print.append(f"Número de estados = {len(self.transition_table)}")

        # Estado inicial
        to_print.append(f"Estado inicial = {self.initial_state_name}")

        # Estados finais
        # end_states = []
        # for _, state in self.transition_table.items():
        #     if state.token_type != None:
        #         end_states.append(state.name)
        # print(','.join(end_states))
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