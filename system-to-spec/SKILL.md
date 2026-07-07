---
name: system-to-spec
description: Use when extracting a portable spec, PRD, or blueprint FROM an already-working system — "replicate this elsewhere", "make it product-agnostic", "document this so another AI can rebuild it", migrating a working setup to another platform, or turning a one-off build into a reusable template.
---

# System to Spec

Reverse-engineer a *working* system into a spec portable enough that a different platform/AI can rebuild it. This is the Paperclip → Agent Atelier move. For net-new ideas (no working system yet), use **forge-prd** instead.

## Core Principle

**"The studio is constant; the brand is configuration."** The spec's central job is separating what is INVARIANT (roles, rules, flows, gates) from what is CONFIGURATION (the specific brand/product/user). Most extraction failures come from baking the current instance's specifics into the invariant layer.

## Extraction Method

1. **Behavior inventory first, code never.** Walk the running system's outputs, schedules, and artifacts. List every behavior as "when X, the system does Y, producing Z." Code is evidence, not the spec.
2. **Roles and handoffs.** Name each agent/component's mandate, inputs, outputs, and who consumes them (the report-is-not-the-repo rule: every stage's output is a durable artifact the next stage reads).
3. **Policies and gates.** Extract every approval gate, default-deny rule, escalation path, budget/circuit-breaker. These are usually implicit in the working system — interview the config and logs to find them. If the system genuinely has none, record "no gates" explicitly — absence is a finding, never invent gates that don't exist.
4. **Split invariant vs config.** For each behavior ask: "would a different product/brand change this?" Yes → config schema. No → spec body. Generalize exactly one product-swap deep: make configurable what the second imaginary product would need, nothing further — speculative abstraction is its own leak. Platform ties (launchd, Telegram) go in the intent doc as named constraints; behaviors reference the abstract role (scheduler, delivery channel).
5. **Deterministic rules become linters.** Anything checkable by rule (rotation, naming, format) gets written as a checkable rule, not prose — prose rules rot.
6. **Acceptance tests.** Write Gherkin scenarios for the behaviors that define "it works": the demo path, the failure path, one gate path.

## Output Format (three layers)

```
spec/
  00-intent.md        # what & why, invariants, roles, flows, policies (markdown)
  config.example.yaml # every configurable knob, flat YAML, commented
  acceptance/*.feature# Gherkin scenarios
```

## Fidelity Checks (before calling it done)

- **Cold-rebuild test**: could someone with ONLY the spec and no access to this machine rebuild it? Every path, credential name, and magic value must be declared, not assumed.
- **Config completeness**: instantiate the config for a *second, imaginary* product. Anything you can't express → the invariant layer has leaked specifics.
- **Trace one real run** end-to-end against the spec; every step the real system took must map to a spec clause. Unmapped steps = undocumented behavior.

## Common Mistakes

- Transcribing the code structure instead of the behavior (spec should survive a full rewrite in another stack)
- Losing the failure/recovery behaviors — working systems encode hard-won error handling that never made it to docs
- Writing "the AI decides" where the working system actually has a rule — dig for the rule
