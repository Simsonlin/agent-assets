# Pilot Run Record

```yaml
date: YYYY-MM-DD
taskReference: repository-or-local-reference
executionIntent: probe | delivery | assurance
effectiveExecutionIntent: probe | delivery | assurance
capabilityFallback: continue | block
route: simple | standard | assurance
capabilityDegradations: []
agents:
  implementers: 0
  reviewers: 0
  fixers: 0
reviewRestriction:
  mechanism: custom-agent-read-only | independent-session-read-only | prompt-only-downgrade | unavailable
  primaryReviewerSession: ""
  finalReviewerSession: ""
rounds: 0
elapsedTime: unavailable
tokens: unavailable
blockingFindings: []
findingClosure: []
implementationStatus: COMPLETE | INCOMPLETE | BLOCKED
goalStatus: CONFIRMED | READY_FOR_HUMAN_VALIDATION | UNCONFIRMED
humanValidation:
  responsibleParty: ""
  nextStep: ""
probeOutcome: SUPPORTED | REJECTED | INCONCLUSIVE | NOT_APPLICABLE
userOverrides: []
wasteObserved: []
notes: ""
```

Record time and tokens only when the harness exposes them without extra instrumentation.

`rounds` counts repair rounds, not initial implementation or review turns.
