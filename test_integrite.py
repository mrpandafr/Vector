"""test_integrite.py — ce qu'une suppression laisse comme trace.

Le modèle n'interdit rien. Mais dans un graphe où l'identité est le
contenu, retirer quelque chose rompt souvent une cohérence visible.
Ce test montre les deux cas où c'est vrai — et le cas où ça ne l'est
pas, parce qu'une limite tue vaut moins qu'une limite dite.

python test_integrite.py — zéro dépendance, comme le reste.
"""
from vector import Vector
from verifier import examiner, references_brisees, orphelins


def registre():
    reg = {}
    def V(name):
        if name not in reg: reg[name] = Vector(name)
        return reg[name]
    return reg, V


def test_suppression_de_noeud_est_detectable():
    """Un nœud atteint par des liens existants ne peut pas disparaître
    en silence : les liens gardent l'ancien objet, une nouvelle
    recherche en crée un autre. Deux entités, un seul nom."""
    reg, V = registre()
    V("JS").links.append([V("Kage"), V("T1"), V("FB")])
    V("Kage").links.append([V("Kage"), V("T1")])
    assert examiner(reg)["intact"], "graphe sain au départ"

    reg.pop("Kage")     # <- la suppression
    V("Kage")           # <- une recherche recrée un objet vide

    brisees = references_brisees(reg)
    assert brisees, "la référence brisée est visible"
    assert ("JS", "Kage") in brisees
    print("✓ suppression d'un nœud : référence brisée détectée")


def test_retrait_qualificateur_unique_est_detectable():
    """Un qualificateur porté par un seul lien devient orphelin quand
    on le retire : présent au registre, atteint par rien."""
    reg, V = registre()
    lien = [V("belle"), V("T1"), V("JS")]
    V("Sarah").links.append(lien)
    V("autre").links.append([V("chose"), V("T1")])   # T1 partagé, JS non
    assert examiner(reg)["intact"], "graphe sain au départ"

    lien.pop()          # <- retrait de JS

    assert "JS" in orphelins(reg), "JS n'est plus atteint par rien"
    print("✓ retrait d'un qualificateur unique : orphelin détecté")


def test_retrait_qualificateur_partage_echappe():
    """LA LIMITE. Si le qualificateur est porté ailleurs, son retrait
    d'un lien ne laisse aucune trace structurelle. L'affirmation
    devient anonyme et rien ne le signale."""
    reg, V = registre()
    lien = [V("belle"), V("T1"), V("JS")]
    V("Sarah").links.append(lien)
    V("Eva").links.append([V("douce"), V("T1"), V("JS")])   # JS partagé

    lien.pop()          # <- retrait de JS chez Sarah seulement

    assert examiner(reg)["intact"], "aucune anomalie : la limite est réelle"
    assert len(V("Sarah").links[0]) == 2, "l'affirmation est devenue anonyme"
    print("✓ retrait d'un qualificateur partagé : INDÉTECTABLE (limite assumée)")


def test_le_partage_rend_la_dissimulation_couteuse():
    """Ce qui reste vrai malgré la limite : plus le graphe partage,
    plus une suppression a de chances de rompre quelque chose."""
    reg, V = registre()
    # un qualificateur très partagé : le retirer partout serait visible
    for i in range(20):
        V(f"mot{i}").links.append([V(f"cible{i}"), V("SOURCE")])
    assert examiner(reg)["intact"]

    # retirer SOURCE d'un seul lien : indétectable
    V("mot0").links[0].pop()
    assert examiner(reg)["intact"], "un retrait isolé passe"

    # le retirer de TOUS : SOURCE devient orphelin
    for i in range(1, 20):
        V(f"mot{i}").links[0].pop()
    assert "SOURCE" in orphelins(reg), "l'effacement complet se voit"
    print("✓ effacer un qualificateur partout devient visible")


if __name__ == "__main__":
    test_suppression_de_noeud_est_detectable()
    test_retrait_qualificateur_unique_est_detectable()
    test_retrait_qualificateur_partage_echappe()
    test_le_partage_rend_la_dissimulation_couteuse()
    print()
    print("Le modèle ne protège pas. Il rend l'effacement coûteux à cacher —")
    print("d'autant plus coûteux que le graphe partage. Une limite subsiste,")
    print("et elle est écrite dans verifier.py plutôt que tue.")
