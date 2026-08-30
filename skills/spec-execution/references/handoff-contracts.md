# Handoff Contracts

The fixed Markdown forms below are the v0.1 normative semantic protocol. A harness may transport the same fields through native structured output, but it must preserve every field and enum exactly. Missing or incompatible fields produce `INVALID_AGENT_OUTPUT`; the main agent requests one correction before treating the agent as failed.

## Implementer assignment

Provide:

- task contract and authoritative sources;
- declared and effective execution intent, `capabilityFallback`, and confidence target;
- owned paths and forbidden paths;
- baseline and existing user changes to preserve;
- required evidence and unavailable verification;
- explicit non-authorizations;
- requested output contract.

## Implementer result

```markdown
STATUS: COMPLETE | INCOMPLETE | BLOCKED
SUMMARY: <goal-level outcome>
CHANGED: <paths and behavioral effect>
EVIDENCE: <checks run and results>
UNAVAILABLE_VERIFICATION: <none or faithful checks still requiring humans/systems>
RESIDUAL_RISKS: <none or known risks>
DEVIATIONS: <none or divergence from task contract>
REVIEW_NOTES: <high-value context, not a full activity log>
```

## Reviewer assignment

Give the reviewer a separate agent/session that did not participate in product-code writes, plus the task contract, baseline, final relevant change, implementer evidence, and prior blocking findings when closing repairs. Do not give the implementer's process narrative or hidden reasoning, and do not ask the reviewer to trust the implementer's conclusion.

Reviewer priorities:

1. Spec goal and acceptance criteria.
2. Material correctness, safety, compatibility, data, and operability risks.
3. Evidence fidelity and unavailable real-world checks.
4. Scope discipline and regression risk.
5. Hygiene only after material issues.

## Reviewer result

```markdown
VERDICT: PASS | REPAIR | ESCALATE
GOAL_ASSESSMENT: <whether the implementation serves the stated goal>
FINDINGS:
- ID: <stable id>
  CLASS: GOAL_BLOCKER | MATERIAL_RISK | ACCEPTABLE_RESIDUAL | HYGIENE_ONLY
  EVIDENCE: <path, behavior, or reproducible observation>
  IMPACT: <why it matters to the task contract>
  REQUIRED_CHANGE: <bounded correction or none>
ROUTE_RECOMMENDATION: SAME_IMPLEMENTER | NEW_FIXER | STOP
VERIFICATION_GAPS: <none or checks that remain unavailable>
```

Each blocking finding needs evidence and impact. Do not emit speculative lists without a concrete connection to the task contract.

Verdict invariants:

- `PASS` if and only if there are no open `GOAL_BLOCKER` or `MATERIAL_RISK` findings.
- `REPAIR` only when blocking findings can be corrected inside the authorized scope and remaining repair budget.
- `ESCALATE` when closure needs a new decision, exceeds authority, lacks a required capability, or has no viable repair budget.
- `SAME_IMPLEMENTER` and `NEW_FIXER` are valid only with `REPAIR`; `STOP` is valid only with `ESCALATE`.

## Repair assignment and closure

Pass stable finding IDs, required outcomes, owned paths, and remaining budget. The fixer must report which IDs it addressed and any new scope. Closure review returns every blocking ID as `CLOSED`, `OPEN`, or `SUPERSEDED` with evidence. `SUPERSEDED` must name the replacement finding. All blockers closed proceeds to the next required review stage; open blockers consume another repair round when budget remains, otherwise stop and report.

## Main-agent closeout

Record only decision-useful state: declared and effective intent, route, capability degradations, agents and rounds, reviewer restriction mechanism and session identity, blockers and closure, evidence, double status, human-validation owner and next step when applicable, user overrides, and any wasteful fixture/test work observed. Do not retain full conversations or chain-of-thought as workflow telemetry.
