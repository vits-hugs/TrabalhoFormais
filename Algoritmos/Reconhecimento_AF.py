""""
Algoritmo de reconhecimento AFD (af_recognition)
Entrada: (AF, cadeia_de_entrada)
Saida: (is_aceitação, lista_estados_alcançados)
"""
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Readers import AFDReader
from Readers import AFNDReader
from Objects import AFD
from Objects import AFND

def af_recognition(af, string):
    print(af.computeInput(string))

if __name__ == '__main__':
    from os import path 
    SETENCE = "a"

    # Leitura de AFD retirar comentario
    # AF_PATH = path.join("Testes","AFD","reconhecimento_afd.afd")
    # af = AFDReader.read(AF_PATH)

    # Leitura de AFND retirar comentario
    AF_PATH = path.join("Testes","AFD","reconhecimento_afnd.afnd")
    af = AFNDReader.read(AF_PATH)

    af_recognition(af, SETENCE)
