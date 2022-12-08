


#file = "test.txt"
file = "input.txt"

l = []

def isOverlap(e1, e2):
    return len(e1.intersection(e2)) != 0

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
        if isOverlap(l[0], l[1]):
            result += 1
        #print(f"l : {l}")
        l.clear()
    print(f"count paire fully content: {result}")