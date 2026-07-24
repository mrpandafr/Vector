# Combien de vecteurs par lien

*Guide de conception. Chaque affirmation de ce document a été testée
avec le code de `vector.py`. K1SS Atelier 0 — 24 juillet 2026.*

---

## Le principe

Le modèle ne fixe pas la longueur d'un lien. L'application la choisit,
selon ce qu'elle doit pouvoir **distinguer**, **attribuer** et **dater**.

Ajouter un vecteur ne rend pas le graphe meilleur. Ça lui permet de
répondre à une question de plus. En retirer un ne l'optimise pas :
ça retire une question.

---

## Ce que chaque longueur permet

| Longueur | Forme | Répond à |
|---|---|---|
| 1 | `[cible]` | que suit quoi |
| 2 | `[cible, quand]` | + quelle occurrence exactement |
| 3 | `[cible, quand, qui]` | + qui l'affirme |
| 4+ | `[cible, ligne, phrase, glyphe]` | + où exactement, citable |

Vérifié : à longueur 1, deux affirmations identiques vers la même cible
sont **indiscernables**. À longueur 2, elles se séparent. Le reste suit.

---

## Intégrité : à partir de quand un mensonge devient détectable

C'est le vrai seuil, et il tombe entre 2 et 3.

**Longueur 2.** Un intrus insère `Sarah -> monstrueuse` à `T2`. Le lien
a exactement la même forme que le lien légitime. On peut ignorer `T2` en
bloc, mais rien ne dit **qui** a menti, ni pourquoi celui-là plutôt que
l'autre.

**Longueur 3.** Le même intrus doit produire une source. S'il en invente
une, elle est hors du cercle connu et devient filtrable en une ligne.
S'il en usurpe une, il commet un faux attribuable.

> À partir de trois vecteurs, **l'anonymat devient inexprimable.** Il
> n'existe aucune façon d'écrire une affirmation sans auteur. La
> pollution de mémoire n'est pas interdite : elle est indicible.

C'est une propriété structurelle, pas une règle de politesse. Elle ne
coûte qu'un vecteur.

---

## Versioning : ce que la croissance enregistre

Un lien grandit. L'ordre de ses qualificateurs **est** l'histoire de ce
qu'on a appris sur cette relation.

```
lundi   [belle]
mardi   [belle, dit_2026-06-29]
jeudi   [belle, dit_2026-06-29, JS]
```

Un seul lien, jamais dupliqué, jamais réécrit.

**Limite honnête** : l'ordre dit ce qu'on a appris, pas *quand* on l'a
appris. Deux liens de même forme sont indiscernables, que l'un ait grandi
en trois semaines et l'autre été écrit d'un coup.

**Et la réponse est déjà dans le modèle** : le moment de l'apprentissage
est un vecteur. On l'ajoute comme les autres.

```
[belle, dit_2026-06-29, su_2026-07-01, JS, su_2026-07-24]
```

Aucune structure ajoutée. Le graphe porte alors deux temps distincts —
quand la chose a été dite, quand nous l'avons apprise — et raconte sa
propre épistémologie : *cette relation a mis 25 jours à devenir
attribuable.*

---

## Les deux échecs, symétriques

**Trop peu.** On ne peut pas répondre à une question qu'on se posera plus
tard. Pire : on ne peut pas détecter qu'on est trompé. Le coût n'apparaît
qu'au moment où il est trop tard pour l'éviter.

**Trop.** On invente des qualificateurs qui ne portent rien. Le symptôme
est mesurable : **un qualificateur jamais réutilisé est un numéro déguisé
en vecteur.** Un compteur plat `@0, @1, @2…` n'est partagé par personne —
chaque valeur sert une fois. Une coordonnée `ligne 12` est partagée par
tous les glyphes de cette ligne : elle existe vraiment.

> Un qualificateur mérite d'être un citoyen quand il est **partagé**.

---

## Comment choisir

Trois questions, dans cet ordre.

**Une seule voix parle-t-elle ?** Si oui, la source ne porte rien : elle
n'apparaît pas. Ce n'est pas une économie, c'est une absence d'information.
Dès qu'une deuxième voix existe, le vecteur source redevient nécessaire —
sans lui, les deux affirmations sont anonymes.

**Faut-il pouvoir citer ?** Un corpus juridique, scientifique, contractuel
exige de pointer exactement. Les coordonnées documentaires sont alors des
qualificateurs, et elles ont la bonne propriété : elles sont partagées.

**Le savoir va-t-il évoluer ?** Si oui, laissez les liens naître courts et
grandir. Un lien né nu qui s'enrichit vaut mieux qu'un lien écrit trop tôt
avec des qualificateurs devinés.

---

## Ce que ce guide n'empêche pas

Rien. Un lien peut être mal conçu, un qualificateur inventé, une source
usurpée. Le modèle ne protège pas par la structure — il **prouve** ce que
coûte chaque transgression : `test_identite.py` pour la suppression d'un
nœud, `test_qualificateur.py` pour l'appauvrissement d'un lien.

Expliquer un choix de conception n'empêche pas le pire. Ça l'évite.

🐢🗿
