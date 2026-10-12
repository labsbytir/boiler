---
name: cloudflare-edge
description: Guidelines for Cloudflare Pages, Workers, D1 SQL, KV, and Edge caching.
---

# Cloudflare Edge Development Playbook

## Guidelines
1. **Edge Cache API:** In route handlers, leverage `caches.default` and set explicit `Cache-Control` headers (`public, s-maxage=3600, stale-while-revalidate=86400`).
2. **D1 Migrations:** Run `pnpm exec wrangler d1 migrations create <name>`. Never edit committed migrations; all migrations must be idempotent.
3. **Edge Safe Code:** Do not use Node C++ native bindings or unsupported Node internals in Edge paths.
