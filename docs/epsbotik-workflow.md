# epsbotik development workflow

This root repository owns the editable firmware and its knowledge. Reference clones under ignored `/sources/` are not worktrees for downstream changes.

## Setup

Install Git, Python 3, Node.js 22+, and `npm install -g lat.md@0.13.3`. For Pi, run `lat init` at the root, select Pi, review generated instructions, then follow the printed reload/restart instructions. Generated `.pi/` files contain local paths and must remain ignored. The CLI works independently of Pi integration.

Lat's default search uses a local model. No hosted indexing, key configuration, or UI publication is required. If semantic search cannot run, use `lat locate`, `lat section`, and direct reading; report the limitation instead of enabling a remote backend silently.

## Feature changes

Read root instructions, applicable nested instructions, binding ADRs, and relevant Lat sections. Create `feature/<topic>` from `main`. Define observable acceptance criteria. Record architecture-level decisions before implementation. Prefer board setup, capabilities, Lua modules, skills, and router rules over core-loop modifications when appropriate.

Keep changes small; update tests and knowledge in the same change. Run the affected-board ESP-IDF build, relevant tests, `python3 tools/epsbotik/check_project.py`, and `lat check`. Frontend changes also require upstream build/typecheck commands. Existing multilingual site changes require aligned translations and site checks. Documentation-only bootstrap does not establish firmware build success. The tested, qualified StickS3 baseline and its non-portable local prerequisites are recorded in [StickS3 build baseline](sticks3-build-baseline.md).

## Upstream integration

`origin` is `https://github.com/ozand/epsbotik.git`; `upstream` is `https://github.com/espressif/esp-claw.git`. The baseline is recorded in [upstream-base.txt](upstream-base.txt). Initial setup uses the existing local baseline, not an unreviewed latest checkout.

```sh
git fetch upstream
git switch main
git switch -c integration/upstream-YYYY-MM-DD
# Review the candidate commit and its dependencies before choosing:
git merge <reviewed-upstream-commit>
# Or, for a selective backport instead:
# git cherry-pick -x <reviewed-fix-commit>
```

Check status first and require a clean tree. Fetching is not integration, and integration is not permission to flash. Resolve conflicts by reviewing intent, especially in root docs and downstream hooks. Validate and review the result before merging to main; never force-push main. Update the upstream-base file only after a full selected upstream commit is incorporated as an ancestor, not after a partial backport. Remove redundant downstream work when upstream supplies an adequate replacement.

## Public commit boundary

Review `git diff --cached --stat` and the actual staged diff. Do not publish reference clones, local context, session logs, environment files, generated caches, build output, device identifiers, or credentials. Automated checks are defense in depth, not proof that every secret has been detected. Inspect filenames and newly added values without printing secret contents.

Preserve the upstream license and existing notices. Mark modified upstream files with an appropriate modification notice. New project code remains under the repository's Apache-2.0 license unless explicitly decided otherwise.

## Decisions and knowledge

[ADR index](adr/INDEX.md) is the authoritative decision history. [Lat](../lat.md/lat.md) describes current project intent and relationships, not session transcripts or a duplicate of all upstream docs. The graph check validates references, not behavioral correctness. Unknown installed-device behavior stays unknown until checked with authorization.
