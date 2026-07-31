# BUNNY build governance — make the build executable, gated, and honest

The BUNNY method (originated by the collaborator "Teo") is the harness that turns a spec into
a *buildable* spec. A PRD that describes a product but not how to build it safely is only half
done. Every forge-prd PRD must encode this governance.

The method is **universal to any PRD** — it does not depend on the product being agentic.

**Authoritative full text:** `reference-output/EXEMPLAR-PRD.md` **§18.2** (the per-contract
build loop) + **§18.4** (the harness) + **§19.1** (the nine gated prompt-contracts) + **§19.2**
(critical-path notes). That is the current, canonical encoding — including the tests-first gate
— and this file is its operating summary.

Each contract runs through the **§18.2 build loop** (once per contract): Architect → Builder →
test-first → CI eval gate → security → review, under a **no-YOLO** posture (the builder
proposes the folder structure + pinned stack for the owner to confirm *before* executing).

**The four vendored `reference-output/bunny-method/01–04` files** are the *original v2
application artifacts* (a worked spec digest, filled contracts, a writeup skeleton, a build
sequence). Read them for extra worked detail and the submission/writeup skeleton — but note
they **pre-date the tests-first per-phase gate** (`02` still says "generate tests/docs/logging
alongside features", which §3 below supersedes with tests-*first*, red→green). **Where the vendored
files and the exemplar/this summary disagree, the exemplar wins.**

---

## 1. The 10-field prompt-contract (per build unit)

Every unit of build work — **a phase, or a slice of a phase** — is specified as a contract
with these ten fields. This is what a spec-driven builder executes, and what its work is
judged against:

| Field | What it pins |
|---|---|
| **INTENT** | why this unit exists — the outcome, in one line |
| **SCOPE** | exactly what is in this unit |
| **NON-GOALS** | what this unit deliberately does not do (prevents scope creep) |
| **INPUTS** | the artifacts/state this unit consumes |
| **INVARIANTS** | what must remain true throughout — separation of concerns, fail-closed safety, idempotency, secrets-never-in-prompts, data integrity |
| **ACTION** | the work to perform |
| **ACCEPTANCE** | the exit criterion — *this is the roadmap gate*, authored as an executable test suite (see §3) |
| **VERIFY** | how acceptance is proven — **evidence, not assertion** (a passing test, a captured artifact, a real run) |
| **AUTHORIZATION** | who authorizes the *next* unit to open (a forward release) — a role **distinct** from the Executor who did the work and the Validator who certified the VERIFY evidence |
| **ON-FAIL** | the pre-declared fallback if the unit cannot complete as specified |

Turn the phased roadmap into a sequence of these contracts, blockers first.

## 2. Validator / Executor / Authorizer separation

No single actor both does the work and certifies it. The **Executor** performs the ACTION.
A **Validator** checks the VERIFY evidence exists and is real. An **Authorizer** (a distinct
role) grants the lock that opens the next phase. **High-stakes or irreversible changes**
(enabling auto-publish, canon/schema edits, other foundational flips) require an *elevated*
authorization bar — a stronger human diff-review / sign-off above the normal per-phase
authorization. This is what keeps "report-is-not-the-repo" honest — the certification is
independent of the claim.

## 3. Tests-first, per-phase gate (the phase gate is a green suite, not a judgment call)

This is the discipline that makes phases deterministic:

- Each phase's **ACCEPTANCE** (its Gherkin scenarios) is authored as that phase's
  **executable test suite BEFORE the phase's code is generated** (red → green).
- The phase **GATE** is then deterministic: the phase is done when its test suite is green
  **AND** the CI evaluation gate passes. Not "looks done" — *is* green.
- Tests **accrue** into a growing regression suite that every later phase must keep green.
  No phase may regress a prior phase's suite.
- **Deterministic tests are the hard gate; the holistic LLM-as-judge stays advisory.** Where
  a check can be made observable, it is the gate; the judge informs but does not authorize.

## 4. Lock-and-proceed / verify-before-next

A phase **locks** when its VERIFY evidence exists and it is authorized; only then does the
next phase **open**. Gates are **checkpoints, not stopping lines** — the target is full
scope, and the gates sequence the work rather than truncate it. This prevents both premature
advancement (building on unverified foundations) and premature stopping (declaring victory at
the first gate).

## 5. Conscious-deviation logging

When the spec and the tool's ground truth disagree, **conform to the tool's ground truth,
then log the deviation** in `/specs/deviation_log.md` — never silently. The spec is
authoritative about intent, but reality is authoritative about mechanism; when they conflict,
reality wins *and gets recorded* so the spec can be reconciled.

## 6. ON-FAIL disciplines (the pre-declared fallbacks)

The universal rule is: **every contract carries a pre-declared, conformant ON-FAIL path.** The
five below are the *exemplar's* concrete fallbacks (an agentic build) illustrating the
mechanism — derive your own domain-appropriate fallbacks per PRD; don't copy these verbatim
into a non-agentic spec.

- **Don't-fake-MCP** — if an MCP server cannot be built as specified, fall back to the
  simplest *conformant* server; never a faked inline function pretending to be MCP.
- **Conform to the framework's actual shape** — build to what the framework really does, not
  what the spec wished it did (then log the deviation).
- **Keep the falsifiable gate** — if a soft/semantic gate is flaky, keep the hard/structural
  gate; do not let a flaky check silently pass everything.
- **Poll-based is the documented default** — prefer the simple, observable mechanism unless
  the spec justifies more.
- **Manual handoff is the unaffected default** — if automation of a handoff fails, the manual
  path still works; automation is additive, never load-bearing for safety.

## 7. Grounding disciplines (honesty over convenience)

- **Report-is-not-the-repo** — a claim of completion is not completion; only VERIFY evidence
  in the actual artifacts counts.
- **Fail-closed** — when a safety-critical input is missing/unconfirmed, block and route to a
  human; never proceed on an empty safety field.
- **Honest-refusal over silent fallback** — if a unit cannot be done correctly, say so; do
  not quietly substitute something weaker and report success.
- **Verify against LIVE docs at build time** — model IDs, API limits, library versions: only
  a live 404 proves a model absent. Confirm at build time, not from memory.
- **Supply-chain hygiene** — verify and pin dependencies; do not pull unpinned/unknown code.

---

## How to encode BUNNY in a PRD

1. A **§18.4-style "build governance" subsection** stating the method: the contract shape,
   the role separation, the tests-first gate, the deviation log, the ON-FAIL/grounding
   disciplines.
2. A **§19.1-style "phased roadmap as gated prompt-contracts"** — the actual build sequence,
   each build unit a filled-in 10-field contract, blockers first, each with a concrete VERIFY
   and a tests-first ACCEPTANCE suite. A load-bearing phase may be **split into multiple
   contracts** (the exemplar splits P1 into P1-A *agents* and P1-B *pipeline+MCP* because
   "MCP becomes real" is the load-bearing slice — §19.2).
3. The **`/specs/contracts/`** directory (the filled 10-field prompt-contracts, one per build
   unit — durable *inputs*, not regenerated output) and the **`/specs/deviation_log.md`** file,
   both stubbed in the artifact set (Appendix D of the skeleton).

The BUNNY source files (`reference-output/bunny-method/`) also include a **writeup skeleton**
(03) for packaging a submission and a **build sequence** (04) — use them when the PRD targets
a course/competition.
