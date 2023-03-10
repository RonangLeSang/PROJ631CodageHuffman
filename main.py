import os

from Node import Node


def tri_frequence(liste):
    """
    Cette fonction retourne une liste triée en fonction du nombre d'apparences de
    chaque caractère de la liste en entrée
    """
    return [char for char in sorted(liste, key=lambda x: x[1])]


def tri_ascii(dico):
    """
    Cette fonction retourne une liste triée en fonction du caractère ascii de
    chaque caractère du dictionnaire en entrée
    """
    return sorted(dico.items(), key=lambda x: ord(x[0]))


def to_txt(liste, nom):
    """
    Écrit un fichier avec la liste passée en paramètre
    """
    with open(f"{nom[:-4]}_freq.txt", "w") as f:
        f.write(f"{len(liste)}\n")
        for i in liste:
            f.write(f"{i[0]}  {i[1]} \n")


def open_file(path):
    """
    Renvoi un dictionnaire avec l'alphabet et les occurrences des caractères
    """
    with open(path, "r") as f:
        texte = f.read()
    dico = {}
    for char in texte:
        if char in dico.keys():
            dico[char] += 1
        else:
            dico[char] = 1
    return dico


def list_to_nodes(liste):
    """
    Renvoi une liste de nœuds à partir d'une liste de caractères
    """
    return [Node(char[0], char[1]) for char in liste]


def construct_tree(liste):
    """
    Construit un arbre à partir d'une liste
    """
    while len(liste) > 1:
        node = Node("neud")
        node.add_children(liste)
        liste.append(node)
    return liste


def into_bin(path, dico):
    """
    Lit dans un fichier texte et le code selon Huffman
    """
    with open(path) as file:
        txt = file.read()
    res = ''
    for char in txt:
        res += dico[char]
    return res


def into_oct(binary):
    """
    Transforme le texte binaire en paramètre en octet
    """
    res = int(binary, 2)
    length = (res.bit_length() + 7) // 8
    res = res.to_bytes(length, byteorder='big')
    return res


def save_comp(path, octets):
    """
    Écrit le texte codé dans un fichier binaire
    """
    with open(f"{path[:-4]}_comp.txt", "wb") as file:
        file.write(octets)


def size_comp(path):
    """
    Compare la taille du fichier encodé par rapport au fichier original
    """
    originalSize = os.stat(path).st_size
    compSize = os.stat(f"{path[:-4]}_comp.txt").st_size
    return 1 - compSize / originalSize


def moy_bits(dico):
    """
    Renvoi le nombre de bits utilisé pour un caractère
    """
    total = 0
    for bits in dico.values():
        total += len(bits)
    return total / len(dico.keys())


def codage(path):
    """
    Code le fichier selon le codage Huffman et renvoi so taux de compression ainsi que son nombre moyen de bits par
    caractère
    """
    dico = open_file(path)
    liste = tri_frequence(tri_ascii(dico))
    to_txt(liste, path)
    nodes = list_to_nodes(liste)
    root = construct_tree(nodes)[0]
    dicoPath = root.cherche_path()
    binTxt = into_bin(path, dicoPath)
    binTxt = into_oct(binTxt)
    save_comp(path, binTxt)
    tauxComp = size_comp(path)
    nbBitsMoyen = moy_bits(dicoPath)
    return tauxComp, nbBitsMoyen


if __name__ == "__main__":

    path = "ressources/alice.txt"

    tauxComp, nbBitsMoyen = codage(path)
    print(f"taux de compression : {tauxComp * 100} %\n"
          f"nombre de bits moyens par lettre : {nbBitsMoyen} bits")
