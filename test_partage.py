"""test_partage.py — le partage est la condition d'existence du graphe.

Un qualificateur qui ne sert qu'une fois ne relie rien : il nomme une
place. Si TOUS les qualificateurs sont dans ce cas, le graphe n'est
plus un graphe — c'est une chaîne, et rien ne peut en émerger.

Ce test tisse le même texte de deux façons et mesure la différence.
Il produit les chiffres cités dans le README.

python test_partage.py — zéro dépendance, comme le reste.
"""
import re
from collections import defaultdict
from vector import Vector

TEXTE = ("Alice courait vite dans le jardin. Le chat dormait paisiblement. " * 300)


def decouper(t):
    return re.findall(r"[\wàâäéèêëïîôöùûüçÀÂÄÉÈÊËÏÎÔÖÙÛÜÇ\-']+|[.!?;:]|.",
                      t, re.DOTALL)


def tisser_compteur_plat():
    """Position = un compteur global. Chaque valeur sert exactement
    une fois — c'est le piège."""
    reg = {}
    def V(n):
        if n not in reg: reg[n] = Vector(n)
        return reg[n]
    pos, prec = 0, None
    for g in decouper(TEXTE):
        gv = V(g)
        if prec is not None:
            prec.links.append([gv, V(f"@{pos}")])
        prec, pos = gv, pos + 1
    return reg


def tisser_coordonnees():
    """Position = (phrase, rang du glyphe). Chaque coordonnée est
    partagée par tous les glyphes qu'elle situe."""
    reg = {}
    def V(n):
        if n not in reg: reg[n] = Vector(n)
        return reg[n]
    phrases = [p for p in re.split(r"(?<=[.!?])\s+", TEXTE) if p.strip()]
    for np, ph in enumerate(phrases):
        prec = None
        for ng, g in enumerate(decouper(ph)):
            gv = V(g)
            if prec is not None:
                prec.links.append([gv, V(f"p{np}"), V(f"g{ng}")])
            prec = gv
    return reg


def mesurer(reg):
    """Pour chaque qualificateur : combien de sujets distincts le
    portent ? C'est la capacité de convergence du graphe."""
    par_qual = defaultdict(set)
    for v in reg.values():
        for lien in v.links:
            for q in lien[1:]:
                par_qual[q.name].add(v.name)
    voisinages = [len(s) for s in par_qual.values()]
    return {
        "citoyens": len(reg),
        "qualificateurs": len(par_qual),
        "servant_une_fois": sum(1 for n in voisinages if n <= 1),
        "voisinage_moyen": sum(voisinages) / len(voisinages),
        "voisinage_max": max(voisinages),
    }


def test_compteur_plat_ne_fait_pas_de_graphe():
    m = mesurer(tisser_compteur_plat())
    assert m["servant_une_fois"] == m["qualificateurs"], \
        "avec un compteur plat, TOUS les qualificateurs sont à usage unique"
    assert m["voisinage_max"] == 1, \
        "aucun qualificateur ne relie jamais deux sujets"
    print(f"✓ compteur plat  : {m['citoyens']} citoyens, "
          f"{m['servant_une_fois']}/{m['qualificateurs']} à usage unique (100%), "
          f"voisinage max {m['voisinage_max']}")
    return m


def test_coordonnees_font_un_graphe():
    m = mesurer(tisser_coordonnees())
    assert m["servant_une_fois"] < m["qualificateurs"] * 0.05, \
        "presque aucun qualificateur n'est à usage unique"
    assert m["voisinage_moyen"] > 2, \
        "les chemins convergent réellement"
    print(f"✓ coordonnées    : {m['citoyens']} citoyens, "
          f"{m['servant_une_fois']}/{m['qualificateurs']} à usage unique, "
          f"voisinage moyen {m['voisinage_moyen']:.1f}")
    return m


def test_le_partage_change_l_echelle():
    plat = mesurer(tisser_compteur_plat())
    coord = mesurer(tisser_coordonnees())
    assert coord["citoyens"] < plat["citoyens"] / 5, \
        "le partage réduit massivement le nombre de citoyens"
    print(f"✓ rapport        : {plat['citoyens'] / coord['citoyens']:.1f}x moins "
          f"de citoyens, et des chemins qui se rejoignent")


if __name__ == "__main__":
    test_compteur_plat_ne_fait_pas_de_graphe()
    test_coordonnees_font_un_graphe()
    test_le_partage_change_l_echelle()
    print()
    print("Un qualificateur qui ne sert qu'une fois ne relie rien.")
    print("Sans partage, il n'y a pas de graphe — il y a une chaîne,")
    print("et rien ne peut émerger d'une chaîne.")
