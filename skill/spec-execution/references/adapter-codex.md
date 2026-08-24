# Codex Adapter

This is the first operational adapter.

## Capability mapping

- Use subagent delegation for implementation, review, and repair.
- Give reviewers fresh role context; use a new reviewer for the Assurance final review.
- Restrict a reviewer through an enforced read-only role or tool configuration, not only through prompt wording.
- Continue the same implementer for local repairs when the harness exposes a continuable agent; otherwise start a fixer with the repair handoff.
- Native structured output may transport the normative handoff fields when reliably available; otherwise use the fixed Markdown contracts.
- Use a separate worktree only when isolation materially reduces risk. Do not create one mechanically for every task.

Subagents inherit the active permission boundary. Do not treat delegation as permission escalation. If the task needs a write or external action outside current authority, return control to the user-facing main agent.

## Model selection

Select by role and risk, not by vendor-specific names embedded in the core workflow:

- simple, bounded implementation or lightweight review: efficient coding-capable model;
- ambiguous implementation, broad repair, or material-risk review: stronger reasoning/coding model;
- Assurance final review: the strongest practical independent reviewer available.

Model diversity is optional. Fresh role context and evidence-based review are required; choosing a different model is justified only when risk or failure history warrants the extra cost.

## Degradation

Disclose unavailable capabilities in the closeout. Assurance must stop if an enforced read-only reviewer, independent final review, necessary isolation, or required evidence cannot be preserved. For Probe and Delivery, a reviewer constrained only by assignment is a disclosed downgrade and may continue only under the workflow-core policy.
