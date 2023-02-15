
class repertoire:
    "definition d'un objet répertoire"
    def __init__(self, nom, parentdir, contenue):
        self.__nom = nom
        self.__parentdir = parentdir
        self.__contenue = contenue
        self.__nbContenue = len(contenue)
        #print(f"create (repertoire: {self.__nom} parentdir: {self.__parentdir} contenue: {self.__contenue})")

    def get_nom(self):
        return self.__nom

    def get_nbContenue(self):
        return self.__contenue

    def get_parentdir(self):
        return self.__parentdir

    def get_contenue(self):
        return self.__contenue

    def add_contenue(self, objet):
        self.__contenue.append(objet)

    def __str__(self):
        return "- %s (dir)" % (self.__nom)

    def affiche_contenu(self):
        print(f"{self.__contenue}")

    def affiche(self):
        self.exploreContenue_rec(0)

    def affiche_rec(self, decalage):
        print(f"  "*decalage+f"{self}")

    def exploreContenue_rec(self, profondeur):
        self.affiche_rec(profondeur)
        for e in self.__contenue:
            if isinstance(e, repertoire):
                e.exploreContenue_rec(profondeur+1)
            else:
                e.affiche_rec(profondeur+1)

    def exploreContenue(self):
        self.exploreContenue_rec(0)

    def getSize_rec(self):
        result = 0
        for e in self.__contenue:
            if isinstance(e, repertoire):
                result += e.getSize_rec()
            else:
                result += e.get_taille()
        return result

    def searchDirSizeOver(self, size):
        result_list = ""
        for e in self.__contenue:
            if isinstance(e, repertoire):
                if e.getSize_rec() > size:
                    result_list += e.get_nom()
        return result_list

    def get_repertoire(self, nom):
        if self.__nom is nom:
            return self
        else:
            for elm in self.__contenue:
                if (isinstance(elm, repertoire)) & (elm.get_nom() == nom):
                    return elm

    def calculate_all_dir(self):
        result = 0
        for k in self.__contenue:
            if isinstance(k, repertoire):
                result += k.calculate_all_dir()
        print(f"{self.get_nom()} size : {self.getSize_rec()}")
        return result

    def listAllDirAboveSize(self, listDir, size):
        print(f"{self} {self.getSize_rec()}")
        if self.getSize_rec() >= size:
            listDir.append((self.get_nom(), self.getSize_rec()))
        for k in self.__contenue:
            if isinstance(k, repertoire):
               # print(f"{k} {k.getSize_rec()}")
                if k.getSize_rec() >= size:
                    k.listAllDirAboveSize(listDir, size)
        return listDir

    #return list contain couple directory name with total size
    def getListAllDirSize(self, liste):
        print(f"{self} {self.getSize_rec()}")
        liste.append((self.get_nom(), self.getSize_rec()))
        for k in self.__contenue:
            if isinstance(k, repertoire):
                k.getListAllDirSize(liste)
        return liste