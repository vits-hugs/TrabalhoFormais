from Objects.GR import Grammar
import Readers.GRReader as GRReader
from First_Follow import FirstCalculator
from First_Follow import FollowCalculator

class LLTable:
    def __init__(self, gr) -> None:
        self.table = self.__create_table(gr)

    def __create_table(self, gr:Grammar):
        fc = FirstCalculator(gr)
        fc.calc(gr.initial_symbol, gr)
        firsts = fc.first

        foCalc = FollowCalculator(gr)
        foCalc.Follow(gr, firsts)
        follows = foCalc.follow

        firsts_enum = self.__get_enum_first(gr)

        
        table = {}
        for prod_num, firsts in firsts_enum.items():
            N = gr.enumerated_producitons[prod_num][1]
            crt_entries = table.get(N, {})
            has_epsilon = False
            for first in firsts:
                if first == '&':
                    has_epsilon = True
                    continue
                crt_entries[first] = prod_num
            
            if has_epsilon:
                for f in follows[N]:
                    crt_entries[f] = prod_num

            table[N] = crt_entries
        return table

    def __get_enum_first(self, gr:Grammar):
        fc = FirstCalculator(gr)
        fc.calc('S', gr)
        firsts = fc.first
        for i in gr.terminais:
            firsts[i] = set([i])
        firsts['&'] = set(['&'])
        
        firsts_enum = {}
        for enum, (production, N) in gr.enumerated_producitons.items():
            crt_firsts = set()
            for i in range(len(production)):
                firsts_i = firsts[production[i]]
                crt_firsts.update(firsts_i)
                if not '&' in firsts_i:
                    break
            firsts_enum[enum] = crt_firsts
        
        return firsts_enum

    def __str__(self):
        to_print = ["Tabela de parsing"]
        for N, vals in self.table.items():
            vals_str = []
            for final, prod in vals.items():
                vals_str.append(f"{final} = {prod}")
            to_print.append(f"{N} - > {'|'.join(vals_str)}")
        
        return '\n'.join(to_print)



if __name__ == "__main__":

   gr =  GRReader.read('GR/prova3.gr')

    

   print(LLTable(gr))