# Contributing Guide

Welcome to [labsbytir/builder-repo](https://github.com/labsbytir/builder-repo).

## Workflow Rules for Humans and Agents
1. **Agent Protocol:** All AI coding agents MUST read [AGENTS.md](AGENTS.md).
2. **Local Pre-Flight Gate:** Always run # Pre-Flight Check — runtime: node

→ [TYPECHECK] npx --no-install tsc --noEmit

### ❌ PRE-FLIGHT FAILURE: TYPECHECK
**Command Executed:** `npx --no-install tsc --noEmit`
**Context for AI Fix:**

```
[41m                                                                               [0m
[41m[37m                This is not the tsc command you are looking for                [0m
[41m                                                                               [0m

To get access to the TypeScript compiler, [34mtsc[0m, from the command line either:

- Use [1mnpm install typescript[0m to first add TypeScript to your project [1mbefore[0m using npx
- Use [1myarn[0m to avoid accidentally running code from un-installed packages
``` before opening a pull request.
3. **Commit Standards:** Use Conventional Commits (, , ).
4. **License:** All contributions are submitted under the Apache License 2.0.
