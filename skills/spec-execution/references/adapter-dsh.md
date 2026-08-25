# DSH Adapter

This adapter maps the portable workflow to DeepSeek Harness. Treat it as an explicit capability mapping until it has completed the pilot suite in a real DSH environment.

## Discovery and invocation

DSH can discover Agent Skills bundles from project and user `.agents/skills`, DSH-specific roots, or configured custom Skill directories. Preserve explicit invocation with `disable-model-invocation: true` and user invocation enabled.

## Subagent mapping

Inspect the active DSH subagent provider and its advertised capabilities before routing. Map, rather than assume:

- fresh role/session context;
- tool or write filtering;
- structured output/schema support;
- resumable or continuable agents;
- model/provider selection;
- workspace or filesystem isolation.

Use the DSH subagent/delegation capability for implementer and reviewer roles. Require the provider to reject unsupported hard requirements instead of silently approximating them. Native schema output is only a transport for the normative handoff fields; when it is unsupported, use the fixed Markdown handoff.

Do not encode a particular model vendor in the core workflow. DSH may route roles through different providers or transports; select by capability, risk, and available budget.

## Verified capability matrix (real DSH session)

Checked against a live DSH session (captain route: deepseek-v4-flash; file policy: workspace-write; approval policy: ask). Update this matrix after each pilot run.

| Capability | Status | Mechanism / gap |
|---|---|---|
| Fresh role/session context | `available` | `subagent` (fresh context), `workflow` `agent()`, `ralph` fresh rounds, AgentTeams members |
| Resumable / continuable agents | `available` | `subagent` durable id + `send_message`; AgentTeams durable members + tasks |
| Structured output / schema | `partial` | Only `workflow` `agent({schema})` supports object-rooted JSON Schema; plain `subagent` returns text only → use the fixed Markdown handoff (the v0.1 normative protocol) |
| Model / provider selection | `partial` (requires explicit user request) | `workflow` `agent({provider, model})` and AgentTeams `add_member(provider, model)`; plain `subagent` has no override. Tool contract allows provider/model only when the user explicitly requests that role-specific route |
| Tool / write filtering | `unavailable` | No per-subagent or per-role tool/path restriction. Only session-level file sandbox (workspace-write) + approval policy. Owned/forbidden paths are soft (prompt-level), not enforceable |
| Workspace / filesystem isolation | `unavailable` | Single shared workspace; no per-role workspace isolation |

Known consequence: the pilot-plan capability-conformance case ("reviewer actually constrained by a read-only sandbox; attempted write denied") cannot pass on the current DSH invocation path.

## Preferred delegation transport: AgentTeams

- **Activation precondition**: AgentTeams exists only when the user explicitly asks ("use AgentTeams to do X") or a `/agent-teams` activation message arrives. When not activated, fall back to plain `subagent` delegation: fresh context and continuability remain, but per-role model/provider selection and task-dependency orchestration are lost.
- **Role mapping**: captain = main agent (orchestration only, never edits product code); implementer / reviewer / fixer = durable team members; one team at a time, tasks with dependencies, delete the team at closeout.
- **Model / effort division of labor — propose, then let the user confirm**: built-in recommendation table: implementer inherits the captain's default route; reviewer / fixer use a stronger reasoning route; the Assurance final reviewer uses the highest-confidence route. `agent_teams_add_member` accepts provider/model only for an explicitly user-requested role route, so the captain proposes and the user explicitly confirms before passing them. Effort rule: same provider/model members inherit the captain's reasoning effort; a changed route uses the target model's default unless explicitly specified. Do not hard-code vendor model names; describe routes generically.
- **Alternative transport**: `workflow` supports fresh agents with `{schema, provider, model}` overrides and suits bounded pipelines; its script body has no filesystem/network access — agents do the work.
- **To verify during pilot**: whether skill invocation and `/agent-teams` activation coexist reliably in the same round, and whether the captain reading this adapter after activation is dependable.

## Degradation

Apply the same Probe/Delivery/Assurance downgrade policy as the workflow core. Record the missing advertised capability and the chosen route. Assurance blocks when required independence, restriction, isolation, or evidence is unavailable.

DSH-specific routing given the matrix above:

- **Probe**: continue with a disclosed downgrade ("write restriction / isolation unavailable") when the result can still answer the decision.
- **Delivery**: continue only when the missing capability creates no material risk; disclose that "implementer instructed to touch only owned paths" is a soft constraint, not enforcement.
- **Assurance**: write restriction and workspace isolation cannot be enforced on this invocation path → block per policy, route through ESCALATE → STOP_AND_REPORT and hand the "whether to relax" decision back to the Spec owner. Never turn the missing enforcement into a synthetic PASS.
