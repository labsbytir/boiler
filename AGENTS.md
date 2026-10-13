# Agent guidance

This file contains active instructions only. `AGENTS_ARCHIVE.md` preserves former long-form guidance for reference; do not load it for routine tasks.

- Complete a coherent request in one pass. Do not impose per-pass file or line caps, ask to extend budgets, or maintain `LOOP_STATE.md`.
- Do not push or commit; the user handles Git publication.
- Do not run the full preflight gate, full test suite, browser tests, or second-model review by default. Run focused checks when needed or requested.
- Keep command output concise and local. Do not send logs to models or external services unless explicitly requested.
- Preserve unrelated worktree changes and local configuration.
- Use the package manager and language already established in the repository. Avoid adding dependencies without a clear need.
- CI and the user-triggered pre-push hook own the full quality gate.
