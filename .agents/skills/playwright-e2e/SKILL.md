---
name: playwright-e2e
description: How to write, debug, and run Playwright end-to-end tests in builder-repo.
---

# Playwright E2E Testing Playbook

## Guidelines
1. Tests live in `tests/e2e/*.spec.ts`.
2. Run tests via `pnpm exec playwright test`.
3. Critical flows requiring coverage:
   - Auth & Session handshakes.
   - Core product navigation & page loads.
   - API error responses and validation displays.
4. **Mocking Rule:**
   - Mock external 3rd-party providers (Stripe, external webhooks).
   - Never mock internal database or API endpoints in E2E tests — verify the real pipeline.
