# reference-output/ — vendored gold-standard artifacts

These are shipped with the skill so it is self-contained (survives the source repo moving).

## `EXEMPLAR-PRD.md`

The **Agent Atelier PRD** (v4.4, ~2,755 lines / 64 pp) — the gold-standard output of this
skill. It is a product-agnostic, spec-driven PRD for an agentic multi-agent marketing-content
studio, generalized from a real 8-agent Instagram engine.

**Use it for:** studying the *quality bar, structure, section density, and voice* — bold
lead-ins, inline `§x.y` cross-refs, fenced Gherkin, conditional-YAML, a pinned data model
(§17), phased prompt-contracts (§19.1), build governance (§18.4), the live "Studio Floor"
operator console (§12.4), and the concept-map rubric (Appendix B).

**Do NOT** copy its domain content into a new PRD. It is one worked example; your product may
be anything. It also demonstrates the product-agnostic discipline — study how brand-specific
facts live in config/Appendix A, never in the generic body.

**A worked `/specs` + config model:** the skill vendors no filled `/specs` tree, but the
exemplar's own **Appendix D** (`EXEMPLAR-PRD.md`) is the worked reference for the roles / canon
/ policies / golden / config artifact set described generically in `references/sdd-skeleton.md`
Appendix D — model your own artifact set on it.

## `bunny-method/`

The four source files of the **BUNNY build-governance method** (from the collaborator "Teo") —
the *original v2 application artifacts* (a worked Agent-Atelier application of the method):

- `01_SPEC_DIGEST.md` — the spec digest / four-file overview.
- `02_PROMPT_CONTRACTS.md` — worked, filled-in prompt-contracts for the example build.
- `03_WRITEUP_SKELETON.md` — the submission/writeup skeleton (for course/competition PRDs).
- `04_BUILD_SEQUENCE.md` — the gated build sequence.

**The authoritative, current full text of the governance harness — including the tests-first
per-phase gate and the 10-field definitions — is `EXEMPLAR-PRD.md` §18.2 + §18.4 + §19.1–§19.2**,
not these four files (which pre-date the tests-first gate: `02` still says "generate
tests/docs/logging alongside features"). Read the four for extra worked detail and the writeup
skeleton, but where they disagree with the exemplar, the exemplar wins. Note these v2 originals
contain internal cross-references to sibling files by their *old* names (e.g. `02` cites
`01_AGENT_ATELIER_SPEC.md`, now vendored as `01_SPEC_DIGEST.md`) and to un-vendored source
sections — read them standalone. The operating summary is `references/bunny-governance.md`.
