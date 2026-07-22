"""test_identite.py — pourquoi DELETE n'existe pas dans ce modèle.

Ce n'est pas une préférence éthique ("on aime garder l'histoire").
C'est une preuve structurelle : dans un graphe où l'identité est
portée par le NOM (pas par un identifiant externe généré ailleurs),
supprimer un nœud scinde ce nom en deux identités incompatibles.

python test_identite.py — zéro dépendance, comme le reste.
"""
from vector import Vector

reg = {}
def V(name):
    if name not in reg: reg[name] = Vector(name)
    return reg[name]


def construire_graphe():
    """Deux vecteurs tiennent chacun un lien vers un troisième, avec
    un historique réel (`seen`) sur ce dernier."""
    T1 = V("2026-07-22_10h00")
    V("JS").links.append((T1, V("FB"), V("Kage")))
    T2 = V("2026-07-22_11h00")
    V("Sarah").links.append((T2, V("JS"), V("Kage")))
    V("Kage").seen.append(T1)
    V("Kage").seen.append(T2)


def simuler_suppression(nom: str):
    """Ce qu'une opération DELETE ferait : retirer le nom du registre.
    Les liens EXISTANTS, eux, gardent une référence Python directe à
    l'ancien objet — ils ne "savent" pas qu'il a été supprimé."""
    return reg.pop(nom)


def demontrer():
    construire_graphe()
    print("=== Avant suppression ===")
    print(f"  Kage.seen : {[t.name for t in V('Kage').seen]}  (historique réel)")

    ancien_kage = simuler_suppression("Kage")

    print("\n=== 'Kage' supprimé du registre ===")
    nouveau_kage = V("Kage")   # une nouvelle recherche par le même nom

    meme_objet = ancien_kage is nouveau_kage
    print(f"  Nouvel objet 'Kage' recréé, id={id(nouveau_kage)}")
    print(f"  Est-ce le même que celui référencé par JS et Sarah ? {meme_objet}")
    print(f"  Historique du nouveau 'Kage' : {nouveau_kage.seen}  (vide !)")

    assert not meme_objet, "la suppression aurait dû casser l'identité"
    assert nouveau_kage.seen == [], "le nouveau Kage ne doit avoir aucun passé"
    assert ancien_kage.seen != [], "l'ancien Kage garde son passé, inaccessible"

    print("\n=== Verdict ===")
    print("  Le même nom 'Kage' désigne maintenant DEUX entités distinctes :")
    print("  - celle que suivent les liens existants de JS et Sarah (historique intact)")
    print("  - celle que retrouve toute NOUVELLE recherche par ce nom (vide)")
    print()
    print("  Ce n'est pas une perte d'information. C'est une incohérence")
    print("  d'identité : le modèle ne peut plus garantir son invariant")
    print("  fondateur — un nom = une identité stable dans le temps.")
    print()
    print("  Conclusion : DELETE n'est pas absent de ce modèle par choix")
    print("  éthique seul. Il est absent parce que sa présence romprait")
    print("  la définition même de ce qu'est un Vector.")


if __name__ == "__main__":
    demontrer()
