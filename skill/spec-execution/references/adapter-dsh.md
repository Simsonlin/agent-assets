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

## Degradation

Apply the same Probe/Delivery/Assurance downgrade policy as the workflow core. Record the missing advertised capability and the chosen route. Assurance blocks when required independence, restriction, isolation, or evidence is unavailable.
