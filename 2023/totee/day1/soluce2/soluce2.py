import re



replace_str = [('one','o1e'), ('two','t2e'), ('three','t3e'), ('four','f4r'), ('five','f5e'), ('six','s6x'), ('seven','s7n'), ('eight','e8t'), ('nine','n9e')]



def replaceStringByNumber(chaine) :
    result = chaine
    for a in replace_str:
        result = result.replace(a[0], a[1])
    return result

def loadFile(input):
    result = 0
    cpt = 1
    liste = []
    with open(input, 'r') as f:
        for line in f:
            str = replaceStringByNumber(line)
            print(f"{line} | {str}")
            # print(f"-{cpt}- {line.strip()}")
            str = re.findall("([0-9])", str)
            # print(f"{str}")
            if len(str) == 1:
                # un seul chiffre ou lettre
                    # si chiffre
                    trebuchet = str[0] + str[0]
                    print(f"trebuchet 1: {trebuchet}")
                    result += int(trebuchet)
                    liste.append(int(trebuchet))
                    # print(f"result: {result}")
            else:
                # en deux partie
                    trebuchet = str[0] + str[-1]
                    print(f"trebuchet 3: {trebuchet}")
                    liste.append(int(trebuchet))
            print(f"result: {result} ")
            cpt += 1

        print(f"soluce2: {result} len:{len(liste)} sum: {sum(liste)}")

def main():
    # inputfile = "soluce2/test.txt"
    inputfile = "soluce2/input.txt"
    # inputfile = "soluce2/input2.txt"
    loadFile(inputfile)


# main
if __name__ == '__main__':
    main()