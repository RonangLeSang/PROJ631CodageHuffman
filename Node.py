class Node:
    """
    Classe représentant un nœud avec une fréquence et un label (son caractère)
    """

    def __init__(self, label, frequency=None, lChild=None, rChild=None):
        self.label = label
        self.frequency = frequency
        self.lChild = lChild
        self.rChild = rChild

    def __le__(self, node):
        return self.frequency <= node.frequency

    def __lt__(self, node):
        return self.frequency < node.frequency

    def __str__(self):
        return f"label : {self.label} frequency : {self.frequency}"

    def __add__(self, node):
        return self.frequency + node.frequency

    def __repr__(self):
        return self.__str__()

    def get_children(self):
        """
        Renvoi tous les enfants du nœud dans un tuple
        """
        return tuple(self.lChild, self.rChild)

    def set_children(self, lChild, rChild):
        """
        Défini les enfants du nœud
        """
        self.lChild = lChild
        self.rChild = rChild

    @staticmethod
    def min_child(liste):
        """
        Retourne les deux nœuds minimums de la liste passée en paramètre
        """
        children = []
        for i in range(0, 2):
            min = liste[0]
            for node in liste:
                if not node == None:
                    if node < min:
                        min = node
            liste.remove(min)
            children.append(min)
        return children[0], children[1]

    def add_children(self, liste):
        """
        Ajoute au nœud courant les deux enfants avec la fréquence la plus faible de la liste passée en paramètre et
        change la fréquence courante
        """
        lChild, rChild = self.min_child(liste)
        self.frequency = lChild + rChild
        self.set_children(lChild, rChild)

    def isLeaf(self):
        """
        Retourne si le nœud est une feuille ou non
        """
        return self.rChild == self.lChild == None

    def cherche_path(self, path='', res={}):
        """
        Renvoi le dictionnaire de tous les caractères avec leurs codes binaires
        """
        if self.isLeaf():
            res[self.label] = path
            return res
        else:
            self.lChild.cherche_path(path + '0', res)
            self.rChild.cherche_path(path + '1', res)
        return res
