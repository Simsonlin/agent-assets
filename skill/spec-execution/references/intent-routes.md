# Intent Routes

`executionIntent` is orthogonal to the SDD Profile. Profile governs persistence and governance; intent governs how one change is implemented and evidenced.

## Probe

Purpose: test an idea, integration feasibility, or directional hypothesis quickly.

- Prefer the smallest reversible implementation that can answer the decision.
- Evidence target: directional confidence, not production completeness.
- Do not build elaborate fixtures, mocks, or generalized infrastructure unless they materially improve the decision.
- A mock may validate local assumptions but cannot substitute for unavailable third-party behavior.
- Record the hypothesis result as `SUPPORTED`, `REJECTED`, or `INCONCLUSIVE`.
- It is valid for implementation to be complete while real-world validation remains ready for a human.

## Delivery

Purpose: produce usable behavior with proportionate confidence.

- Cover acceptance criteria and material regressions.
- Prefer existing tests and direct behavior checks; add tests when they provide durable evidence for material behavior or risk.
- Use manual verification when it is the most faithful evidence.
- Do not block delivery on low-impact hygiene unless the task contract makes it a requirement.

## Assurance

Purpose: implement sensitive system logic, contracts, migrations, safety boundaries, or governed release behavior with high confidence.

- Require traceability from acceptance criteria and contracts to evidence.
- Exercise failure paths, compatibility, rollback, and fail-closed behavior when relevant.
- Preserve independent final review.
- Block rather than silently downgrade when required evidence or isolation is unavailable.

## Evidence fields

The task contract should state:

- `requiredEvidence`: evidence needed for the goal decision.
- `unavailableVerification`: checks the agent cannot faithfully perform and who or what can perform them.
- `acceptableResidualRisks`: known risks explicitly accepted for this intent.
- Optional `confidenceTarget`: an explicit override; otherwise use directional for Probe, reasonable for Delivery, and high for Assurance.

Tests are evidence by default, not authority. Create or modify them for evidence value, not to satisfy a blanket test-count expectation.
