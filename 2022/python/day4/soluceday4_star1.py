


#file = "test.txt"
file = "input.txt"

l = []

def isInEnsemble(e1, e2):
    return (len(e1 - e2) == 0) or (len(e2 - e1) == 0)

# a = isInEnsemble({6},{3,4,5,6})
# b = isInEnsemble({2,3},{3,4,5})
# print(f"isInEnsemble({6},{3,4,5,6}) :{a}")
# print(f"isInEnsemble({2,3},{3,4,5}) :{b}")


result = 0
with open(file, "r") as f:
    for line in f:
        a = line.strip().split(",")
        #print(f"a: {a}")
        for e in a:
            #print(f"e: {e.split('-')}")
            lBorne = e.split("-")
            borneInf = int(lBorne[0])
            borneSup = int(lBorne[1])+1
            #print(f"borneInf: {borneInf} borneSup: {borneSup}")
            ensemble = set([x for x in range(borneInf, borneSup)])
            l.append(ensemble)
        if isInEnsemble(l[0], l[1]):
            result += 1
        #print(f"l : {l}")
        l.clear()
    print(f"count paire fully content: {result}")
