import Readers.GRReader as GRReader
from Objects.GR import Grammar



class FirstCalculator:
    def __init__(self,gr:Grammar):
        self.first: dict[str,set] = {}
        for NT in gr.productions.keys():
           self.first[NT] = set()
        
    def calc(self,NT:str,gr:Grammar):
        for setence in gr.productions[NT]:
                if setence[0] in gr.terminais or setence[0] == '&':
                    self.first[NT].update([setence[0]])
                else:
                    if setence[0] != NT:
                        self.calc(setence[0],gr)
                        if len(setence) > 1 and setence[1] in gr.productions.keys():
                            self.calc(setence[1],gr)
                    self.first[NT].update(self.first[setence[0]].difference('&')) 

class FollowCalculator:
    def __init__(self,gr:Grammar):
        self.follow: 'dict[str,set]' = {}
        for NT in gr.productions.keys():
           self.follow[NT] = set()
        self.follow[gr.initial_symbol] = {'$'}


    def follow_of_setence(self,cabeca,setence: str,gr:Grammar,firstTable: 'dict[str,set]'):
        if setence[-1] in gr.productions.keys():
            self.follow[setence[-1]].update(self.follow[cabeca])
            if setence[-1] in gr.nullableNT and len(setence )>1:
                self.follow_of_setence(cabeca,setence[:-1],gr,firstTable)

        if len(setence )< 2:
            return
        if setence[0] in gr.productions.keys():
            if setence[1] in gr.terminais:
                self.follow[setence[0]].update([setence[1]])
            else:
                self.follow[setence[0]].update(firstTable[setence[1]].difference('&'))
                if setence[1] in gr.nullableNT and len(setence) > 2:
                    new_setence = [setence[0]]
                    new_setence.extend(setence[2:])
                    self.follow_of_setence(cabeca,new_setence,gr,firstTable) 
        
        self.follow_of_setence(cabeca,setence[1:],gr,firstTable)

    def Follow(self,gr:Grammar,firstTable: 'dict[str,set]'):
        for key,production in gr.productions.items():
            for prod in production:
                self.follow_of_setence(key,prod,gr,firstTable)

        for key,production in gr.productions.items():
            for prod in production:
                if prod[-1] in gr.productions.keys():
                    self.follow[prod[-1]].update(self.follow[key])
                    if prod[-1] in gr.nullableNT and len(prod)>1:
                        self.follow_of_setence(key,prod[:-1],gr,firstTable)

if __name__ == '__main__':
   gr =  GRReader.read('GR/prova3.gr')
   print(gr)
   gr.treat_left_epsilon_productions()
   print(gr)
   calculator = FirstCalculator(gr)
   calculator.calc('S',gr)
   print('First:')
   print(calculator.first)
   print('-'*35)
   FoCalc = FollowCalculator(gr)
   print('Follow')
   FoCalc.Follow(gr,calculator.first)

    

   print(FoCalc.follow)