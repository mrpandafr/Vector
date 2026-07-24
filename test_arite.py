"""test_arite.py — un lien porte 1 à n vecteurs, et il grandit.

Le modèle ne fixe pas combien de vecteurs qualifient une relation.
L'application le décide, selon ce qu'elle doit pouvoir distinguer —
et ce qu'elle sait aujourd'hui n'est pas ce qu'elle saura demain.

python test_arite.py — zéro dépendance, comme le reste.
"""
from vector import Vector

def registre():
    reg = {}
    def V(name):
        if name not in reg: reg[name] = Vector(name)
        return reg[name]
    return reg, V


def test_longueurs_libres():
    """Plusieurs longueurs coexistent sur le même vecteur."""
    reg, V = registre()
    a = V("Alice")
    a.links.append([V("court")])                                    # 1
    a.links.append([V("vite"), V("T1")])                             # 2
    a.links.append([V("loin"), V("T2"), V("JS")])                    # 3
    a.links.append([V("bien"), V("L0"), V("p1"), V("g2")])           # 4

    assert [len(l) for l in a.links] == [1, 2, 3, 4]
    assert [l[0].name for l in a.links] == ["court", "vite", "loin", "bien"]
    print("✓ longueurs 1 à 4 coexistent ; la cible est toujours en tête")


def test_un_lien_grandit():
    """Un lien né nu s'enrichit sans jamais être réécrit ni dupliqué."""
    reg, V = registre()
    lien = [V("belle")]
    V("Sarah").links.append(lien)
    etapes = [len(lien)]

    lien.append(V("T1"));  etapes.append(len(lien))
    lien.append(V("JS"));  etapes.append(len(lien))
    lien.append(V("fr"));  etapes.append(len(lien))

    assert etapes == [1, 2, 3, 4], "le lien a grandi à chaque découverte"
    assert len(V("Sarah").links) == 1, "un seul lien, jamais dupliqué"
    assert lien[0].name == "belle", "la cible n'a pas bougé"
    print("✓ un lien grandit : 1 → 4, sans duplication, cible immobile")


def test_cible_en_tete_est_necessaire():
    """Si la cible était en dernier, chaque ajout la déplacerait.
    La liste vivante impose sa propre convention."""
    reg, V = registre()
    lien = [V("belle")]
    V("Sarah").links.append(lien)
    for q in ("T1", "JS", "fr", "certain", "v2"):
        lien.append(V(q))
        assert lien[0].name == "belle", "la cible reste en position 0"
    print("✓ cible en tête : cinq ajouts, elle n'a jamais bougé")


def test_une_seule_voix():
    """Quand une seule source parle, la nommer n'ajoute rien.
    Le qualificateur ne se retire pas par optimisation : il n'apparaît
    pas, parce qu'il ne porte aucune information."""
    reg, V = registre()
    for i, (mot, suiv) in enumerate([("Alice", "court"), ("court", "vite")]):
        V(mot).links.append([V(suiv), V(f"T{i}")])

    quals = {q.name for v in reg.values() for l in v.links for q in l[1:]}
    assert quals == {"T0", "T1"}, "aucune source répétée inutilement"
    print("✓ une seule voix : 2 vecteurs suffisent")


def test_plusieurs_voix():
    """Dès que deux sources parlent, le troisième vecteur redevient
    nécessaire : sans lui, les deux affirmations sont anonymes."""
    reg, V = registre()
    s = V("Sarah")
    s.links.append([V("belle"), V("T1"), V("JS")])
    s.links.append([V("froide"), V("T2"), V("FB")])

    assert {l[2].name for l in s.links} == {"JS", "FB"}
    print("✓ plusieurs voix : le 3e vecteur redevient nécessaire")


def test_longueur_1_ne_reconstruit_pas():
    """Avec la cible seule, un mot répété rend la trace ambiguë.
    L'émergence reste possible ; l'attestation, non."""
    reg, V = registre()
    V("Alice").links.append([V("aime")])
    V("aime").links.append([V("Bob")])
    V("Claire").links.append([V("aime")])
    V("aime").links.append([V("Denis")])

    sorties = [l[0].name for l in V("aime").links]
    assert sorties == ["Bob", "Denis"]
    assert len(set(sorties)) > 1, "deux suites possibles, indiscernables"
    print("✓ longueur 1 : l'émergence tient, la trace est perdue")


def test_longueur_2_reconstruit():
    """Un qualificateur qui situe suffit à lever l'ambiguïté."""
    reg, V = registre()
    V("aime").links.append([V("Bob"), V("@2")])
    V("aime").links.append([V("Denis"), V("@5")])

    par_position = {l[1].name: l[0].name for l in V("aime").links}
    assert par_position == {"@2": "Bob", "@5": "Denis"}
    print("✓ longueur 2 : chaque occurrence redevient distincte")


if __name__ == "__main__":
    test_longueurs_libres()
    test_un_lien_grandit()
    test_cible_en_tete_est_necessaire()
    test_une_seule_voix()
    test_plusieurs_voix()
    test_longueur_1_ne_reconstruit_pas()
    test_longueur_2_reconstruit()
    print("\nLe modèle ne fixe pas la longueur d'un lien.")
    print("L'application la choisit — et le temps la fait grandir.")
