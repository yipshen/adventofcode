import re



def loadFile(input):
    result = 0
    with open(input, 'r') as f:
        for line in f:
            str = re.sub("[^0-9]", "", line)
            if len(str) == 1:
                trebuchet = str + str
                print(f"trebucher: {trebuchet}")
                result += int(trebuchet)
            else:
                trebuchet = str[0]+str[-1]
                print(f"trebucher: {trebuchet}")
                result += int(trebuchet)
    print(f"result: {result}")



def main():
    # inputfile = "test.txt"
    inputfile = "input.txt"
    loadFile(inputfile)






# main
if __name__ == '__main__':
    main()