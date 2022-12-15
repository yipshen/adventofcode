


#file = "test.txt"
file = "input.txt"

def areOccurence(liste):
    list_size = len(liste)
    for e in liste :
        #print(f"areOccurence : {liste.count(e)}")
        if liste.count(e) >= 2:
            return True
    return False

#print(f"areOccurence('abcd'): {areOccurence('abcd')}")
#print(f"areOccurence('abcda'): {areOccurence('abcda')}")

with open(file, "r") as f:
    for line in f :
        print(f"ligne: {line}")
        for i,c in enumerate(line) :
            #print(f"line[{i}:{i+4}]: {line[i:i+4]}")
            if not (areOccurence(line[i:i+14])):
                print(f"fanion : {i+14}")
                break

