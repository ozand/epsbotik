# epsbotik — ADR Index

This series uses `ADR-NNN-kebab-case-slug.md` with three-digit padding. Records contain status, context, decision, consequences, alternatives, test contract, and rollback. The owner approved these decisions before bootstrap implementation. Test results are recorded separately rather than rewriting accepted rationale.

| ADR | Decision | Status |
|---|---|---|
| [ADR-001](./ADR-001-root-downstream-repository.md) | Develop epsbotik at the root with upstream history | Accepted |
| [ADR-002](./ADR-002-root-lat-knowledge.md) | Keep epsbotik knowledge beside root application code | Accepted |

## How to amend

Accepted records are amended by a new ADR with `Supersedes: ADR-NNN`, not edited in place. Update only the superseded status in the old record. Append new numbers; never reuse or renumber them. Proposed records may be edited. Superseded and withdrawn decisions remain history, not current constraints. Add every record to this index in the same change.

## Burned numbers

None.
