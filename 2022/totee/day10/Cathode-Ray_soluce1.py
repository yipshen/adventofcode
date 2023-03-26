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

def executePrograme(code: list) -> int:
    registerX = 1
    clockCircuit = 221
    ipCode = 0
    cycle = 1
    codeSize = len(code)
    signalStrength = 0
    idSignal = 0
    listSignal = [20, 60, 100, 140, 180, 220]
    resultat = 0
    for tick in range(2,clockCircuit):
        #logger.debug({tick})
        if ipCode < codeSize:
            instruction = code[ipCode]
        else:
            #fin code
            break

        if instruction == "noop":
            ipCode += 1
            cycle = 1
        elif "addx" in instruction:
            if cycle == 0 :
                registerX += int(instruction.split()[1])
                ipCode += 1
                cycle = 1
            else:
                cycle -= 1

        if tick == listSignal[idSignal]:
            signalStrength = listSignal[idSignal] * registerX
            logger.debug(f"cyle {listSignal[idSignal]} register X : {registerX} signal strength : {signalStrength}")
            idSignal += 1
            resultat += signalStrength

    return resultat



def main():

    #fileinput = 'test2.txt'
    fileinput = 'input.txt'
    code = loadProgram(fileinput)
    sumSignal = executePrograme(code)
    print(f"resultat X: {sumSignal}")



if __name__ == '__main__':

    main()

