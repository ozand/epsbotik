# Development

Code, tests, decisions, and current knowledge evolve together in epsbotik, while upstream integration remains a reviewed operation.

## Feature workflow

Read relevant knowledge and nested instructions, define acceptance criteria, then make a focused feature-branch change.

Follow [[docs/epsbotik-workflow.md]] and inherited [[.agents/gotchas.md]]. Architecture, contract, trust-boundary, or persisted-format decisions require an ADR before implementation. [[docs/adr/INDEX.md]] lists binding statuses; superseded and withdrawn records are history. Update meaningful knowledge with code and tests, not as a session transcript.

## Upstream integration

The root repository retains upstream ancestry so reviewed original changes can be merged without copying from reference clones.

Use integration branches and the upstream remote as defined in [[docs/epsbotik-workflow.md]]. Prefer merge for ongoing synchronization; selectively backport with provenance only after dependency review. Do not rewrite published main. [[docs/upstream-base.txt]] advances only when a complete selected base is incorporated, not after partial cherry-picks.

## Validation and safety

Structural knowledge checks supplement executable tests and review; none authorizes device operations.

Run [[verification]] checks and affected firmware/frontend tests. Preserve alignment when changing translated site documentation under [[docs/src/content/docs]], as required by [[.agents/docs.md]]. Downstream maintainer docs, ADRs, and this graph have a separate scope. Hosted indexing and public UI publication require separate approval.
