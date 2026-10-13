# Agent guidance

`AGENTS_ARCHIVE.md` is historical reference; do not load it for routine tasks.

- Finish coherent requests without per-pass budgets, file caps, or `LOOP_STATE.md` updates.
- Preserve user changes and local configuration; never expose secrets.
- Do not commit or push; the user publishes changes.
- Use the smallest relevant check. CI and the user-triggered push hook run the full gate. Avoid full suites, browser tests, and second-model reviews unless requested.
- Keep logs concise and local; do not send them to models or external services unless asked.
- Use existing tools and dependencies. Avoid unnecessary dependencies.
