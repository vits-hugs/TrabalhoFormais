import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Readers.Er_reader import ER_parser

class T_Node:
    def __init__(self,type,left=None,right=None) -> None:
        self.type = type
        self.left = left
        self.right = right

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

def create_tree(s: str):
    return T_Node('.',__create_tree(s),'#')

def __create_tree(s: str):
    if len(s) == 1: # if verify last
        return  T_Node(s)
    if s[-1] == ')':
        index = get_parent_index(s)

        simbolo = s[index -1 ]
        esquerda = s[:index -1]
        direita = s[1+index: -1]

        if index == 0:
            return __create_tree(direita)
        
        return T_Node(simbolo,__create_tree(esquerda),__create_tree(direita))

    if s[-1] in ('*','+','?'):
        return T_Node('*',__create_tree(s[:-1]))

    simbolo = s[-2]
    esquerda = s[0:-2]
    direita = s[-1]
    return  T_Node(simbolo,__create_tree(esquerda),T_Node(direita))
    

if __name__ == "__main__":
    d = ER_parser()
    d.parseEr_fromFile("ER/er_example.txt")
    print(d.definitions)

    g = create_tree(d.definitions['teste3'])
    print(g)
