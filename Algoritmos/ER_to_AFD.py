import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Readers.Er_reader import ER_parser
from Objects.AFD import AFD,D_State
global id 
id = 1


class T_Node:
    def __init__(self,type,left=None,right=None) -> None:
        self.type = type
        self.left = left
        self.right = right
        self.id = -1

    def __str__(self):
        if self.left == None and self.right == None:
            return self.type

        return '[' + self.type +':' 'L:' +str(self.left) + 'H R:' + str(self.right)   +']'
    
def get_parent_index(s: str ):
    cont = -1 
    for i in range(len(s)-1,-1,-1):
        if s[i] == ')':
            cont += 1
        if s[i] == '(':
            if cont == 0:
                return i 
            else:
                cont -=1 


class Er_toTree():
    def __init__(self) -> None:
        self.letra_num = {}

    def create_tree(self, s: str):
        last_node = T_Node('#')
        last_node.id = -2
        return T_Node('.',self.__create_tree(s),last_node)

    def __create_tree(self,s: str):
        if len(s) == 1: # if verify last
            folha = T_Node(s)
            global id
            folha.id = id 
            self.letra_num[str(id)] = folha.type 
            id +=1
            return  folha 
        if s[-1] == ')':
            index = get_parent_index(s)

            simbolo = s[index -1 ]
            esquerda = s[:index -1]
            direita = s[1+index: -1]

            if index == 0:
                return self.__create_tree(direita)
            
            return T_Node(simbolo,self.__create_tree(esquerda),self.__create_tree(direita))

        if s[-1] in ('*','+','?'):
            return T_Node(s[-1],self.__create_tree(s[:-1]))

        simbolo = s[-2]
        esquerda = s[0:-2]
        direita = s[-1]
        return  T_Node(simbolo,self.__create_tree(esquerda),self.__create_tree(direita))




def nullable(node : T_Node):
    if node.left== None and node.right == None:
        return False
    if node.type == '|':
        return nullable(node.left) or nullable(node.right)
    if node.type == '.':
        return nullable(node.left) and nullable(node.right)
    if node.type == '*':
        return True
    if node.type == '+':
        return False
    if node.type == '?':
        return True 
    
def firstpos(node : T_Node) -> set: 
    if node.left== None and node.right == None:
        return set([node.id])
    
    if node.type == '|':
        return firstpos(node.left).union(firstpos(node.right))
    
    if node.type == '.':
        if (nullable(node.left)):
            return firstpos(node.left).union(firstpos(node.right))
        else:
            return firstpos(node.left)
        
    if node.type == '*':
        return firstpos(node.left)

    if node.type == '+':
        return firstpos(node.left)
    
    if node.type == '?':
        return firstpos(node.left)
    
def lastpos(node : T_Node) -> set:
    if node.left== None and node.right == None:
        return set([node.id])
    
    if node.type == '|':
        return lastpos(node.left).union(lastpos(node.right))
    
    if node.type == '.':
        if (nullable(node.right)):
            return lastpos(node.left).union(lastpos(node.right))
        else:
            return lastpos(node.right)
    
    if node.type == '*':
        return lastpos(node.left)
    
    if node.type == '+':
        return lastpos(node.left)
    
    if node.type == '?':
        return lastpos(node.left)
    

class FollowPosTable:
    def __init__(self):
        self.followpos = {'-2':set()}

    def make_table(self,node):
        self.__followpos(node)
        if node.right:
            self.make_table(node.right)
        if node.left:
            self.make_table(node.left)

    def __followpos(self,node : T_Node) -> set:
        if node.type == '.':
            for pos in lastpos(node.left):
                if str(pos) in self.followpos:
                    self.followpos[str(pos)].update(firstpos(node.right))
                else:
                    self.followpos[str(pos)] = firstpos(node.right)

        if node.type == '*':
            for pos in lastpos(node):
                if str(pos) in self.followpos:
                    self.followpos[str(pos)].update(firstpos(node))
                else:
                    self.followpos[str(pos)] = firstpos(node)

        if node.type == '+':
            for pos in lastpos(node):
                if str(pos) in self.followpos:
                    self.followpos[str(pos)].update(firstpos(node))
                else:
                    self.followpos[str(pos)] = firstpos(node)


def nome(se:set()):
    d = list(se)
    d.sort()
    return '_'.join(map(str,d))
    

def make_automata(followTable, letra_num : dict , node: T_Node):
    D_states = [nome(firstpos(node))]
    N_Marcado = [firstpos(node)]

    Estado_inicial = nome(firstpos(node))
    alfabeto = set(letra_num.values()).difference('#')
    Transicoes = {}

    while len(N_Marcado)> 0:
        S = N_Marcado.pop()    
        for letra in alfabeto:
            U = set()
            for p in S:
                if letra_num[str(p)] == letra:
                    U.update(followTable[str(p)])
                if nome(U) not in D_states:
                    D_states.append(nome(U))
                    N_Marcado.append(U)
            if len(U) > 0:
                if nome(S) in Transicoes:
                    Transicoes[nome(S)][letra] = nome(U)
                else:
                    Transicoes[nome(S)] = D_State(nome(S),{letra:nome(U)})
    
    Estado_final = set([i for i in D_states if '-' in i])
    
    return AFD(Estado_inicial,alfabeto,Transicoes,Estado_final)

def ER_to_AFD(er) -> AFD:
    er_to_tree = Er_toTree()
    tree = er_to_tree.create_tree(er)

    FPT = FollowPosTable()
    FPT.make_table(tree)
 
    er_to_tree.letra_num['-2'] = '#'
    
    AFD = make_automata(FPT.followpos,er_to_tree.letra_num,tree)
    return AFD
if __name__ == "__main__":
    from os import path 
    ER_PATH = path.join("Testes","ER","teste.txt")
    ER_CHOICE = '1'
    AFD_FILENAME = "AFD_de_ER"

    parser = ER_parser()
    parser.parseEr_fromFile(ER_PATH)
    
    ER = parser.definitions[ER_CHOICE]
    AFD = ER_to_AFD(ER)
    print(AFD)
    AFD.generate_read_file(AFD_FILENAME)