
class Grammar:

    def __init__(self,initial_symbol: str, n_terminais: str, productions : 'dict[str:list]'):
        self.initial_symbol = initial_symbol
        self.n_terminais = n_terminais
        self.productions = productions

    
    def __str__(self):
        Is = f"Simbolo Inicial {self.initial_symbol} \n"
        Terminais = str(self.n_terminais) + '\n'
        str_productions = ""
        for key,value in self.productions.items():
            str_productions += f"{key} -> {value} \n"

        return Is + Terminais + str_productions[:-2]
