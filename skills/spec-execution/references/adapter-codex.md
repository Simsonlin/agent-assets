# Codex Adapter

This is the first operational adapter.

## Capability mapping

- Use subagent delegation for implementation, review, and repair.
- Give reviewers fresh role context; use a new reviewer for the Assurance final review.
- Restrict a reviewer through an enforced read-only sandbox or tool configuration, not only through prompt wording.
- Continue the same implementer for local repairs when the harness exposes a continuable agent; otherwise start a fixer with the repair handoff.
- Native structured output may transport the normative handoff fields when reliably available; otherwise use the fixed Markdown contracts.
- Use a separate worktree only when isolation materially reduces risk. Do not create one mechanically for every task.

Codex subagents inherit the parent sandbox by default. Codex custom agents may override that sandbox, including with `sandbox_mode = "read-only"`, but a configuration file is not proof that the active spawn path selected it. Do not treat delegation as permission escalation. If the task needs a write or external action outside current authority, return control to the user-facing main agent.

## Reviewer restriction routing

During preflight, inspect the capabilities actually callable in the current run. Select the first enforceable reviewer path:

1. A fresh custom reviewer agent whose loaded configuration explicitly sets `sandbox_mode = "read-only"`, when the active delegation interface can select that agent by identity.
2. A fresh independent Codex session launched with an explicit read-only sandbox, such as a supported non-interactive `codex exec --sandbox read-only --ephemeral` invocation. This is reviewer delegation, not a review performed by the main implementation context.
3. If neither path is callable, apply the capability-downgrade policy. Assurance blocks; Probe or Delivery may continue only when workflow-core permits it.

Do not infer enforcement from any of the following alone:

- a reviewer-like task name;
- prompt text telling an ordinary write-capable agent not to edit;
- the presence of a custom-agent file when the spawn interface cannot select it;
- general Codex product documentation when the active runtime exposes no matching invocation path.

For this workflow, enforced read-only means that the reviewer cannot write the task workspace or invoke mutating external tools. Use a reviewed profile or tool filtering to disable write-capable MCP servers, connectors, hooks, and equivalent external actions; a filesystem sandbox alone is insufficient when those capabilities remain callable.

For each review, record the mechanism that enforced read-only access and the reviewer session identity. Capture the runtime thread or run identifier when exposed. For an ephemeral invocation that exposes no persistent identity, assign and record a unique invocation identifier before launch together with the exact restriction mechanism. For Assurance final review, start a new reviewer session; do not resume the primary reviewer. Do not change the parent task to read-only merely to create a reviewer, because the implementer and repair path may still require the authorized write boundary.

Codex custom agents are documented at <https://developers.openai.com/codex/multi-agent>. A project may provide a reviewer under `.codex/agents/`, or a user may provide one under `~/.codex/agents/`; this Skill does not install or mutate those configurations without separate authorization.

## Model selection

Select by role and risk, not by vendor-specific names embedded in the core workflow:

- simple, bounded implementation or lightweight review: efficient coding-capable model;
- ambiguous implementation, broad repair, or material-risk review: stronger reasoning/coding model;
- Assurance final review: the strongest practical independent reviewer available.

Model diversity is optional. Fresh role context and evidence-based review are required; choosing a different model is justified only when risk or failure history warrants the extra cost.

## Degradation

Disclose unavailable capabilities in the closeout. Assurance must stop if an enforced read-only reviewer, independent final review, necessary isolation, or required evidence cannot be preserved. For Probe and Delivery, a reviewer constrained only by assignment is a disclosed downgrade and may continue only under the workflow-core policy.
