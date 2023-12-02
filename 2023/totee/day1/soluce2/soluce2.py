import re


dict_value={'one':'1', 'two':'2', 'three':'3', 'four':'4', 'five':'5', 'six':'6', 'seven':'7', 'eight':'8', 'nine':'9'}
# dict_value={'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9}
def loadFile(input):
    result = 0
    cpt = 1
    liste = []
    with open(input, 'r') as f:
        for line in f:
            str = re.findall("(one|two|three|four|five|six|seven|eight|nine|[0-9])", line)
            print(f"--{cpt} {line.strip()}")
            print(f"{str}")
            if len(str) == 1:
                if str[0].isdigit():
                    trebuchet = str[0] + str[0]
                    print(f"trebuchet 1: {trebuchet}")
                    result += int(trebuchet)
                    liste.append(int(trebuchet))
                    # print(f"result: {result}")
                else:
                    trebuchet = dict_value[str[0]] + dict_value[str[0]]
                    print(f"trebuchet 2: {trebuchet}")
                    result += int(trebuchet)
                    liste.append(int(trebuchet))
                    # print(f"result: {result}")
            else:
                if str[0].isdigit():
                    if str[-1].isdigit():
                        trebuchet = str[0] + str[-1]
                        print(f"trebuchet 3: {trebuchet}")
                        liste.append(int(trebuchet))
                    else:
                        trebuchet = str[0] + dict_value[str[-1]]
                        print(f"trebuchet 4: {trebuchet}")
                        liste.append(int(trebuchet))
                    result += int(trebuchet)
                    # print(f"result: {result}")
                else:
                    if str[-1].isdigit():
                        trebuchet = dict_value[str[0]] + str[-1]
                        print(f"trebuchet 5: {trebuchet}")
                        liste.append(int(trebuchet))
                    else:
                        trebuchet = dict_value[str[0]] + dict_value[str[-1]]
                        print(f"trebuchet 6: {trebuchet}")
                        liste.append(int(trebuchet))
                    result += int(trebuchet)
            print(f"result: {result} ")
            cpt += 1

        print(f"soluce2: {result} len:{len(liste)} sum: {sum(liste)}")

def main():
    # inputfile = "soluce2/test.txt"
    inputfile = "soluce2/input.txt"
    loadFile(inputfile)


# main
if __name__ == '__main__':
    main()