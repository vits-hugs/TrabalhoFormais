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
                    self.first[NT].update(setence[0])
                else:
                    other = self.calc(setence[0],gr)
                     

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
                self.follow[setence[0]].update(setence[1])
            else:
                self.follow[setence[0]].update(firstTable[setence[1]].difference('&'))
                if setence[1] in gr.nullableNT and len(setence) > 2:
                    new_setence = setence[0] + setence[2:]
                    self.follow_of_setence(cabeca,new_setence,gr,firstTable) 
        
    

    def Follow(self,gr:Grammar,firstTable: 'dict[str,set]'):
        for key,production in gr.productions.items():
            for prod in production:
                self.follow_of_setence(key,prod,gr,firstTable)



if __name__ == '__main__':
   gr =  GRReader.read('GR/Follow.gr')
   print(gr)
   gr.add_productions()
   print(gr)
   calculator = FirstCalculator(gr)
   calculator.calc('S',gr)
   print(calculator.first)
   FoCalc = FollowCalculator(gr)
   FoCalc.Follow(gr,calculator.first)
   print(FoCalc.follow)