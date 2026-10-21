# epsbotik

Personal downstream of [Espressif ESP-Claw](https://github.com/espressif/esp-claw), developed at this repository root for custom IoT-agent behavior and M5Stack StickS3 adaptation. This README is modified for epsbotik; original upstream documentation remains in Git history and the documentation site sources.

## Status and provenance

The initial source baseline is `345073de68179542c307e303df81e38baadf77f0`. Git ancestry and the original [Apache-2.0 license](LICENSE) are retained. This is an independent downstream project, not an official Espressif release. Bootstrap changes development documentation and tooling only; it does not change firmware behavior.

The owner reports ESP-Claw is installed on their StickS3. Its firmware version is unknown and is not established by this checkout. No device access, configuration change, restart, or flashing is part of repository setup.

## Start here

- [AGENTS.md](AGENTS.md): agent responsibilities, safety boundaries, and inherited engineering guidance.
- [Knowledge graph](lat.md/lat.md): project intent, architecture, and verification links.
- [Architecture decisions](docs/adr/INDEX.md): currently binding decisions and their history.
- [Development workflow](docs/epsbotik-workflow.md): setup, branches, upstream integration, and publication checks.
- [Bootstrap verification](docs/bootstrap-verification.md): executed checks and untested boundaries.
- [Device research summary](docs/device-research.md): deliberately sanitized prior observations and unknowns.
- [Upstream application guide](application/edge_agent/README.md): firmware setup; select the correct board rather than blindly copying a generic board example.

## Layout and ownership

`application/`, `components/`, and `tools/` contain our editable source tree, inherited from ESP-Claw. `docs/` contains documentation and ADRs; `lat.md/` is the downstream knowledge graph. `/sources/` is an ignored, reference-only local directory, never the development target. Local context and session logs are not published.

## Development checks

Install Node.js 22 or newer, Python 3, and the pinned development tool:

```sh
npm install -g lat.md@0.13.3
python3 tools/epsbotik/check_project.py
lat check
```

For a new Pi checkout, run `lat init`, select Pi, review the generated changes, and follow its activation instructions. Project-local Pi files are ignored because the generated extension embeds local installation paths. The CLI and this repository's instructions remain usable without the extension. Semantic indexing is local by default; do not enable hosted embeddings or publish the graph without separate approval.

Firmware work additionally requires the upstream ESP-IDF environment, board-manager setup, and an affected-board build. Hardware operations require explicit task-specific authorization. See [the workflow](docs/epsbotik-workflow.md).
