from repertoire import repertoire
from fichier import fichier

file = "test.txt"
# file = "input.txt"
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
total = [x for (i,x) in l1 if (x < 100000)]
print(f"total : {total}\nsum : {sum(total)}")


# root = repertoire("/", None, [])
# a = repertoire("a", root, [])
# e = repertoire("e", a, [])
# f = fichier("f", 29116, a)
# g = fichier("g", 2557, a)
# h = fichier("h.lst", 62596, a)
# i = fichier("i", 584, e)
# b = fichier("b.txt", 14848514, root)
# c = fichier("c.dat", 8504156, root)
# d = repertoire("d", root, [])
# j = fichier("j", 4060174, root)
#
# e.add_contenue(i)
# root.add_contenue(a)
# a.add_contenue(e)
# a.add_contenue(f)
# a.add_contenue(g)
# a.add_contenue(h)
# root.add_contenue(b)
# root.add_contenue(c)
# root.add_contenue(d)
# d.add_contenue(j)
# root.affiche()
# print(root.get_repertoire(root.get_nom()))
# print(root.get_repertoire(e.get_nom()))
# print(root.get_repertoire(d.get_nom()))
# root.affiche_rec(0)
# root.affiche_rec(1)
# root.affiche_rec(2)
#
# root.affiche()
#
# print(f"root: {root.getSize_rec()}")
# print(f"a: {a.getSize_rec()}")
# print(f"e: {e.getSize_rec()}")
# print(f"dir > 100 : {a.searchDirSizeOver(100)}")
