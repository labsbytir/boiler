# Agent guidance

`AGENTS_ARCHIVE.md` is historical reference; do not load it for routine tasks.

- Finish a coherent request without per-pass budgets, file caps, or `LOOP_STATE.md` updates.
- Preserve existing user changes and local configuration. Never expose secrets.
- Do not commit or push; the user publishes changes.
- Use the smallest relevant check. Leave full gates, full suites, and browser tests to CI or an explicit request.
- Keep logs concise and local; do not send them to models or external services unless asked.
- Use existing tools and dependencies. Avoid unnecessary dependencies.
