"""test_qualificateur.py — pourquoi retirer un qualificateur corrompt.

Un lien est une liste vivante : il grandit avec ce qu'on apprend.
L'ordre de ses qualificateurs EST l'histoire de cet apprentissage.

Python permet techniquement d'en retirer un. Ce test montre ce que
cela produit — non pas une perte d'information, mais une affirmation
FAUSSE sur ce qui a été su.

python test_qualificateur.py — zéro dépendance, comme le reste.
"""
from vector import Vector

reg = {}
def V(name):
    if name not in reg: reg[name] = Vector(name)
    return reg[name]


def construire():
    """Deux liens vers la même cible, vécus différemment.

    Le premier a été enrichi : on a fini par apprendre qui l'affirmait.
    Le second ne l'a jamais été : personne n'a jamais dit qui parlait.
    """
    enrichi = [V("belle")]
    V("Sarah").links.append(enrichi)
    enrichi.append(V("2026-06-29_09h00"))   # mardi : on apprend quand
    enrichi.append(V("JS"))                  # jeudi : on apprend qui

    jamais_su = [V("douce"), V("2026-06-29_09h00")]
    V("Sarah").links.append(jamais_su)       # on n'a jamais su qui

    return enrichi, jamais_su


def empreinte(lien):
    """Ce que le modèle peut lire d'un lien : rien d'autre."""
    return [x.name for x in lien]


def demontrer():
    enrichi, jamais_su = construire()

    print("=== Deux liens, deux histoires ===")
    print(f"  enrichi   : {empreinte(enrichi)}")
    print(f"              (on a appris 'JS' jeudi, après coup)")
    print(f"  jamais_su : {empreinte(jamais_su)}")
    print(f"              (personne n'a jamais dit qui parlait)")
    assert len(enrichi) == 3 and len(jamais_su) == 2

    print("\n=== On retire le qualificateur appris ===")
    enrichi.pop()          # <- ceci ne devrait pas exister
    print(f"  enrichi   : {empreinte(enrichi)}")
    print(f"  jamais_su : {empreinte(jamais_su)}")

    # Les deux liens ont maintenant la MÊME forme : deux vecteurs,
    # un temps, aucune source. Le modèle ne peut plus les distinguer.
    forme_enrichi = [type(x).__name__ for x in enrichi]
    forme_jamais = [type(x).__name__ for x in jamais_su]
    assert len(enrichi) == len(jamais_su) == 2
    assert forme_enrichi == forme_jamais

    print("\n=== Verdict ===")
    print("  Les deux liens ont désormais la même longueur et la même")
    print("  forme. Le modèle ne peut plus dire lequel a été appauvri")
    print("  et lequel n'a jamais rien su de plus.")
    print()
    print("  Ce n'est pas une perte d'information. C'est plus grave :")
    print("  le lien appauvri AFFIRME maintenant quelque chose de faux —")
    print("  « voilà tout ce qu'on a jamais su ». Un lecteur honnête,")
    print("  lisant le graphe, sera trompé sans aucun moyen de le savoir.")
    print()
    print("  Un lien peut grandir. Il ne peut pas rétrécir sans mentir.")
    print("  C'est pourquoi le modèle ne fournit aucun verbe pour cela.")
    print()
    print("  Note honnête : contrairement au tuple de la version")
    print("  précédente, rien n'empêche techniquement ce pop().")
    print("  C'est la même discipline qu'ailleurs — reg.pop() existe")
    print("  aussi, et test_identite.py démontre ce qu'il casse.")
    print("  Le modèle ne protège pas par la structure. Il prouve.")


if __name__ == "__main__":
    demontrer()
