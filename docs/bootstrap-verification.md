# Bootstrap verification

This records bootstrap checks, not runtime or installed-device verification. The accepted ADRs retain their original test-contract state; results are recorded here without rewriting accepted rationale.

## Executed locally

On 2026-10-21, `python3 tools/epsbotik/check_project.py` passed all four tests: upstream ancestry, public boundary, ADR index, and knowledge entrypoints. `lat check` passed after new source files were staged so its Git-based discovery could see the test references. `lat search 'upstream integration'` built the local index and returned relevant graph sections.

`git diff 345073de -- application components` was empty. The upstream license was retained unchanged. A limited staged-content privacy-pattern scan passed; it is not a guarantee against every sensitive value. Session logs, original device research, and reference clones were excluded rather than published.

## Automation and limits

[Repository checks](../.github/workflows/epsbotik-check.yml) run the Python contract and pinned Lat checker on main pushes and pull requests. They require network access to install packages but no project API keys. No CI success is claimed until its GitHub run is observed.

No firmware build, frontend build, device access, flashing, restart, USB change, or functional hardware test was performed. Firmware source was not changed by bootstrap. Pi extension generation and activation are separate from successful CLI graph/search checks.
