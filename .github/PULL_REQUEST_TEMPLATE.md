## Summary
<!-- Brief description of changes -->

## Quality Gate Checklist
- [ ] # Pre-Flight Check — runtime: node

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
``` passed locally with exit code 0.
- [ ] Ponytail review was verified (no bloat, minimal diff, existing components reused).
- [ ] All environment variables are validated in  (no raw ).
- [ ] Relevant Playwright E2E or unit tests are included.
- [ ] No unapproved dependencies were introduced.
- [ ] Commit messages follow Conventional Commits format.
