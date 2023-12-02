import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
compareLog = logging.getLogger("function_compare")


# input = "test.txt"
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


with open(input, 'r') as f :
    pair_count = 1
    isRight = False
    resultat = []
    for line in f:
        if line.strip() == '':
            logger.debug(f"== Pair {pair_count} ==")
            t = compare(leftList, rightList)
            print(f"paire {pair_count} t: {t}")
            if t :
                resultat.append(pair_count)
            pair_count += 1
        else:
            if isRight:
                rightList = eval(line.strip())
                isRight = False
            else:
                leftList = eval(line.strip())
                isRight = True
    print(f"resultat : {resultat} \nsum : {sum(resultat)}")