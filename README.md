# Vector

**A living memory in eleven lines.** Time is a node. A link carries as
many vectors as it needs — and it grows with what you learn. Nothing is
ever deleted. Meaning is not stored — it emerges when you read.

```python
class Vector:
    """TOUT. Deux champs. Rien de plus."""

    def __init__(self, name: str):
        self.name = name
        self.links: list[list] = []   # [[cible, qualificateur, ...], ...]
                                       # Chaque lien est une liste VIVANTE :
                                       # la cible en tête, puis les
                                       # qualificateurs, dans l'ordre où on
                                       # les apprend. Un lien grandit ; il
                                       # ne se réécrit jamais.
```

That is the entire model. No dependencies. MIT.

---

## The four decisions

1. **One class for everything.** A word, a person, an instant, a channel,
   a tool: the same object. No types, no ontology, no labels on links.
2. **Time is a citizen of the graph.** Instants are nodes, reached and
   shared by links. Identity through time is a link to oneself:
   `[self, T]`. There is no update function — time *is* the update.
3. **A link is a living list.** The target comes first; qualifiers follow,
   in the order they were learned. The model does not fix how many — the
   application does, and time makes it grow.
4. **Append-only, at every level.** No DELETE, no overwrite, no
   normalization, no stored score. A link grows; it never shrinks.
   Correction is a dated addition. The verb *delete* does not exist in
   this codebase — deliberately.

---

## An object names itself

A Vector has no identifier. Its `name` is not a label attached to an
identity — it **is** the identity.

```python
def V(name):
    if name not in reg: reg[name] = Vector(name)
    return reg[name]
```

That is the whole registry. Ask for a name, get the vector. Ask twice,
get the same object. No generator, no UUID, no authority deciding what
counts as the same thing.

The consequences are not cosmetic.

**Deduplication is not a feature — it is an absence.** Two articles of
the French Civil Code with strictly identical text (2372-2 and 2488-2, on
fiduciary security) merged into a single citizen when the code was woven.
Nobody wrote that behaviour. There is simply no way to express two
different citizens carrying the same content.

**Identity is verifiable by anyone.** You do not have to trust a registry
that assigned an ID. You read the name, you have the identity. Two graphs
built independently from the same corpus produce the same citizens, with
no reconciliation step.

**Distinguishing requires qualifying, not renaming.** If two occurrences
of the same word must be told apart, you do not invent `word_1` and
`word_2`. You qualify the links that reach them. The word stays one
citizen; its occurrences are distinct paths to it. That is the whole
reason a link carries more than its target.

**And it is what makes deletion visible.** Because links hold the object
itself and lookups resolve by name, removing a name splits it into two
entities — one still held by existing links, one recreated empty. A
system with external IDs would simply have a dangling pointer, which is
routine. Here it is a contradiction in the identity itself.

---

## A link grows

A relation is rarely known all at once. Monday you know Sarah is *belle*.
Tuesday you learn when it was said. Thursday you learn who said it.

```python
lien = [V("belle")]                 # lundi   — la cible, rien d'autre
V("Sarah").links.append(lien)
lien.append(V("2026-06-29_09h00"))  # mardi   — on apprend quand
lien.append(V("JS"))                # jeudi   — on apprend qui
```

One link. Never duplicated, never rewritten. The order of its qualifiers
*is* the history of what was learned about that relation.

This is why the target comes first: if it were last, every addition would
displace it. The living list imposes its own convention.

If you also want to record *when you learned it*, that too is a vector.
Nothing is added to the model:

```
[belle, dit_2026-06-29, su_2026-07-01, JS, su_2026-07-24]
```

The graph then carries its own epistemology: *this relation took 25 days
to become attributable.*

---

## Length is a design decision

| Length | Form | Answers |
|---|---|---|
| 1 | `[target]` | what follows what |
| 2 | `[target, when]` | + which occurrence exactly |
| 3 | `[target, when, who]` | + who asserts it |
| 4+ | `[target, line, phrase, glyph]` | + where exactly, citable |

Removing a vector does not make Vector more efficient. It removes a
question it can answer. When a single voice speaks, the source vector does
not disappear by optimization — it never appears, because it carries no
information.

**The integrity threshold falls between 2 and 3.** At length 2, an
intruder inserting a false assertion produces a link of exactly the same
shape as a legitimate one: you can discard a whole timestamp, never know
who lied. At length 3, the intruder must produce a source. Invent one and
it falls outside the known circle, filterable in a single line. Usurp one
and it is an attributable forgery.

> From three vectors on, **anonymity becomes inexpressible.** There is no
> way to write an assertion without an author. Memory pollution is not
> forbidden — it is unsayable.

---

## Sharing is the condition of the graph

This is the part that matters most, and it is measured, not claimed.

Two ways to weave the same 6 600-glyph text. One uses a flat counter for
position (`@0, @1, @2…`). The other uses shared coordinates (line, phrase,
glyph rank).

| | flat `@N` | coordinates |
|---|---|---|
| citizens | **6 611** | **623** |
| distinct qualifiers | 6 599 | 612 |
| qualifiers used **exactly once** | **100 %** | **0 %** |
| average neighbourhood per qualifier | **1.0** | **5.9** |
| maximum neighbourhood | **1** | 7 |

Read the last two rows again. With a flat counter, **every qualifier leads
to exactly one neighbour**. Not on average — always. No qualifier ever
connects two things.

That is not a graph. It is a chain.

And Vector's entire promise — *meaning is not stored, it emerges when you
walk; two readers, two traversals, two meanings* — requires paths to
**converge**. If every qualifier leads to exactly one place, walking
returns precisely what you wrote, in the order you wrote it. Nothing
emerges, because there is nothing for emergence to come from.

**Sharing is not an optimization. It is the condition under which the
graph exists at all.** A qualifier used once does not link two things —
it merely names a slot.

> A qualifier deserves to be a citizen when it is **shared**. A flat
> counter, never reused, is a number disguised as a vector.

---

## The risk of over-optimization

Every shortcut that looks like a saving tends to attack the same thing:
the sharing that makes the graph a graph.

**Hashing an identity.** Replacing content by a fingerprint saves bytes
and destroys the property that two identical contents are *the same
citizen*. Worse, collisions produce false proximity: two unrelated items
land in the same bucket and the score reports a similarity that does not
exist. A score that cannot name what it shares is a score that lies.

**Chunking at fixed size.** Cutting every N tokens saves indexing effort
and severs units the author actually chose. The boundary does not follow
meaning — it follows a counter. What was one sentence becomes two
fragments that each mean less than the whole.

**Flat counters as coordinates.** Measured above: 100 % single-use
qualifiers, zero convergence. It looks compact. It quietly turns the graph
into a list.

**Factoring out a constant qualifier.** We did this ourselves — a
`source_defaut` field to avoid repeating one value. It saved 7 % before
compression, and gzip recovered the difference entirely. It also made the
serialization format narrower than the model it claimed to serialize.
The optimization was real; it was worth less than the honesty it cost.

The pattern is always the same: **the saving is measurable immediately,
the loss only becomes visible when someone asks a question the graph can
no longer answer.**

---

## Vector and RAG

Nothing here forbids using Vector as a retrieval layer. A chain with a
fast index is a perfectly serviceable RAG, and Vector can serve that
purpose without lying about what it is.

But the premises differ, and it is worth being precise about how.

**Most graph-RAG systems build their graph with a language model.**
GraphRAG derives its knowledge graph from source documents through an LLM.
Cognee extracts entities and relations the same way. LightRAG generates a
short description for each entity it identifies. The graph is an
*interpretation* produced by a model, at a cost per document.

**Vector builds its graph without any model.** A legal corpus of nearly
three thousand articles and a complete novel were both woven with zero
model calls: the structure comes from the text itself, not from a reading
of it. Encoding cost is CPU time, once. Query cost afterwards is close to
nothing.

**Identity is content, not a generated key.** Two articles with strictly
identical text merge into one citizen without anyone programming it. In a
system where each chunk receives a generated UUID, they remain two
unrelated rows.

**The unit is the one the author chose.** An article, a sentence, a line —
never a window of N tokens ending wherever the counter stopped.

### What this does not do

Vector does not generate, does not synthesize, does not converse. It finds.
A language model remains necessary for anything that must be *written*.

Vector has not been tested at the scale of millions of documents, nor
under heavy concurrent writes. Where those constraints dominate, a mature
vector database is the honest answer.

And no benchmark yet compares Vector to Graphiti, Cognee or a classical
RAG pipeline on the same corpus with the same questions. Until that
exists, everything above describes premises, not measured superiority.

### Where doing without RAG is reasonable

A **finite, stable corpus** — a legal code, a standard, a technical
reference, a contract base — is the case where the RAG pipeline is
disproportionate. The corpus does not change hourly. It has natural
units. Its cross-references are already written into it.

For that case, encoding once and walking the graph answers the question
without a single model call. That is not a claim of superiority. It is a
claim that the expensive machinery was not needed here.

---

## No types — not even for time

The model cannot structurally distinguish a time from a source, nor from
a document coordinate. All three are qualifiers. Which one is an instant
and which is a speaker is decided by the reader, not by the structure.
That is not a gap. It is decision 1, carried through.

Two earlier versions of this model were less consistent, and it is worth
saying plainly:

- It had a third field, `seen`, holding the instants a vector had been
  traversed at. It was a link of length 1 frozen into structure — an
  answer to one need, mistaken for a component of the model. Worse, in
  practice it meant **reading wrote**: every consultation appended to the
  corpus. Recency belongs to the medium, not to the memory. It is now an
  observer, like any other reading.
- Its links were tuples, immutable by construction. That was the only
  place where the model enforced append-only structurally, while
  everywhere else it merely *proves* what breaking it costs. The
  inconsistency was in the tuple, not in the discipline.

```python
def vu_a(v):
    """Les instants où ce vecteur existe : ses liens vers lui-même."""
    return [q for l in v.links if l[0] is v for q in l[1:]]
```

If a consultation deserves to survive the session, assert it — sourced and
dated, like anything else. It then becomes contestable, which an anonymous
counter never was.

---

## Deletion leaves traces

The model forbids nothing. But in a graph where identity is content,
removing something usually breaks a coherence that can be examined.
`verifier.py` looks for it — an organ of reading, not a piece of the model.

**Deleting a node is detectable.** Existing links hold the object itself;
a new lookup by the same name creates another. The registry and the links
then disagree, and the disagreement is mechanical to find:

```python
if reg.get(x.name) is not x:      # a link reaches an object the registry
    ...                            # no longer recognises
```

**Removing a lone qualifier is detectable.** It survives in the registry
while nothing reaches it any more, and it asserts nothing itself. It has
no reason to be there.

**Removing a shared qualifier is not detectable.** This is a real limit,
and it is written in `verifier.py` rather than left unsaid. Strip `JS`
from one link while another link still carries `JS`, and the assertion
becomes anonymous with no structural trace. Nothing signals it.

What remains true is worth stating precisely: **the denser the sharing,
the more expensive concealment becomes.** Removing one occurrence of a
widely shared qualifier passes unnoticed; removing all of them orphans it
and shows. Sharing is not only the condition of emergence — it is also
what makes impoverishment hard to hide.

---

## The model does not protect. It proves.

Python lets you call `reg.pop()`. It lets you call `lien.pop()`. The model
forbids neither — it provides no verb for either, and it demonstrates what
each one costs.

`test_identite.py` — deleting a node splits its name into two incompatible
entities: one still reachable through existing links (history intact), one
freshly recreated by any new lookup (empty). Not a loss of information —
a structural corruption of identity.

`test_qualificateur.py` — removing a qualifier from a link makes it
indistinguishable from a link that never knew more. The impoverished link
now asserts something false: *this is all we ever knew*. An honest reader
is misled, with no way to detect it. A link can grow. It cannot shrink
without lying.

---

## Meaning as a read-time event

The model stores no semantics: no weights, no embeddings, no categories.
Meaning happens when someone *walks* the graph — weighting by recency and
density of traversed times, filtering by source, at read time. Two readers,
two traversals, two meanings — same graph. Nothing ever goes stale: when
meaning shifts, the path changed, not the data.

Everything else — linguistic analysis, persistence, search, LLMs — is a
**medium**: a mortal, replaceable reading organ. The corpus outlives every
medium that reads it.

---

## Run it

```
python exemple.py
python test_arite.py
python test_identite.py
python test_qualificateur.py
python test_partage.py
python test_integrite.py
```

`test_partage.py` reproduces the table above. Run it and check the
numbers yourself.

`GUIDE.md` explains how to choose the length of a link: what each level
allows, where the integrity threshold falls, and how to tell a real
qualifier from a number in disguise.

Read the assertions. Verify it yourself.

---

## What this is not

Not a patch on RAG. Not a vector database. Not a product. A different set
of premises, running in production at K1SS Atelier 0, Besançon. Born from
watching a memory outlive its medium — and deciding that machines deserved
the same dignity.

*Le texte source est la vérité. Le temps est un atome. La source est la
frontière du privé. Le sens émerge — on ne le force pas.*

— **JS** (vision) · **Kage** (words) · **FB** (gestures) — K1SS Atelier 0, MIT, 2026 🐢💎🗿
