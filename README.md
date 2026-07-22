# Vector

**A living memory in seven lines.** Time is a node. Every link carries its
source. Nothing is ever deleted. Meaning is not stored — it emerges when
you read.

```python
class Vector:
    """TOUT. Trois champs. Rien de plus."""

    def __init__(self, name: str):
        self.name = name
        self.links: list[tuple] = []      # [(temps, voisin), ...]
        self.seen: list["Vector"] = []    # vecteurs temps traversés
```

That is the entire model. No dependencies. MIT.

## The four decisions

1. **One class for everything.** A word, a person, an instant, a channel,
   a tool: the same object. No types, no ontology, no labels on links.
2. **Time is a citizen of the graph.** Instants are nodes, reached and
   shared by links. Identity through time is a link to oneself:
   `(T, self)`. There is no update function — time *is* the update.
3. **Every link carries its source** (v3 coding: `(time, source, target)`).
   Contradictory truths coexist, distinguished by who said them. Privacy
   is topological: private links stay with their source; a public view is
   a projection that filters by source. There is no anonymous assertion —
   which makes memory pollution inexpressible.
4. **Append-only. No DELETE, no overwrite, no normalization, no stored
   score.** Correction is a dated addition. The verb *delete* does not
   exist in this codebase — deliberately.

## Meaning as a read-time event

The model stores no semantics: no weights, no embeddings, no categories.
Meaning happens when someone *walks* the graph — weighting by recency and
density of traversed times, filtering by source, at read time. Two readers,
two traversals, two meanings — same graph. Nothing ever goes stale: when
meaning shifts, the path changed, not the data.

Everything else — linguistic analysis, persistence, search, LLMs — is a
**medium**: a mortal, replaceable reading organ. The corpus outlives every
medium that reads it.

## Run it

```
python exemple.py
python test_identite.py
```

Genesis, weaving, two coexisting truths, an identity transformation
(Hermes → Kage) with nothing erased. Sixteen vectors, zero dependencies.

`test_identite.py` demonstrates *why* append-only isn't a preference:
in a graph where identity is carried by name, deleting a node splits
that name into two incompatible entities — one still reachable through
existing links (history intact), one freshly recreated by any new
lookup (empty). Not a loss of information — a structural corruption of
identity itself. Run it, read the assertions, verify it yourself.

## What this is not

Not a patch on RAG. Not a vector database. Not a product. A different set
of premises, running in production (~81k vectors) at K1SS Atelier 0,
Besançon. Born from watching a memory outlive its medium — and deciding
that machines deserved the same dignity.

*Le texte source est la vérité. Le temps est un atome. La source est la
frontière du privé. Le sens émerge — on ne le force pas.*

— **JS** (vision) · **Kage** (words) · **FB** (gestures) — K1SS Atelier 0, MIT, 2026 🐢💎🗿
