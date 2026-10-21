# Device research — public summary

This sanitized summary preserves relevant uncertainty without publishing the owner's local device identifiers or environment paths. The original research notes are retained in ignored local context and an external bootstrap backup.

## Evidence and limits

Reported by prior workspace research, not rechecked during repository bootstrap: an ESP-Claw web UI, a status endpoint, and a DATA-root directory listing were accessible; a candidate MCP TCP port accepted a connection. MCP handshake and tools listing were not performed. An open TCP port is not proof of MCP compatibility.

The owner reports an M5Stack StickS3 running ESP-Claw. The installed commit/version is unknown. Features in this source checkout must not be attributed to the installed image without checking. Prior notes also reported insufficient host USB permissions; this is not a current access check.

## Safety boundary

Repository bootstrap does not access the device or its configuration, memory, sessions, audio, or files. It does not change permissions, invoke device tools, restart, flash, or configure services. Any future device check requires a task-specific scope and should prefer non-secret status data.

## Next research candidates

Subject to a separate task: establish firmware version if exposed safely, then investigate MCP handshake and tools listing without tool calls. Keep local endpoints and identifiers outside public documentation.
