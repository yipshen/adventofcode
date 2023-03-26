import logging
from monkey import Monkey
import re
import gmpy2
from gmpy2 import mpz
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def monkeyExiste(dictMonkey, monkeyId) -> bool:
    if monkeyId in dictMonkey:
            return True
    return False

def searchMonkey(dictMonkey, monkeyId) -> Monkey:
    return dictMonkey[monkeyId]


def loadData(input: str) -> dict:
    dictofMonkeys = {}

    with open(input, 'r') as f:
        for line in f:
            if "Monkey" in line:
                id = int(line[-3])
                # logger.debug(f"id {id} type: {type(id)} ")
                if not monkeyExiste(dictofMonkeys, id):
                    dictofMonkeys[id] = Monkey(id)
            elif "items" in line:
                items = re.search('items:(.*)$', line).group(1).strip().split(',')
                logger.debug(f"monkey {dictofMonkeys[id].getMonkeyId()} items {items}")
                # q = list(map(mpz, items))
                q = list(map(int, items))
                logger.debug(f"monkey {dictofMonkeys[id].getMonkeyId()} items q {q}")
                dictofMonkeys[id].addItem(q)
            elif "Operation" in line:
                operation = re.search('new = (.*)$', line).group(1)
                logger.debug(f"operation {operation} type: {type(operation)}")
                dictofMonkeys[id].setOperation(operation)
            elif "Test" in line:
                decisionValue = int(re.search('by (.*)$', line).group(1))
                logger.debug(f"decisionValue {decisionValue} type: {type(decisionValue)}")
                dictofMonkeys[id].setDecisionValue(decisionValue)
            elif "true" in line:
                idMonkey1 = int(line[-2])
                logger.debug(f"idMonkey1 {idMonkey1}")
                if monkeyExiste(dictofMonkeys, idMonkey1):
                    m1 = searchMonkey(dictofMonkeys, idMonkey1)
                    dictofMonkeys[id].addMonkeyFriend(m1)
                else:
                    m1 = Monkey(idMonkey1)
                    dictofMonkeys[idMonkey1] = m1
                    dictofMonkeys[id].addMonkeyFriend(m1)
            elif "false" in line:
                idMonkey2 = int(line[-2])
                logger.debug(f"idMonkey2 {idMonkey2}")
                if monkeyExiste(dictofMonkeys, idMonkey2):
                    m2 = searchMonkey(dictofMonkeys, idMonkey2)
                    dictofMonkeys[id].addMonkeyFriend(m2)
                else:
                    m2 = Monkey(idMonkey2)
                    dictofMonkeys[idMonkey2] = m2
                    dictofMonkeys[id].addMonkeyFriend(m2)

    return dictofMonkeys

def MonkeysStatus(dictMonkey):
    # print("************ status monkey ************")
    for i in range(0, len(dictMonkey)):
        print(f"monkey {i} div: {dictMonkey[i].getDecisionValue()} ope: {dictMonkey[i].getOperation()} Friends {dictMonkey[i].getMonkeyFriends()} items: {dictMonkey[i].getAllItem()}")


def MonkeysItemSize(dictMonkey):
    print("************ Monkey item size ************")
    for i in range(0, len(dictMonkey)):
        item = dictMonkey[i].getItem()
        if item:
            itemSize = len(dictMonkey[i].getItem())
            print(f"monkey {i} : {itemSize}")

def main():
    file = 'test.txt'
    #file = 'input.txt'
    monkeys = loadData(file)
    stats ={}
    totalMonkey = len(monkeys)
    for i in range(0, totalMonkey):
        stats[i] = 0
    #stats = {0:0, 1:0, 2:0, 3:0}
    #print(f"monkeys {monkeys}")
    print("@@@@@@@@@@@@@@@@@@  start  @@@@@@@@@@@@@@@@@@@@@@@@")
    MonkeysStatus(monkeys)
    for loop in range(1, 21):
        # start_time = time.time()
        for m in range(0, totalMonkey):
            currentMonkey = monkeys[m]
            countItem = len(currentMonkey.getAllItem())

            for ite in range(0, countItem):
                # print(f"Monkey {currentMonkey} list Item : {currentMonkey.getAllItem()}")
                #worry = currentMonkey.getWorryLevel()
                #start_time = time.time()
                currentMonkey.throwItem2()
                #print(f"throwItem2 - execute time: {(time.time() - start_time)} s")
                #print(f"Monkey{currentMonkey} item {currentMonkey.getItem()} worry: {worry}")
                stats[m] += 1
            # print("\n")
            print(f"------------monkey {m} inspect all item ------------------")
            MonkeysStatus(monkeys)
        # if loop == 1 or loop == 20 or loop == 1000 or loop == 2000:
        print(f"========= end round {loop}====================")
        MonkeysStatus(monkeys)
        #MonkeysItemSize(monkeys)
        print(stats)
        # print(f"loop {loop} - execute time: {(time.time() - start_time)} s")


    listNbInspect = sorted([stats[x] for x in stats ], reverse=True)
    solution = listNbInspect[0] * listNbInspect[1]
    #
    print(f"{stats} max {solution}")


if __name__ == '__main__':

    main()










