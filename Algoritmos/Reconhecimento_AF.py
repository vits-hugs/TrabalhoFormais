""""
Algoritmo de reconhecimento AFD (afd_recognition)
Entrada: Gramatica
Saida: Gramatica (Sem recursão a esquerda)
"""
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Readers import AFDReader
from Readers import AFNDReader
from Objects import AFD
from Objects import AFND

def afd_recognition(afd, string):
    print(afd.computeInput(string))

if __name__ == '__main__':
    afd = AFNDReader.read("AFND/teste_afnd.afnd")
    afd_recognition(afd, "abab")
