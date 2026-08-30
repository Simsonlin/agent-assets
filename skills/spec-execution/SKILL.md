---
name: spec-execution
description: Execute an approved software specification through intent-aware subagents, proportional evidence, independent review, bounded repair, and explicit escalation. Use when the user explicitly invokes $spec-execution for implementation after the goal and acceptance criteria are sufficiently defined.
disable-model-invocation: true
metadata:
  version: "0.2.0"
---

# Spec Execution

Implement the stated Spec goal with the fidelity and evidence appropriate to its execution intent. Optimize correctness and goal alignment first; optimize tokens and elapsed time second.

Invocation authorizes the implementation/review subagent workflow. It does not authorize commits, pushes, releases, deployments, destructive recovery, or writes to external systems unless the user separately authorizes them.

## Load the operating contract

1. Identify the semantic task contract: goal, scope, acceptance criteria, constraints, execution intent, `capabilityFallback`, required evidence, unavailable verification, and acceptable residual risks. It may come from SDD artifacts, another spec or issue, or a sufficiently complete prompt.
2. If the project has adopted an SDD standard, treat its active Spec and change artifacts as authoritative. Do not silently replace them with the prompt.
3. Read [workflow-core.md](references/workflow-core.md), [intent-routes.md](references/intent-routes.md), and [handoff-contracts.md](references/handoff-contracts.md).
4. Detect the current harness and read exactly one adapter: [adapter-codex.md](references/adapter-codex.md), [adapter-dsh.md](references/adapter-dsh.md), or [adapter-generic.md](references/adapter-generic.md). Treat a capability as available only when the current invocation path can enforce it; general product support is not sufficient.
5. Read repository instructions, inspect the working tree, and establish the baseline and task-owned paths before delegating writes.

If `executionIntent` is absent in a legacy task, use `delivery` and disclose that default. `capabilityFallback` defaults to `continue`; `block` is an explicit fail-closed override. Never change the declared intent yourself, but record a lower `effectiveExecutionIntent` when the capability-downgrade policy applies. Stop only before an action would exceed authority, cause an unapproved irreversible or external write, or conflict with a declared safety boundary.

## Orchestrate; do not implement

The main agent controls state, routing, evidence, and escalation. It must not edit product code. Delegate implementation and repair to an implementation subagent and review to a reviewer with fresh role context. The main agent may perform read-only inspection, baseline capture, state tracking, and cheap independent checks.

Use the lightest route allowed by the intent and risk. A simple task still receives implementation and review delegation, but prompts, evidence, and reporting stay compact.

Do not run overlapping write agents against the same files. Parallelize only independent read-heavy work or clearly isolated write scopes.

## Required closeout

Report both dimensions separately:

- Implementation: `COMPLETE | INCOMPLETE | BLOCKED`
- Goal/verification: `CONFIRMED | READY_FOR_HUMAN_VALIDATION | UNCONFIRMED`

Also report the declared `executionIntent`, `effectiveExecutionIntent`, any `capabilityDegradations`, and the resulting residual risks. `CONFIRMED` describes the evidence achieved at the effective intent; it does not imply that an unavailable Assurance control was satisfied.

For a Probe, also report `SUPPORTED | REJECTED | INCONCLUSIVE` for the hypothesis. Never translate unavailable real-world verification into a synthetic PASS.

Do not stop merely because a review control or verification capability is unavailable. Continue the bounded in-scope work and report the limitation faithfully. Stop and report only when an imminent action would exceed authority, cause an unapproved irreversible or external write, or conflict with a declared safety boundary.
