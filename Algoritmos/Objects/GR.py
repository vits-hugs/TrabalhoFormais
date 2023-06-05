
class Grammar:

    def __init__(self,initial_symbol: str, n_terminais: str, productions : 'dict[str:list]'):
        self.initial_symbol = initial_symbol
        self.terminais = n_terminais
        self.productions = productions
        self.nullableNT = set()

    def add_productions(self):
        for key,value in self.productions.items():
            if '&' in value:
                self.nullableNT.update(key)
        
        for key,production in self.productions.items():
            for prod in production:
                if prod[0] in self.nullableNT:
            
                    if len(prod) == 1:
                        self.productions[key].append('&')
                    else:
                        self.productions[key].append(prod[1:])



    
    def __str__(self):
        Is = f"Simbolo Inicial {self.initial_symbol} \n"
        Terminais = str(self.terminais) + '\n'
        str_productions = ""
        for key,value in self.productions.items():
            str_productions += f"{key} -> {value} \n"

        return Is + Terminais + str_productions[:-2]
