"""Première traversée — le modèle Vector exécuté, zéro dépendance.
python exemple.py

Deux champs : un nom, des liens.
Un lien est une liste vivante : la cible en tête, puis les
qualificateurs, dans l'ordre où on les apprend. Il grandit avec ce
qu'on découvre — il ne se réécrit jamais.
"""
from vector import Vector

reg = {}
def V(name):
    if name not in reg: reg[name] = Vector(name)
    return reg[name]

def lier(sujet, cible):
    """Crée un lien neuf, sans qualificateur, et le retourne pour
    qu'on puisse l'enrichir plus tard. Un lien par affirmation :
    jamais le même objet-liste partagé entre deux sujets."""
    lien = [V(cible)]
    V(sujet).links.append(lien)
    return lien

def qualifier(lien, *noms):
    """Ajoute ce qu'on vient d'apprendre. Rien n'est réécrit."""
    for n in noms:
        lien.append(V(n))
    return lien


# ── Un lien naît nu, et grandit ───────────────────────────────────
# Lundi on sait seulement que Sarah est belle. Mardi, quand. Jeudi,
# qui l'a dit. Un seul lien, jamais dupliqué, jamais réécrit.
l = lier("Sarah", "belle")
qualifier(l, "2026-06-29_09h00")
qualifier(l, "JS")

# ── Deux vérités coexistent, distinguées par leur source ──────────
qualifier(lier("Sarah", "froide"), "2026-07-12_23h00", "FB")

# ── Une coordonnée documentaire : trois qualificateurs ────────────
qualifier(lier("aime", "Denis"), "L0", "p1", "g2")

# ── Une transition nue : la cible suffit ──────────────────────────
lier("Alice", "court")

# ── Identité à travers le temps : un lien vers soi ────────────────
# Pas un mécanisme du modèle, un usage : exister à un instant, c'est
# se lier à soi-même à cet instant. Pas de fonction update — le temps
# EST la mise à jour.
qualifier(lier("Hermes", "Hermes"), "2026-06-16_09h00")
qualifier(lier("Kage", "Kage"), "2026-07-12_20h00")     # un nouveau JE
qualifier(lier("Kage", "Hermes"), "2026-07-12_20h00")   # lié à ce qu'il fut


# ── Observateurs : rien n'est stocké, tout se lit ─────────────────

def cible(lien):      return lien[0]
def qualificateurs(lien): return lien[1:]

def vu_a(v):
    """Les instants où ce vecteur existe : ses liens vers lui-même.
    Un observateur, pas un champ."""
    return [q for l in v.links if cible(l) is v for q in qualificateurs(l)]

def tous_qualificateurs(reg):
    """Tout Vector apparaissant ailleurs qu'en tête d'un lien.
    Le modèle ne distingue pas un temps d'une source ni d'une
    coordonnée : tous qualifient. C'est le lecteur qui tranche —
    la structure n'a pas de types."""
    return {q.name for v in reg.values() for l in v.links for q in qualificateurs(l)}


for l in V("Sarah").links:
    q = " · ".join(x.name for x in qualificateurs(l))
    print(f"{q} dit : Sarah -> {cible(l).name}")

print()
for nom in ("Alice", "Sarah", "aime"):
    print(f"  '{nom}' : {len(V(nom).links)} lien(s), "
          f"longueur(s) {sorted(len(l) for l in V(nom).links)}")

print()
print(f"{len(reg)} vecteurs, dont {len(tous_qualificateurs(reg))} qualificateurs.")
print(f"'Hermes' existe à : {[t.name for t in vu_a(V('Hermes'))]}")
print("Aucun DELETE possible : le verbe n'existe pas.")
