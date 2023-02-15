from repertoire import repertoire
from fichier import fichier

#file = "test.txt"
file = "input.txt"
root = repertoire("/", None, [])
def loadInputFile(file):
    currentDir = None
    with open(file, "r") as f:
        for line in f:
            # print(f">>>>>>>{line}")
            if line.split()[0] == "$":
                if len(line.split()) > 2 :
                    # cd commands
                    argument = line.split()[2]

                    if argument == "..":
                        # change directory to parent
                        currentDir = currentDir.get_parentdir()
                    else:
                        # if this new director is root
                        if argument == "/" :
                            currentDir = root
                        else:
                            currentDir = currentDir.get_repertoire(argument)
                    # print(f"currentDir : {currentDir.get_nom()}")
            else:
                # listing elements
                # print(f"element: {line}",end="")
                if line.split()[0] == "dir":
                    nom_repertoire = line.split()[-1]
                    new_rep = repertoire(nom_repertoire, currentDir, [])
                    currentDir.add_contenue(new_rep)
                    currentDir.affiche_contenu()
                    # print(f"addDirectory({line.split()[-1]})")
                else:
                    nom_fichier = line.split()[-1]
                    taille_fichier = int(line.split()[0])
                    new_file = fichier(nom_fichier, taille_fichier, currentDir)
                    currentDir.add_contenue(new_file)
                    currentDir.affiche_contenu()
                    # print(f"addFile({line.split()[-1]})")
                    # addFile()


loadInputFile(file)
root.affiche()
#listDir = root.findAllDirAboveSize([],100000)

#print(f" {root.get_repertoire('a').get_repertoire('e').getSize_rec()}")


#l1 = root.listAllDirAboveSize([],100)
l1 = root.getListAllDirSize([])
print(f"l1 : {l1}")
# filter directory size inferior to 100000
total = [x for (i,x) in l1]
total.sort()
def chooseDeleteDir(listDir):
    filesystemSpace = 70000000
    firmwareSpace = 30000000
    usedSpace = listDir[-1]
    for elm in listDir:
        if (elm + (filesystemSpace - usedSpace)) >= firmwareSpace :
            return elm

resultat = chooseDeleteDir(total)

print(f"smallest size dir to delete is {resultat}")
