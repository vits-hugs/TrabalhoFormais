import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Objects.GR import Grammar

def read(s):
    text = open(s)

    # initial_simbol
    # n_terminais
    # productions 

    productions = {}
    
    x = text.readline().rstrip().replace(' ','').split('->')
    inital_simbol = x[0]
    terminais = set()
    while True:
        if x == ['']:
            break
        result_production = x[1].split('|')

        productions[x[0]] = result_production

        for i in result_production:
            [terminais.add(x) for x in i]


        x = text.readline().rstrip().replace(' ','').split('->')



    text.close()

    terminais.difference_update(productions.keys())
    terminais.difference_update('&')
    return Grammar(inital_simbol,terminais,productions)


if __name__ == '__main__':
    print(read("GR/gram.gr"))