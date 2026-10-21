# ADR-002: Keep the epsbotik knowledge graph beside root application code

**Status**: Accepted
**Date**: 2026-10-21
**Authors**: ozand and coding agent
**Supersedes**: None
**Related**: ADR-001 (repository boundary)

## Context

Reported by Lat documentation: Lat stores linked project knowledge in Markdown, validates references, supports C symbol links, and offers Pi integration. Verified: the owner approved using it for epsbotik, not for the ignored reference clone. Structural validation does not prove runtime behavior.

## Decision

Use Lat 0.13.3 as a development tool and store epsbotik knowledge in root `lat.md/`. Keep root README and AGENTS as entry points, formal decision history in `docs/adr/`, and concise current intent in Lat. Agent work reads relevant knowledge first, updates it alongside meaningful behavior changes, and runs `lat check` before completion. Configure project-local Pi integration; no hosted knowledge publication or external model indexing is authorized by this decision.

This is not a replacement for Git, executable tests, upstream documentation, or human review. Do not put secrets, device-specific identifiers, session transcripts, or source inventories in the graph. Do not mass-annotate unchanged upstream code. Distinguish verified behavior, reported facts, proposals, and unknowns. Existing multilingual upstream docs retain their alignment rules; downstream maintainer docs and Lat are a separate scope.

## Consequences

### What gets easier

Agents can retrieve project-specific constraints and connect them to implementation. Knowledge evolves with the code it describes.

### What gets harder

Contributors must maintain graph links and install a pinned development tool. Integration activation may require reloading Pi. Structural checks still need semantic review.

### What does not change

Firmware has no new runtime dependency. Existing license, build requirements, hardware authorization, and test obligations remain.

## Alternatives Considered

- Put Lat inside the reference clone: rejected because it would describe the wrong project and remain outside published downstream history.
- Use only session logs: rejected because logs do not provide a curated, reviewable source of current constraints.
- Duplicate all upstream documentation: rejected because duplicated detail increases drift and maintenance cost.

## Test Contract

| Claim in Decision | Test | Currently |
|---|---|---|
| Graph structure and references resolve | `lat check` | pending |
| Root knowledge and instructions exist | `python3 tools/epsbotik/check_project.py` (`test_knowledge_entrypoints`) | not yet written |
| ADR index remains complete | `python3 tools/epsbotik/check_project.py` (`test_adr_index`) | not yet written |
| Firmware unaffected | `git diff 345073de -- application components` | pending |

## Rollback

Remove the integration and graph in a follow-on decision and commit; firmware needs no migration. Retain ADR history.

## References

- https://www.lat.md/quick-start
- https://www.lat.md/docs/concepts
- https://www.lat.md/docs/lat-workflow
- [ADR index](./INDEX.md)
