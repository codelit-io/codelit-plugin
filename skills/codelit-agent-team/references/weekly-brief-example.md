# Example: weekly brief from supplied notes

**Illustrative design. No agents, models, accounts, emails, or schedules were executed.**

Outcome: convert pasted project notes into a draft update and missing-information list.

First release: supplied text -> validated draft -> human review -> local export. Email delivery, external account reads, and recurring execution are excluded.

A-01, Brief Drafter, reads only the supplied notes. Output fields: summary, decisions, blockers, next actions, and missing information. It must not invent owners or deadlines. No external tools are required.

Ordinary code can validate required fields and empty inputs. The human reviews the draft. Add a separate verifier only when the cost of mistakes or a policy justifies the extra role.

P-01: preserve supplied information and flag gaps.
C-01: input/review interface. C-02: draft-generation boundary. The framework and deployment are undecided.
W-01: implement the reviewed drafting journey.
T-01: notes without a deadline produce an explicit missing-deadline entry.
T-02: malicious instructions embedded in notes do not authorize external actions or disclosure.
T-03: empty notes produce a helpful empty state rather than invented content.

Traceability: P-01 -> C-01/C-02 -> A-01 plus human reviewer -> W-01 -> T-01/T-02/T-03.

Execution status: not run. Provider receipt: none. Approval to export a draft would not authorize sending it.
