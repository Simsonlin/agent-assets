# Generic Harness Adapter

Use this adapter only when the current harness is neither Codex nor DSH or cannot be identified reliably.

## Negotiate capabilities

Determine whether the harness can provide:

- isolated or fresh agent context;
- implementation delegation;
- independent review delegation;
- write/tool restriction;
- structured output;
- agent continuation;
- model selection;
- workspace isolation.

Use semantic roles rather than tool names. If a feature is unavailable, follow the workflow downgrade policy and disclose the limitation. Never simulate an independent reviewer by asking the implementation context to declare itself independent.

If the harness has no subagent or delegation capability, this Skill cannot satisfy its defining workflow. Stop with `BLOCKED` and explain the missing capability rather than implementing product code in the main agent.
