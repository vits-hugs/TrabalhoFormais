import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from Readers import AFDReader
from Readers import AFNDReader
from Objects import AFD
from Objects import AFND

def afd_recognition(afd_file, string):
    afd = AFDReader.read(afd_file)

    print(afd.computeInput(string))
    # for state in afnd.transition_table:
    #     print(afnd.transition_table[state].transitions)

if __name__ == '__main__':
    from os import path 
    AFND_PATH = path.join("Testes","AFD","intersection.afd")
    SETENCE = "bb"
    afd_recognition(AFND_PATH, SETENCE)
