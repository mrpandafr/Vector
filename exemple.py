"""Première traversée — le modèle Vector exécuté, zéro dépendance.
python exemple.py
"""
from vector import Vector

reg = {}
def V(name):
    if name not in reg: reg[name] = Vector(name)
    return reg[name]

def tisser(sujet, mots, source, T):
    """v3 : la chaîne part du sujet ; chaque lien porte (temps, source, cible)."""
    prec = V(sujet)
    for mot in mots:
        m = V(mot)
        prec.links.append((T, V(source), m))
        m.seen.append(T)
        prec = m

# Genèse : le premier temps est un Vector, le premier JE s'auto-lie.
t0 = V("2026-06-16_09h00"); moi = V("Hermes")
moi.links.append((t0, moi)); moi.seen.append(t0)

# Deux vérités coexistent — distinguées par la source dans le lien.
tisser("Sarah", ["est", "belle"],  "JS", V("2026-06-29_09h00"))
tisser("Sarah", ["est", "froide"], "FB", V("2026-07-12_23h00"))

# Transformation d'identité : reconfiguration, jamais suppression.
Tk = V("2026-07-12_20h00"); kage = V("Kage")
kage.links.append((Tk, kage))       # nouveau JE
kage.links.append((Tk, moi))        # lien vers ce qu'il fut — rien d'effacé

for (T, src, cible) in V("Sarah").links:
    print(f"{T.name} · {src.name} dit : Sarah -> {cible.name}")

# FB: comptage STRUCTUREL des temps-atomes — un temps est un Vector qui
# apparaît en première position d'au moins un tuple de lien, jamais un
# Vector reconnu par la forme de son nom (l'ancien `n[:2]=='20'` était
# une convention de démo, pas un mécanisme du modèle : un mot pourrait
# légitimement commencer par "20" et serait alors compté à tort).
temps_atomes = set()
for v in reg.values():
    for lien in v.links:
        temps_atomes.add(lien[0].name)      # premier élément de tout tuple = temps

print(f"{len(reg)} vecteurs, dont {len(temps_atomes)} temps-atomes.")
print("Aucun DELETE possible : le verbe n'existe pas.")
