

class fichier:

    def __init__(self, nom, taille, parentdir):
        self.__nom = nom
        self.__taille = taille
        self.__parentdir = parentdir
        #print(f"create (fichier: {self.__nom} taille: {self.__taille} parentdir: {self.__parentdir})")

    def get_nom(self):
        return self.__nom

    def get_taille(self):
        return self.__taille

    def get_parentdir(self):
        return self.__parentdir

    def __str__(self):
        return "- %s (file, size=%d)" % (self.__nom, self.__taille)

    def affiche_rec(self,decalage):
        print(f"  "*decalage+f"{self}")

    def affiche(self):
        print(self)