from os import path 
class Grammar:


    def __init__(self,initial_symbol: str, n_terminais: str, productions : 'dict[str:list]'):
        self.initial_symbol = initial_symbol
        self.terminais = n_terminais
        self.productions : dict[str,list[list[str]]] = productions 
        self.enumerated_producitons = self.__enum_prods()
        self.nullableNT = set()

    def __enum_prods(self):
        cnt = 0
        enumerated = {}
        for N, productions in self.productions.items() :
            for production in productions:
                enumerated[cnt] = (production, N)
                cnt += 1
        return enumerated

    def treat_left_epsilon_productions(self):
        for key,production in self.productions.items():
            if ['&'] in production:
                self.nullableNT.update(key)
        last = 0
        while last != len(self.nullableNT):
            last = len(self.nullableNT)
            for key,productions in self.productions.items():
                for production in productions:
                    nullable = True
                    for lex in production:
                        if lex not in self.nullableNT:
                            nullable = False 
                            break 
                    if nullable:
                        self.nullableNT.update(key)

        
        for key,production in self.productions.items():
            for prod in production:
                if prod[0] in self.nullableNT:
            
                    if len(prod) == 1:
                        self.productions[key].append(['&'])
                    else:
                        self.productions[key].append(prod[1:])

    def __str__(self):
        Is = f"Simbolo Inicial {self.initial_symbol} \n"
        Terminais = str(self.terminais) + '\n'
        str_productions = ""
        for key,value in self.productions.items():
            str_productions += f"{key} -> {value} \n"

        return Is + Terminais + str_productions[:-2]

    def print_enums(self):
        print("Producoes enumeradas")
        for enum, (prod, N) in self.enumerated_producitons.items():
            print(f"{enum} = {N} -> {''.join(prod)}")
    
    def generate_read_file(self, name):
        str_terminais = ''
        for simbolo in self.terminais:
            str_terminais += str(simbolo) + ','
        str_terminais = str_terminais[:-1] + "\n"

        str_productions = ''
        for key, value_list in self.productions.items():
            str_productions += f"{key} -> "
            for production in value_list:
                for value in production:
                    str_productions += value
                str_productions += ' | '
            
            str_productions = str_productions[:-3] +'\n'

        file = open(path.join("Gerados","Gramaticas",name), "w")
        file.write(str_terminais)
        file.write(str_productions)
        file.close()
