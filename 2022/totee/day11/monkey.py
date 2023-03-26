import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import gmpy2
from gmpy2 import mpz, mul, powmod, add
import time



class Monkey:

    def __init__(self, monkeyId: int, listItem: list, decisionValue: int, operation :str , monkeyFriends: list):
        self.__listItem = listItem
        self.__decisionValue = decisionValue
        self.__monkeyId = monkeyId
        self.__operation = operation
        self.__monkeyFriendsToShare = monkeyFriends

    def __init__(self, monkeyId: int, listItem: list = None, decisionValue: int = "", operation :str = "", monkeyFriends: list = None ):
        self.__listItem = list()
        self.__decisionValue = decisionValue
        self.__monkeyId = monkeyId
        self.__operation = operation
        self.__monkeyFriendsToShare = list()


    def whoiam(self):
        return self

    def getItem(self):
        if self.__listItem :
            return self.__listItem[0]


    def getAllItem(self):
        return self.__listItem

    def addItem(self, a):
        if isinstance(a, list):
            self.__listItem.extend(a)
        else:
            self.__listItem.append(a)

    def getDecisionValue(self):
        return self.__decisionValue

    def setDecisionValue(self, v):
        self.__decisionValue = v

    def setOperation(self, ope):
        # if ope == "old * old":
        #     self.__operation = "mul(old, old)"
        # elif "old *" in ope:
        #     self.__operation = "mul(old,"+ope[5:]+")"
        # elif "old +" in ope:
        #     self.__operation = "add(old,"+ope[5:]+")"
        self.__operation = ope


    def getOperation(self):
        return self.__operation

    def getMonkeyId(self):
        return self.__monkeyId

    def getWorryLevel(self):
        if len(self.__listItem) > 0:
            old = self.__listItem[0]
            return eval(self.__operation)
        else:
            return None


    def addMonkeyFriend(self,monkeyFriends):
        if isinstance(monkeyFriends, list):
            self.__monkeyFriendsToShare.extend(monkeyFriends.copy())
        else:
            self.__monkeyFriendsToShare.append(monkeyFriends)

    def getMonkeyFriends(self):
        return list(map(lambda Monkey: Monkey.getMonkeyId(),self.__monkeyFriendsToShare))


    def inspectItem(self, item, ope):
        # start_time = time.time()
        logger.debug(f"inspectItem - item :{item} ope: {ope}")
        old = item
        result = eval(ope)
        # print(f"inspectItem execute time: {(time.time() - start_time)} s")
        return result

    def throwItem(self):
        newWorryItem = self.getWorryLevel()
        boredItemValue = newWorryItem // 3
        logger.debug(f"monkey {self.__monkeyId} worry level after inspect {newWorryItem} bored Worry Level divided by 3 :{boredItemValue}")
        if boredItemValue % self.__decisionValue == 0:
            logger.debug(f"throw item {boredItemValue} to Monkey {self.__monkeyFriendsToShare[0].getMonkeyId()}")
            self.__monkeyFriendsToShare[0].addItem(boredItemValue)
        else:
            logger.debug(f"throw item {boredItemValue} to Monkey {self.__monkeyFriendsToShare[1].getMonkeyId()}")
            self.__monkeyFriendsToShare[1].addItem(boredItemValue)
        self.__listItem.pop(0)

    def throwItem2(self):
        boredItemValue = self.inspectItem(self.getItem(), self.__operation)
        logger.debug(f"throwItem2 - boredItemValue : {boredItemValue}")
        if boredItemValue % self.__decisionValue == 0:
            # print(f"test is_divible - execute time: {(time.time() - start_time)} s")
            print(f"++++++monkey {self.__monkeyId} item {boredItemValue} is divisible by {self.__decisionValue}+++++++")
            # congruence = gmpy2.c_mod(boredItemValue, self.__decisionValue)
            congruence = boredItemValue % self.__decisionValue
            logger.debug(f"throw item {congruence} to Monkey {self.__monkeyFriendsToShare[0].getMonkeyId()}")
            #start_time = time.time()
            self.__monkeyFriendsToShare[0].addItem(congruence)
            #print(f"addItem - execute time: {(time.time() - start_time)} s")
        else:
            # print(f"test is_divible - execute time: {(time.time() - start_time)} s")
            # congruence = gmpy2.c_mod(boredItemValue, self.__decisionValue)
            # congruence = boredItemValue % self.__decisionValue
            logger.debug(f"throw item {boredItemValue} to Monkey {self.__monkeyFriendsToShare[1].getMonkeyId()}")


            self.__monkeyFriendsToShare[1].addItem(boredItemValue)
        self.__listItem.pop(0)


    def __str__(self):
        return "Monkey %d \nlistItem: %s \noperation: %s \ndecisionValue: %d \nmonkeyFriends %s" %\
           (self.__monkeyId, self.__listItem, self.__operation, self.__decisionValue, self.getMonkeyFriends())





    def affiche(self):
        print(self)




# m1 = Monkey(1, [1, 2], 23, "old + 1", [])
# m2 = Monkey(2, [3, 4], 19, "old * old", [])
# m3 = Monkey(3, [5, 6], 19, "old + 3", [m1, m2])
# m1.affiche()
# m2.affiche()
# m3.affiche()
# m3.addMonkeyFriend(m1)
# m3.affiche()
#print(m2.getWorryLevel())
