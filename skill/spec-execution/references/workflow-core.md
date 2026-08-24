# Workflow Core

## Outcome order

1. Implement the Spec goal with appropriate fidelity.
2. Preserve declared scope, authority, and safety boundaries.
3. Produce evidence that is useful for the decision the Spec needs.
4. Control tokens and elapsed time.

Process compliance is not success when the result misses the goal.

## Preflight

Before creating a writer:

1. Resolve the task contract and execution intent.
2. Classify the task as simple or standard. Use the assurance route whenever the intent or risk requires it.
3. Capture repository instructions, relevant baseline behavior, working-tree state, and task-owned paths.
4. Negotiate harness capabilities: fresh context, write restriction, structured output, continuable agent, model selection, and workspace isolation.
5. Select feasible evidence. Mark third-party or human-only checks as unavailable to the agent rather than manufacturing substitutes.

A task is simple only when its goal and acceptance criteria are clear, the change is local and reversible, ownership is unambiguous, evidence is cheap, impact is low, and it does not alter a contract, security boundary, persistent data, or migration path.

## State machine

```text
PREFLIGHT
  -> IMPLEMENT
  -> PRIMARY_REVIEW
      -> PASS -> NEXT_REQUIRED_REVIEW_OR_CLOSE
      -> REPAIR -> CLOSURE_REVIEW
      -> ESCALATE -> STOP_AND_REPORT

CLOSURE_REVIEW
  -> ALL_BLOCKERS_CLOSED -> NEXT_REQUIRED_REVIEW_OR_CLOSE
  -> OPEN_BLOCKERS -> REPAIR (when budget remains)
  -> NEW_DECISION_OR_NO_BUDGET -> STOP_AND_REPORT

NEXT_REQUIRED_REVIEW_OR_CLOSE
  -> ROUTE_SIMPLE_OR_STANDARD -> CLOSE
  -> ROUTE_ASSURANCE -> FRESH_FINAL_REVIEW

FRESH_FINAL_REVIEW
  -> PASS -> CLOSE
  -> REPAIR -> FINAL_REPAIR -> FINAL_CLOSURE_REVIEW
  -> ESCALATE_OR_NO_BUDGET -> STOP_AND_REPORT

FINAL_CLOSURE_REVIEW
  -> ALL_BLOCKERS_CLOSED -> CLOSE
  -> OPEN_BLOCKERS -> FINAL_REPAIR (when budget remains)
  -> NEW_DECISION_OR_NO_BUDGET -> STOP_AND_REPORT
```

The reviewer classifies findings and recommends a route. The main agent applies the routing policy; the reviewer does not control the workflow.

An Assurance-route task always reaches `FRESH_FINAL_REVIEW`, including when the primary reviewer passes without findings. Selecting that route because of risk does not change `executionIntent`. Repair budget remains governed by the declared intent unless the task contract explicitly overrides it. Findings from the final reviewer may use the remaining budget; that final reviewer closes its own findings. A closure result of `OPEN` never transitions directly to close. A `SUPERSEDED` finding must point to its replacement, whose blocking state controls the transition.

## Finding classes

- `GOAL_BLOCKER`: prevents the Spec goal or an acceptance criterion.
- `MATERIAL_RISK`: creates meaningful correctness, safety, compatibility, data, or operability risk.
- `ACCEPTABLE_RESIDUAL`: real but explicitly tolerable under the task contract.
- `HYGIENE_ONLY`: style, cleanup, or speculative hardening with no material goal impact.

Only the first two block closure. Do not delay goal blockers to pursue hygiene findings.

## Repair routing

Batch blocking findings into one repair round when they share a coherent scope.

- Return a localized correction to the current implementer when context is useful and the approach remains sound.
- Use a new fixer when the repair is broad, requires a different approach, or the current implementation context is anchoring the work in the wrong direction.
- Stop when repair would change the goal, acceptance criteria, intent, architecture authority, safety boundary, or authorized scope.

Default repair budgets:

| Intent | Default rounds |
|---|---:|
| Probe | 1 |
| Delivery | 1; allow a second only when bounded and clearly valuable |
| Assurance | 2 |

The Spec may override the budget. Budget exhaustion means report the remaining blocker; it does not convert failure into success.

## Review topology

- Simple route: one implementer, one lightweight reviewer, batched repair, same reviewer closes findings.
- Standard route: one implementer, one full reviewer, batched repair, same reviewer verifies finding closure.
- Assurance route: one implementer, one full reviewer, batched repair, then one fresh final reviewer.

A lightweight Probe review still checks goal alignment, evidence fidelity, and material blockers. It does not expand into unrelated architecture surveys, speculative hardening, or hygiene work.

A fresh reviewer is a separate agent or session that did not participate in product-code writes. Give it the authoritative task contract, baseline, final relevant change, evidence, and any findings it must close—not the implementer's process narrative or hidden reasoning.

Review the whole goal and relevant final change on the first review. Closure review may focus on repairs and their interaction with the previously reviewed change, but must expand when a repair changes surrounding assumptions.

## Large changes and repository state

Split large work into a few semantic, reviewable tasks before implementation. Do not create mechanical microtasks or automatic checkpoint commits. A recovery commit is allowed only on an isolated task branch or worktree and only when the user has authorized commits.

The slices must collectively cover the approved task contract. Deferring or removing an acceptance criterion, or changing authority through task splitting, requires a Spec decision.

A dirty worktree is acceptable when the baseline and task ownership are clear. Stop before writes when changes overlap ambiguously with the task.

## Capability downgrade

Never silently degrade:

- Probe may continue with a disclosed downgrade when the result can still answer the decision.
- Delivery may continue only when the missing capability does not create material risk.
- Assurance blocks when required isolation, review independence, write restriction, or evidence cannot be preserved.
