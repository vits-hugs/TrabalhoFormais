import Readers.GRReader as GRReader
from Objects.GR import Grammar
from tabela import LLTable
import copy


class StackEmulator:
    def __init__(self, gr:Grammar) -> None:
        self.__gr = gr
    
    # Entrada deve ser uma lista de tokens
    def emulate(self, entry:list[str]):
        # Resgatar tabela de parsing
        gr = self.__gr
        gr.print_enums()
        table = LLTable(gr)
        print(table)
        table = table.table
        enum_prods = gr.enumerated_producitons

        # Iniciar stack
        if entry[-1] != '$':
            entry.append('$')
        stack = ['$', gr.initial_symbol]
        crt_entry_pos = 0
        while True:
            print(f"Pilha = {''.join(stack)}")
            print(f"Entrada = {''.join(entry[crt_entry_pos:])}")
            crt_token = entry[crt_entry_pos]
            if crt_entry_pos > len(entry) - 1:
                print("ERROR")
                break
            
            # Aceitar caso stack e input forem vazios
            elif crt_token == '$' and stack[-1] == '$':
                print("Accepted!!")
                break
            
            # Caso stack == input, deletar da stack e avançar input
            elif crt_token == stack[-1]:
                stack.pop(-1)
                crt_entry_pos += 1
            
            # Caso stack for não terminal, empilhar produção
            elif stack[-1] in table:
                prod_enum = table[stack[-1]][crt_token]
                prod = copy.deepcopy(enum_prods[prod_enum][0])
                prod.reverse()
                stack.pop(-1)
                for i in prod:
                    if i == '&':
                        continue
                    stack.append(i)
            else:
                print("ERROR")
                break
            print("-"*15)

        

if __name__ == "__main__":
    gr =  GRReader.read('GR/prova3.gr')
    entry = "c v f com ; b e ; b e".split()
    emulator = StackEmulator(gr)
    emulator.emulate(entry)