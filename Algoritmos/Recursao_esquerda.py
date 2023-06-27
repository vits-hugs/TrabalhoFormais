from Objects.GR import Grammar
from Readers.GRReader import read


# Remove a recursão a esquerda de uma produção
def direct_recursion(grammar_head: str, grammar_production: list):
    new_production = {grammar_head: grammar_production}

    # Marca em um dicionario todas as produções com recursão a esquerda
    production_positions = []
    for position, production in enumerate(grammar_production):
        if production[0] == grammar_head:
            production_positions.append(position)

    if len(production_positions) == 0:
        return new_production

    # Cria as novas produções sem recursão a esquerda
    new_production_destination = [['&']]
    new_head = grammar_head + '@'
    for position in production_positions:
        grammar_production[position].pop(0)
        new_production_destination.append(grammar_production[position] + [new_head])

    # Remove as recursões a esquerda
    for index in sorted(production_positions, reverse=True):
        del grammar_production[index]

    # Adiciona as recursões a direita
    for production in grammar_production:
        production.append(new_head)

    # Cria as regras das novas produções
    new_production[new_head] = new_production_destination

    return new_production

# Algoritmo que remove a recursão a esquerda em gramáticas não circulares
def indirect_recursion(grammar: Grammar):
    grammar = remove_useless_productions(grammar)
    productions_head = list(grammar.productions.keys())
    new_production = {}

    for i in range(0, len(productions_head)):
        j = 0
        for j in range(j, i):
            # Lista a posição dos aparecimentos da recursão a esquerda para a cabeça i apontada
            production_position_i = is_first_prodution(productions_head[j], grammar.productions[productions_head[i]])

            # Para cada produção de j ele retira a produção e coloca como parte da produção de i
            for position_i in production_position_i:
                if len(grammar.productions[productions_head[i]][position_i]) >= 2:
                    alfa = grammar.productions[productions_head[i]].pop(position_i)

                    for position_j in range(0, len(grammar.productions[productions_head[j]])):
                        grammar.productions[productions_head[i]].append(grammar.productions[productions_head[j]][position_j] + alfa[1:])

        # Adiciona a nova produção a um dicionário que substituira as produções da gramática
        temporary_production = direct_recursion(productions_head[i], grammar.productions[productions_head[i]])
        grammar.productions[productions_head[i]] = temporary_production[productions_head[i]]
        new_production = new_production | temporary_production
    
    grammar.productions = new_production
    return grammar

# Remove produções do tipo A -> A
def remove_useless_productions(grammar: Grammar):
    new_production = {}
    for key, production_list in grammar.productions.items():
        new_production[key] = []
        for production in production_list:
            if len(production) > 1 or production[0] != key:
                new_production[key].append(production)

    grammar.productions = new_production
    return grammar

# Função que verifica se o simbolo aparece como primeiro de alguma produção
# Retorna uma lista com as posições que aparece
def is_first_prodution(first, production_list):
    position_list = []
    for position, production in enumerate(production_list):
        if production[0] == first:
            position_list.append(position)
    
    return position_list
            
if __name__ == '__main__':
    gr = read("GR/gramatica_teste.gr")
    print(indirect_recursion(gr))    
