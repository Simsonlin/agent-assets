---
name: spec-execution
description: Execute an approved software specification through intent-aware subagents, proportional evidence, independent review, bounded repair, and explicit escalation. Use when the user explicitly invokes $spec-execution for implementation after the goal and acceptance criteria are sufficiently defined.
disable-model-invocation: true
metadata:
  version: "0.1.0"
---

# Spec Execution

Implement the stated Spec goal with the fidelity and evidence appropriate to its execution intent. Optimize correctness and goal alignment first; optimize tokens and elapsed time second.

Invocation authorizes the implementation/review subagent workflow. It does not authorize commits, pushes, releases, deployments, destructive recovery, or writes to external systems unless the user separately authorizes them.

## Load the operating contract

1. Identify the semantic task contract: goal, scope, acceptance criteria, constraints, execution intent, required evidence, unavailable verification, and acceptable residual risks. It may come from SDD artifacts, another spec or issue, or a sufficiently complete prompt.
2. If the project has adopted an SDD standard, treat its active Spec and change artifacts as authoritative. Do not silently replace them with the prompt.
3. Read [workflow-core.md](references/workflow-core.md), [intent-routes.md](references/intent-routes.md), and [handoff-contracts.md](references/handoff-contracts.md).
4. Detect the current harness and read exactly one adapter: [adapter-codex.md](references/adapter-codex.md), [adapter-dsh.md](references/adapter-dsh.md), or [adapter-generic.md](references/adapter-generic.md).
5. Read repository instructions, inspect the working tree, and establish the baseline and task-owned paths before delegating writes.

If `executionIntent` is absent in a legacy task, use `delivery` and disclose that default. Never change the intent yourself. If the stated intent conflicts with the real risk or evidence boundary, stop and recommend a Spec decision.

## Orchestrate; do not implement

The main agent controls state, routing, evidence, and escalation. It must not edit product code. Delegate implementation and repair to an implementation subagent and review to a reviewer with fresh role context. The main agent may perform read-only inspection, baseline capture, state tracking, and cheap independent checks.

Use the lightest route allowed by the intent and risk. A simple task still receives implementation and review delegation, but prompts, evidence, and reporting stay compact.

Do not run overlapping write agents against the same files. Parallelize only independent read-heavy work or clearly isolated write scopes.

## Required closeout

Report both dimensions separately:

- Implementation: `COMPLETE | INCOMPLETE | BLOCKED`
- Goal/verification: `CONFIRMED | READY_FOR_HUMAN_VALIDATION | UNCONFIRMED`

For a Probe, also report `SUPPORTED | REJECTED | INCONCLUSIVE` for the hypothesis. Never translate unavailable real-world verification into a synthetic PASS.

Stop and report when the goal, acceptance criteria, authority, intent, safety boundary, or implementation strategy requires a decision not already made in the task contract. Do not treat mere technical difficulty as a reason to stop while bounded in-scope progress remains possible.
