import logging
import string
import re

logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=logging.WARNING)

#file = "test.txt"
file = "input.txt"
grille = []


def isInstruction(ligne):
    return ligne[0] == "m"

def isLineCol(ligne):
    return ligne[1] == '1'
#print(f"toto : {isInstruction('move 1 from 2 to 1')}")

with open(file, "r") as f:
    colonne_max = 0
    for line in f:
        if line in "\n" or isLineCol(line):
            continue
        if isInstruction(line):
            instructions = [int(x) for x in re.findall("\d+", line)]
            print(f"instructions : {instructions}")
            move = instructions[0]
            fromCol = instructions[1] - 1
            toCol = instructions[2] - 1
            for i in range(0,move):
                grille[toCol].insert(0,grille[fromCol][0])
                grille[fromCol].pop(0)
            print(f" {line} {grille}")

        else:
        # logging.DEBUG(str(len(line))+"")

            for col,caisse in enumerate(line[1::4],1):
                colonne = col
                print(f"{caisse} | colonne: {colonne} colMax: {colonne_max}")
                if colonne > colonne_max:
                    colonne_max = colonne
                    for i in range(0,colonne_max):
                        if len(grille) < colonne_max :
                            grille.append(list(''))
                if caisse != " ":
                    grille[colonne-1].append(caisse)

                #    print(f"position: {line.find(caisse)}")
                #print(f"line: {line} longueur line: {len(line)} nb caisse: {len()}")
                print(f"{grille}")

    resulte = [item[0] for item in grille]
    print(f"{''.join(resulte)}")