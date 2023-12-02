import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
compareLog = logging.getLogger("function_compare")


#input = "test.txt"
input = "input.txt"



def compare(left, right, depth=0):
    # print(" "*depth + f"- Compare {left} vs {right}")
    compareLog.debug(" "*depth + f"- Compare {left} vs {right}")
    depth += 1
    leftSize = len(left)
    rightSize = len(right)
    result = None
    if isinstance(left, list) and isinstance(right, list):
        # right and left is both list
        for i in range(leftSize):
            if result != None:
                break
            if i < rightSize:
                (l,r) = (left[i],right[i])
                # first value right and first value left is integer
                if isinstance(l, int) and isinstance(r, int):
                    # print(" "*depth + f"- Compare {l} vs {r}")
                    compareLog.debug(" "*depth + f"- Compare {l} vs {r}")
                    if l < r :
                        depth += 1
                        # print(" "*depth + f"- Left side is smaller, so inputs are in the right order")
                        compareLog.debug(" " * depth + f"- Left side is smaller, so inputs are in the right order")
                        return True
                    if l > r :
                        depth += 1
                        # print(" "*depth + f"- Right side is smaller, so inputs are not in the right order")
                        compareLog.debug(" " * depth + f"- Right side is smaller, so inputs are not in the right order")
                        return False

                # both value are lists
                if isinstance(l, list) and isinstance(r, list):
                    result = compare(l,r,depth)

                # exactly one value is an integer
                if (isinstance(l,list) and isinstance(r, int)) :
                    # print(" "*depth + f"- Compare {l} vs {r}")
                    compareLog.debug(" " * depth + f"- Compare {l} vs {r}")
                    depth += 1
                    # print(" "*depth + f"- Mixed types; convert left to [{r}] and retry comparison")
                    compareLog.debug(" " * depth + f"- Mixed types; convert left to [{r}] and retry comparison")
                    n = [r]
                    result = compare(l, n,depth)

                if (isinstance(l, int) and isinstance(r,list)) :
                    # print(" "*depth + f"- Compare {l} vs {r}")
                    compareLog.debug(" " * depth + f"- Compare {l} vs {r}")
                    depth += 1
                    # print(" "*depth + f"- Mixed types; convert left to [{l}] and retry comparison")
                    compareLog.debug(" " * depth + f"- Mixed types; convert left to [{l}] and retry comparison")
                    n = [l]
                    result = compare(n, r,depth)
            else:
                break
        # break recursive function
        if result != None:
            return result
        if leftSize < rightSize :
            # print(" "*depth + f"- Left side ran out of items, so inputs are in the right order")
            compareLog.debug(" " * depth + f"- Left side ran out of items, so inputs are in the right order")
            return True

        if leftSize > rightSize :
            # print(" " * depth + f"- Right side ran out of items, so inputs are not in the right order")
            compareLog.debug(" " * depth + f"- Right side ran out of items, so inputs are not in the right order")
            return False
    return result

def countElement(liste):
    cpt=0
    if isinstance(liste, list):
        cpt += 1
        for e in liste:
            cpt += countElement(e)
    else:
        cpt += 1
    return cpt

def printList(l):
    print('-'*20)
    pos = 1
    for i in l:
        print(f"{pos}: {i}")
        pos += 1

listToSort = []
with open(input, 'r') as f :
    pair_count = 1
    isRight = False

    for line in f:
        if line != '\n':
            listToSort.append(eval(line.strip()))
    listToSort.append([[2]])
    listToSort.append([[6]])

# logger.debug(f"listTSort : {listToSort} ")
printList(listToSort)
# for i in listToSort:
#     logger.debug(f"{i} : len {len(i)} count: {countElement(i)-1}")

nonTrie = True
listSize = len(listToSort)
cptnonTrie = 0
round = 0
while nonTrie:
    round += 1
    cptnonTrie = 0
    for i in range(0,listSize-1):
        r = compare(listToSort[i],listToSort[i+1])
        # print(f"compare {listToSort[i - 1]} - {listToSort[i]} |r : {r}")
        if not r:
            switch = listToSort[i+1]
            listToSort[i+1] = listToSort[i]
            listToSort[i] = switch
            cptnonTrie += 1

    if cptnonTrie == 0:
        nonTrie = False

    print(f"round : {round}")

printList(listToSort)
index1 = listToSort.index([[2]]) + 1
index2 = listToSort.index([[6]]) + 1
print(f"position [[2]] :{index1} \nposition [[6]] : {index2} \n solution: {index1 * index2}")