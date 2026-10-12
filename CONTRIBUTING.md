# Contributing Guide

Welcome to [labsbytir/builder-repo](https://github.com/labsbytir/builder-repo).

## Workflow Rules for Humans and Agents

1. **Pull Request Workflow:** Direct pushes to `main` are protected. All contributions must be submitted via feature branches and Pull Requests.
2. **Review & Approval:** All Pull Requests require code owner review and approval prior to merge. Review requests are automatically routed according to [`.github/CODEOWNERS`](.github/CODEOWNERS).
3. **Local Pre-Flight Gate:** Always ensure quality checks pass locally before opening a pull request:
   ```bash
   pnpm run check
   ```
   This executes TypeScript typechecking, linting, unit tests, and security audits.
4. **CI Quality Gate:** All Pull Requests must pass the automated GitHub Actions `quality-gate` workflow.
5. **Conversation Resolution:** All comment threads and review discussions must be resolved prior to merging.
6. **Commit Standards:** Use Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`).
7. **Agent Protocol:** AI coding agents working in this repository MUST consult [`AGENTS.md`](AGENTS.md).
8. **License:** All contributions are submitted under the Apache License 2.0.
