import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def loadProgram(fileInput: str) -> list:
    codeProgram = []
    with open(fileInput, "r") as f:
        for line in f:
            codeProgram.append(line.strip())
            #logger.debug(f"code: {line.strip()}")
    return codeProgram


def spritePosition(position:int) -> list:
    result = ['.' for x in range(0,40)]
    if position < 0:
        result[0] = "#"
    elif position == 0 :
        result[0] = "#"
        result[1] = "#"
    elif position == 39 :
        result[39] = "#"
        result[38] = "#"
    elif position >= 40 :
        result [39] = "#"
    else:
        result[position-1] = "#"
        result[position] = "#"
        result[position+1] = "#"
    return result

def printCRTLine(lineCRT:list) -> None:
    print(f"{''.join(lineCRT)}")

def executePrograme(code: list) -> int:
    registerX = 1
    clockCircuit = 241
    ipCode = 0
    cycle = 1
    codeSize = len(code)
    signalStrength = 0
    line = 0
    endCRTLine = [40, 80, 120, 160, 200, 240]
    beginCRTLine = [1, 41, 81, 121, 161, 201]
    resultat = 0
    sprite = spritePosition(registerX)
    pixel = 0
    for tick in range(1,clockCircuit):
        #logger.debug({tick})
        if tick == beginCRTLine[line]:
            currentCRTrow = []

        if ipCode < codeSize:
            instruction = code[ipCode]
        else:
            #fin code
            break

        currentCRTrow.append(sprite[pixel])
        #logger.debug(f"sprite Position tick: {tick} \n{''.join(currentCRTrow)} \n{''.join(sprite)}")


        if instruction == "noop":
            ipCode += 1
            cycle = 1
        elif "addx" in instruction:
            if cycle == 0 :
                registerX += int(instruction.split()[1])
                sprite = spritePosition(registerX)
                ipCode += 1
                cycle = 1
            else:
                cycle -= 1

        pixel += 1
        if tick == endCRTLine[line]:
            printCRTLine(currentCRTrow)
            line += 1
            currentCRTrow = []
            pixel = 0


    return resultat



def main():

    #fileinput = 'test2.txt'
    fileinput = 'input.txt'
    code = loadProgram(fileinput)
    executePrograme(code)
    #print(f"resultat X: {sumSignal}")
    #printCRTLine(spritePosition(39))


if __name__ == '__main__':

    main()
