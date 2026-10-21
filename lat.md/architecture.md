# Architecture

The inherited ESP-Claw architecture separates the application shell, event routing, agent loop, callable capabilities, and board-specific hardware setup.

## Runtime boundaries

Inherited design guidance keeps board and feature logic outside the critical agent loop whenever an extension point suffices.

[[application/edge_agent/main/main.c]] is the application entry point. [[components/common/app_claw]] initializes agent services. [[components/claw_modules/claw_event_router]] routes incoming events; [[components/claw_modules/claw_core]] owns the agent runtime. These roles are reported by inherited [[.agents/design.md]] and [[AGENTS.md]], not established by a new runtime test.

## Extension points

Capabilities, Lua modules, skills, and board overlays are the preferred places for localized downstream adaptation.

[[components/claw_capabilities]] contains callable groups. [[components/common/app_claw/app_capabilities.c]] registers them. [[components/lua_modules]] and [[components/common/app_claw/app_lua_modules.c]] supply Lua functionality. [[application/edge_agent/boards/m5stack/m5stack_sticks3]] contains the StickS3 definition. Lua links are file-level because Lat's documented symbol-language list does not include Lua.

## Storage boundary

Inherited firmware guidance separates read-only SYSTEM content from writable DATA and requires runtime path resolution instead of fixed writable mount paths.

[[application/edge_agent/fatfs_image]] supplies build-time content. Board overlays target SYSTEM, not DATA. Reusable code must use the storage/path APIs described in [[AGENTS.md]] and [[.agents/design.md]]. This describes the source design, not a claim about the owner's installed firmware.
