# Project

Epsbotik is a personal downstream of ESP-Claw for custom IoT-agent behavior and StickS3 adaptation, with its source and knowledge owned by the root repository.

## Provenance

The starting upstream commit is recorded in [[docs/upstream-base.txt]], with Git ancestry and [[LICENSE]] retained.

Verified during setup: the reference checkout contains a full upstream history. The root tree is derived from that baseline. Bootstrap does not modify firmware behavior. [[docs/adr/INDEX.md]] records the binding repository and knowledge decisions.

## Ownership

Our editable firmware lives at the root, not under the ignored reference directory.

[[application/edge_agent]] owns the main firmware application; [[components]] holds reusable modules and capabilities. [[README.md]] and [[AGENTS.md]] route contributors into this graph and the engineering rules. Local reference clones, private context, and session logs are outside publication.

## Device uncertainty

The owner reports ESP-Claw on a StickS3, but the installed firmware version is unknown.

The source version does not establish installed capabilities. Prior network and USB observations are reported rather than repeated setup measurements; see [[docs/device-research.md]]. Device access and changes require explicit task-specific authorization. Public knowledge excludes private endpoints, device identifiers, and credentials.
