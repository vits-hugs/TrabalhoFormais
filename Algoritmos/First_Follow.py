import Readers.GRReader as GRReader
from Objects.GR import Grammar
import copy



class FirstCalculator:
    def __init__(self,gr:Grammar):
        #inicia dicionario com todos os NT
        self.first: dict[str,set] = {}
        for NT in gr.productions.keys():
           self.first[NT] = set()
    
    #Calcula First indo para outros NT alcançaveis
    def calc(self,NT:str,gr:Grammar):
        gr = copy.deepcopy(gr)
        gr.treat_left_epsilon_productions()
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
    #inicia dicionario com todos os NT
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
        gr = copy.deepcopy(gr)
        gr.treat_left_epsilon_productions()
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
   from os import path 
   GRAMMAR_PATH = path.join("Testes","GR","prova3.gr")
   gr =  GRReader.read(GRAMMAR_PATH)

   gr.treat_left_epsilon_productions() #Trata todas as epsilon produções


   First_calculator = FirstCalculator(gr)
   First_calculator.calc(gr.initial_symbol,gr)
   print('First:')
   for key,value in First_calculator.first.items():
       print(f"First({key}) : {value}")
   print('-'*35)
   Follow_calculator = FollowCalculator(gr)

   print('Follow')
   Follow_calculator.Follow(gr,First_calculator.first)
   for key,value in Follow_calculator.follow.items():
        print(f"Follow({key}) : {value}")