---
lat:
  require-code-mention: true
---
# Verification

Repository tests guard downstream ownership and documentation structure; they do not establish firmware or hardware correctness.

## Upstream ancestry

The declared upstream baseline must be an ancestor of HEAD, allowing ordinary integration with a shared Git base.

Run `python3 tools/epsbotik/check_project.py`. This does not fetch remote changes or prove a backport's dependencies are complete.

## Public boundary

Reference sources, private context, and session data must be ignored and absent from tracked or staged files.

The test checks representative exclusions and repository filenames. Manual staged-content review remains required because ignore rules and pattern checks cannot establish absence of every secret.

## ADR index

Every ADR must appear in the index, every indexed ADR must exist, and status and mandatory sections must be present and consistent.

This guards navigability, not the correctness of the architectural reasoning or completeness of behavioral tests.

## Knowledge entrypoints

Root instructions, the graph entry point, and installed-tool version guidance must exist and identify the downstream workflow.

Run `lat check` separately to validate graph links and sections. Pi integration activation and semantic retrieval must be checked independently; file existence alone does not prove tool availability.
