"""verifier.py — un organe de lecture, pas une pièce du modèle.

Le modèle n'interdit pas la suppression : Python la permet, ici comme
partout. Mais un graphe où l'identité est le contenu porte les traces
de ce qu'on lui retire. Ce fichier les cherche.

Ce n'est pas une protection. C'est un examen.

python verifier.py — zéro dépendance, comme le reste.
"""


def references_brisees(reg):
    """Un lien atteint un objet qui n'est plus celui du registre.

    Signature d'un nœud supprimé : les liens existants gardent une
    référence directe vers l'ancien objet, tandis qu'une nouvelle
    recherche par le même nom en recrée un autre, vide. Le même nom
    désigne alors deux entités — et cette incohérence se voit."""
    anomalies = []
    for v in reg.values():
        for lien in v.links:
            for x in lien:
                if reg.get(x.name) is not x:
                    anomalies.append((v.name, x.name))
    return anomalies


def orphelins(reg):
    """Un citoyen que plus aucun lien n'atteint et qui n'affirme rien.

    Signature possible d'un qualificateur retiré : il subsiste au
    registre, mais plus rien ne le porte. Il n'a aucune raison d'être
    là. Attention : un citoyen fraîchement créé et pas encore relié
    a la même forme — c'est un signal, pas une preuve."""
    atteints = {x.name for v in reg.values() for l in v.links for x in l}
    return [n for n, v in reg.items() if n not in atteints and not v.links]


def examiner(reg):
    """Les deux examens, ensemble. Retourne un rapport lisible."""
    brisees, orph = references_brisees(reg), orphelins(reg)
    return {
        "references_brisees": brisees,
        "orphelins": orph,
        "intact": not brisees and not orph,
    }


# ── La limite, dite franchement ───────────────────────────────────
#
# Ces deux examens détectent :
#   - la suppression d'un nœud atteint par des liens existants
#   - le retrait d'un qualificateur qui n'était porté que là
#
# Ils NE détectent PAS :
#   - le retrait d'un qualificateur partagé ailleurs dans le graphe
#
# Retirer 'JS' d'un lien alors qu'un autre lien porte encore 'JS' ne
# laisse aucune trace structurelle. L'affirmation devient anonyme, et
# rien ne le signale. C'est une limite réelle du modèle, pas un défaut
# de cet examen.
#
# Ce qui reste vrai : plus un graphe est dense en partage — donc plus
# il est un graphe et non une chaîne — plus les suppressions ont de
# chances de rompre quelque chose de visible. Le partage n'est pas
# seulement la condition de l'émergence. C'est aussi ce qui rend
# l'appauvrissement coûteux à dissimuler.


if __name__ == "__main__":
    from vector import Vector

    reg = {}
    def V(n):
        if n not in reg: reg[n] = Vector(n)
        return reg[n]

    V("JS").links.append([V("Kage"), V("T1"), V("FB")])
    V("Kage").links.append([V("Kage"), V("T1")])
    print("Graphe sain      :", examiner(reg)["intact"])

    reg.pop("Kage"); V("Kage")
    r = examiner(reg)
    print("Après suppression:", r["intact"], "->", r["references_brisees"])
