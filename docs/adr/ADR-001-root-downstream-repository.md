# ADR-001: Develop epsbotik at the repository root with upstream history

**Status**: Accepted
**Date**: 2026-10-21
**Authors**: ozand and coding agent
**Supersedes**: None
**Related**: ADR-002 (knowledge graph)

## Context

Verified: the workspace has local context and a clean, full-history reference clone of espressif/esp-claw at 345073de68179542c307e303df81e38baadf77f0. The owner approved a public downstream project and specified the final spelling `epsbotik`. The installed device firmware version remains reported as unknown; source history does not identify it.

## Decision

Develop application code at the repository root, retaining upstream Git ancestry. Use `origin` for ozand/epsbotik, `upstream` for espressif/esp-claw, and `main` for the tested downstream line. Keep `/sources/` ignored and reference-only. Preserve the original license and attribution. Keep machine-specific context and session logs out of publication.

This is a downstream development repository, not an unrelated source snapshot, an automatic upstream deployment service, or permission to flash hardware. Integrate upstream through reviewed integration branches; prefer merge for ongoing synchronization and use `cherry-pick -x` selectively after dependency review. Do not rewrite published main history.

## Consequences

### What gets easier

Common ancestry enables normal upstream merges. Code and project knowledge share commits. The reference clone is unnecessary for normal Git synchronization.

### What gets harder

Upstream changes to shared root documentation may conflict. Public commits require a privacy review. Selective backports require dependency analysis.

### What does not change

Device operations require task-specific authorization. Runtime behavior is unchanged by repository setup.

## Alternatives Considered

- Develop inside `sources/esp-claw/`: rejected by the owner; sources are reference-only.
- Copy files into unrelated Git history: rejected because ordinary upstream merges would lose their shared base.
- Keep local work without a public remote: rejected because the owner requested a public repository.

## Test Contract

| Claim in Decision | Test | Currently |
|---|---|---|
| Upstream base is an ancestor | `python3 tools/epsbotik/check_project.py` (`test_upstream_ancestry`) | not yet written |
| Sources and local context are excluded | `python3 tools/epsbotik/check_project.py` (`test_public_boundary`) | not yet written |
| ADR files and index agree | `python3 tools/epsbotik/check_project.py` (`test_adr_index`) | not yet written |
| No firmware changes in bootstrap | `git diff 345073de -- application components` | pending |

## Rollback

Local context is backed up outside the repository before migration. Repository setup can be reverted in a new commit; public pushes cannot guarantee removal of data already copied by others. Do not delete or rewrite upstream history to undo setup.

## References

- https://github.com/espressif/esp-claw
- [ADR index](./INDEX.md)
