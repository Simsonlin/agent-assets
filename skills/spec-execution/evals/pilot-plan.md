# Pilot Plan

Run the Skill against approximately nine real implementation tasks before expanding workflow complexity:

- three Probe tasks, including at least one third-party or human-only validation boundary;
- three Delivery tasks, including one simple local change and one broader behavioral change;
- three Assurance tasks, including a contract, migration, safety, or fail-closed concern.

Prefer representative work over synthetic fixtures. Do not force a task into an intent merely to balance the count.

Evaluate:

1. Did the implementation serve the stated Spec goal?
2. Was the selected route proportionate to intent and material risk?
3. Did review find goal blockers or material risks without over-prioritizing hygiene?
4. Did evidence faithfully represent what was and was not verified?
5. Did repair rounds converge within budget?
6. Did the workflow avoid wasteful fixtures, tests, repeated full reviews, or unnecessary agents?

Before counting an effective Assurance pilot as successful, run a capability-conformance case in an isolated disposable fixture:

- confirm the selected reviewer path is actually constrained by a read-only sandbox, rather than only instructed not to write;
- confirm a harmless attempted workspace write is denied and leaves the fixture unchanged;
- confirm write-capable external tools are absent or disabled for the reviewer path;
- confirm the final reviewer uses a fresh session distinct from the implementer and primary reviewer;
- confirm the adapter can use an explicitly read-only independent Codex session when the active spawn interface cannot select a custom reviewer;
- confirm the workflow records `effectiveExecutionIntent: delivery`, rather than `BLOCKED`, when enforced read-only review is unavailable and `capabilityFallback` is omitted or `continue`;
- confirm `capabilityFallback: block` reports `BLOCKED` when the same capability is unavailable;
- confirm a task with only human or external verification remaining reports `COMPLETE + READY_FOR_HUMAN_VALIDATION`, including the responsible party and next step.

Store only the compact run record. Do not store full conversations, hidden reasoning, or copies of product code.
