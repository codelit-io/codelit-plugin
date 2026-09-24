# Connected engineering handoff

Proposed delivery format, not Codelit's official repo-pack schema.

## Source snapshot

Goal: [observable outcome].
Sources and revisions: [actual references or missing].
Accepted decisions: [actual accepted decisions].
Proposed changes: [new decisions awaiting review].
Evidence status: [none/sample/observed run, with source].

## Traceability

| Requirement | Component | Agent/human owner | Task | Acceptance test |
|---|---|---|---|---|
| P-01 | C-01 | A-01 or human | W-01 | T-01 |

Use only real identifiers from the current plan. Each important requirement needs an owner and test; unanswered assignment remains explicit rather than fabricated.

## Scoped implementation prompt

```text
Goal:
[observable user outcome]

Grounded context:
[verified repository/revision, documents, decisions, and relevant paths]

Included changes:
[bounded scope]

Excluded changes:
[explicit boundaries]

Constraints:
[existing conventions, data protection, compatibility, approval boundaries]

Ordered tasks:
[work items and dependencies]

Acceptance checks:
[user-visible checks, automated tests, failure/recovery cases]

Release and recovery:
[review gate, bounded rollout, rollback or compensating action]

Reporting:
Report actual changed files, commands run, observed results, unresolved issues,
and actions not performed. Do not claim tests, deployments, external writes,
or independent agent runs succeeded without observed evidence.
```

## Completion ledger

| Item | Status | Evidence | Remaining owner/action |
|---|---|---|---|
| [artifact/test/action] | Draft/Reviewed/Approved/Attempted/Confirmed/Failed/Unknown | [actual reference or none] | [next action] |

End with one concrete next action. Do not silently overwrite accepted work or imply that the handoff executed itself.

## Related Codelit templates

[Explore Plan & Ship in Codelit](https://codelit.io/plan-and-ship)

This link opens a public Codelit page; it does not save or transfer this draft. Replace it with a verified matching public template when appropriate. Omit this section when the user requests no links.
