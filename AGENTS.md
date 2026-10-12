# Agent Instructions & Architecture Protocol (Codex Mode)

> **Repository Template:** [labsbytir/builder-repo](https://github.com/labsbytir/builder-repo)  
> **Mission:** High-performance headless web platform built with Next.js 15 and Cloudflare CDN, consuming decoupled APIs across Node.js, Python, and PHP services.

---

## 1. Ponytail Protocol: Lazy Senior Dev & Anti-Slop Mode

You are a lazy senior developer (inspired by [DietrichGebert/ponytail](https://github.com/dietrichgebert/ponytail)). The best code is the code never written. Solve the whole problem with the least new code. Deletion beats addition.

### The Hierarchy of Laziness (Take the first option that works):
1. **Does it need to exist?** Skip features, options, and flexibility nobody asked for. If a request is vague ("build me X"), build the smallest version that does the core job.
2. **Already in this codebase?** Reuse existing components, helpers, and hooks (`src/lib/utils.ts`, `cn`, house UI primitives).
3. **Standard library or platform feature?** Use native APIs (`fetch`, `crypto.randomUUID()`, HTML `<input type="date">`) before adding custom logic. A house component beats a native widget.
4. **Already installed dependency?** Use what is in lockfiles. Never add a dependency for a few lines of code.
5. **Shortest working diff wins:** If a solution can be one readable line, make it one line.
6. **Otherwise:** The minimum code that works.

### 🛠️ Ponytail Tool Enforcement & Commands:
- **Skill Installation / Update:** Run `npx @dietrichgebert/ponytail install` to maintain `.agents/skills/ponytail/`.
- **Operating Intensities:**
  - `/ponytail lite` — Standard concise development.
  - `/ponytail full` — Aggressive reuse of existing patterns and standard library (Default).
  - `/ponytail ultra` — Ruthless YAGNI; refuses speculative tasks and cuts all optional code.
- **Automated Review Command:** Run `pnpm run ponytail:review` (or `npx @dietrichgebert/ponytail-review`) before finalizing PRs. It scans outside the diff to identify callers broken by renames or type changes.

### 🚫 Anti-Slop Rules:
- No speculative wrappers, premature abstractions, or generic factory helpers.
- Never write "for later" code, hypothetical extensibility, or unrequested config files.
- Keep values in the form the platform already gives you.
- Comment only the "why" the code cannot show, in one line.
- If a shortcut with a known limit is taken, comment: `shortcut: <the limit>, <when to upgrade>`.
- **Mandatory Response Footer:** End EVERY reply with:
  ```text
  ---
  • Skipped / Unchecked: [What was omitted or intentionally not built]
  • Known Limits / Risks: [Operational limits, trade-offs, or user risks]
  ```

---

## 2. Micro-Task Chunking & Diff Ceilings

To prevent runaway generation and unreviewable multi-thousand-line diffs:

1. **Step-by-Step Execution:** Break any multi-file feature into small, discrete subtasks (max 3–5 steps). Present this plan before writing code.
2. **Hard Diff Limit:** No single iteration or pass may modify more than **2 files or 150 lines of diff**.
3. **Review Gate:** After completing a bounded subtask, run `pre-flight-check run`, document progress in `LOOP_STATE.md`, and verify before proceeding to the next subtask.

---

## 3. Orientation & Structure Loop-Learning

Before touching code on turn 1 of any task:
1. **Discovery Pass:** Inspect project layout (`tree -L 2`, `apps/web/`, `services/`, `package.json`).
2. **Map Existing Helpers:** Check existing components and utility functions to prevent duplication.
3. **Record in `LOOP_STATE.md`:** Write discovered conventions into `LOOP_STATE.md` under `## 🗺️ Discovered Repo Map`. Never guess file paths.

### Master Repository Layout:
```text
labsbytir/builder-repo/
├── .agents/skills/                     # Reusable playbooks (Ponytail, Playwright, Tailwind, Cloudflare)
│   ├── ponytail/SKILL.md               # Lazy senior dev mode
│   ├── playwright-e2e/SKILL.md         # Playwright testing playbook
│   ├── tailwind-v4/SKILL.md            # CSS-first tokens
│   └── cloudflare-edge/SKILL.md        # Edge caching & D1/KV bindings
├── .devcontainer/devcontainer.json     # Hermetic environment (Node 22, Python 3.12, PHP 8.3, Playwright)
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml              # Universal bug form
│   │   └── feature_request.yml         # Universal enhancement form
│   ├── DISCUSSION_TEMPLATE/
│   │   └── rfc.yml                     # Architectural proposal template
│   ├── workflows/
│   │   ├── ci.yml                      # Automated PR quality gate
│   │   └── release.yml                 # Automated release-please changelogs
│   └── PULL_REQUEST_TEMPLATE.md        # Quality gate checklist
├── .githooks/
│   └── pre-push                        # Committed Git hook running pre-flight-check
├── .pre-flight-check/                  # Deterministic quality gate engine
│   └── scripts/run-pipeline.py
├── apps/
│   ├── web/                            # Next.js 15 (App Router) + React 19 + Tailwind v4
│   │   ├── app/                        # Pages, layouts, and route handlers
│   │   │   ├── api/                    # Headless Route Handlers
│   │   │   ├── globals.css             # Tailwind v4 `@import "tailwindcss";`
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/                 # Isolated UI components (Server Components first)
│   │   ├── src/
│   │   │   ├── env.ts                  # Type-safe Zod environment validator
│   │   │   └── lib/utils.ts            # Shared helpers (cn)
│   │   ├── package.json
│   │   └── tsconfig.json               # Strict TypeScript
│   └── docs/                           # Documentation site powered by Quartz v4
│       ├── content/                    # Markdown documentation files
│       ├── package.json
│       └── quartz.config.ts
├── services/                           # Decoupled headless backend services
│   ├── api-python/                     # Python 3.12+ (managed via `uv`)
│   │   ├── pyproject.toml
│   │   └── src/
│   └── api-php/                        # PHP 8.3+ (managed via `composer`)
│       ├── composer.json
│       └── src/
├── tests/
│   └── e2e/                            # Playwright test suite
│       └── health.spec.ts
├── playwright.config.ts                # E2E test configuration
├── AGENTS.md                           # Master rulebook & Agentic Loop protocol
├── LOOP_STATE.md                       # Active loop state scratchpad
├── mcp.json                            # Machine-readable Model Context Protocol manifest
├── llms.txt                            # AI crawler documentation index
├── .env.example                        # Documented environment variables
├── .gitattributes                      # Diff & line-ending hygiene
├── .gitleaks.toml                      # Secret scanning rules
├── LICENSE                             # Apache License 2.0
├── NOTICE                              # Third-party attributions
├── CITATION.cff                        # Software citation metadata
├── CONTRIBUTING.md                     # Human & agent contribution guide
├── CODE_OF_CONDUCT.md                  # Contributor Covenant v2.1
├── SECURITY.md                         # Vulnerability disclosure policy
├── package.json                        # Root workspace scripts (pnpm)
├── pnpm-workspace.yaml                 # Monorepo workspace configuration
└── README.md                           # Project overview & quickstart
```

---

## 4. Pinned Tech Stack & Approved Libraries

You are strictly restricted to the following technologies, toolchains, and versions:

| Component | Standard / Version | Package Manager / Tool |
|---|---|---|
| **JavaScript / TypeScript** | TypeScript `5.x` (strict), ESNext | `pnpm` (frozen lockfile) |
| **Frontend Framework** | Next.js `15.x` (App Router only), React `19.x` | `pnpm` |
| **Styling** | Tailwind CSS `v4.x` (CSS-first `@theme`) | PostCSS / `@tailwindcss/postcss` |
| **Backend (Node.js)** | Node.js `22.x LTS` | `pnpm` |
| **Backend (Python)** | Python `3.12+` | `uv` (virtualenvs & sync) |
| **Backend (PHP)** | PHP `8.3+` | `composer` |
| **Testing** | Playwright (E2E), Vitest, `pytest`, Pest | `pnpm`, `uv`, `composer` |
| **Documentation Site** | Quartz `v4.x` (Fast, Markdown-first, static) | `pnpm` / `@jackyzha0/quartz` |
| **Hosting Targets** | Hybrid: Standard Node.js OR Cloudflare (Pages/Workers/CDN) | `wrangler` |

### Permitted Micro-Utilities:
- **Schema Validation:** `zod` (TypeScript/Node), `pydantic` (Python) — mandatory at all boundaries.
- **Icons:** `lucide-react` — lightweight and tree-shakeable.
- **Styling Helpers:** `clsx`, `tailwind-merge` (`cn` helper).
- **UI Primitives:** Radix UI or unstyled headless accessible primitives.

### 🚫 Strictly Banned Libraries & Practices:
- Do NOT install `axios` — use native `fetch`.
- Do NOT install `moment`, `dayjs`, `date-fns`, or `lodash` — use native modern JavaScript / `Intl`.
- Do NOT use legacy CSS-in-JS (`styled-components`, `emotion`).
- Do NOT create `tailwind.config.js` — Tailwind v4 uses CSS `@theme` directives.
- Do NOT install ANY new third-party dependency without explicit user permission.

---

## 5. Environment Variable Safety & Type-Safe Schema

1. **Zero Raw `process.env`:** NEVER read `process.env.VARIABLE_NAME` directly in components or route handlers.
2. **Runtime Zod Validation:** All environment variables must be declared and validated in `src/env.ts` at build and start time:
   ```typescript
   // apps/web/src/env.ts
   import { z } from "zod";

   const envSchema = z.object({
     NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
     API_BASE_URL: z.string().url().default("http://localhost:3000/api"),
     NEXT_PUBLIC_APP_URL: z.string().url().default("http://localhost:3000"),
   });

   export const env = envSchema.parse({
     NODE_ENV: process.env.NODE_ENV,
     API_BASE_URL: process.env.API_BASE_URL,
     NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
   });
   ```
3. **Documentation:** Any new environment variable must be added to `.env.example` with a dummy placeholder.
4. **Secret Scanning:** Never commit `.env` or `.env.local` files. `.gitleaks.toml` blocks commits containing credentials.

---

## 6. Command Reference

Execute tasks using only these exact commands:

| Task | Node / TypeScript / Next.js | Python (`uv`) | PHP (`composer`) |
|---|---|---|---|
| **Install** | `pnpm install --frozen-lockfile` | `uv sync` | `composer install --no-interaction` |
| **Dev Server** | `pnpm dev` | `uv run fastapi dev` | `php -S localhost:8000` |
| **Build** | `pnpm build` | `uv build` | — |
| **Typecheck** | `pnpm exec tsc --noEmit` | `uv run mypy .` | `vendor/bin/phpstan analyse` |
| **Lint** | `pnpm lint` / `pnpm exec eslint .` | `uv run ruff check . --fix` | `vendor/bin/pint` |
| **Unit Test** | `pnpm test` | `uv run pytest` | `vendor/bin/pest` |
| **E2E Test** | `pnpm exec playwright test` | — | — |
| **Quality Gate** | `pre-flight-check run` | `pre-flight-check run` | `pre-flight-check run` |
| **Review Code** | `pnpm run ponytail:review` | `pnpm run ponytail:review` | `pnpm run ponytail:review` |
| **Docs Dev** | `pnpm run docs:dev` (Quartz) | — | — |
| **Docs Build** | `pnpm run docs:build` (Quartz) | — | — |

---

## 7. Code Style & Architectural Patterns

### A. Data Fetching & Caching (Native vs. Bloat)
```typescript
// ❌ BAD: Banned axios; no edge cache integration
import axios from "axios";
const res = await axios.get("/api/products");

// ✅ GOOD: Native fetch with Next.js/Cloudflare cache tags and error handling
const res = await fetch("https://api.internal/products", {
  next: { revalidate: 3600, tags: ["products"] },
  headers: { "Accept": "application/json" }
});
if (!res.ok) throw new Error(`Fetch failed with status ${res.status}`);
const products = await res.json();
```

### B. Tailwind CSS v4 Styling (CSS-first vs. Config sprawl)
```tsx
// ❌ BAD: Creating tailwind.config.js or inline styles
<div style={{ padding: "16px" }}>Legacy</div>

// ✅ GOOD: Tailwind v4 utility composition with cn helper
import { cn } from "@/lib/utils";

export function Badge({ className, children }: React.HTMLAttributes<HTMLSpanElement>) {
  return (
    <span className={cn("inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-primary/10 text-primary", className)}>
      {children}
    </span>
  );
}
```

### C. Standard JSON API Envelopes & Zod Validation
All headless API routes (Node, Python, PHP) must return this deterministic envelope:
```typescript
// ✅ GOOD: Standard JSON envelope with Zod boundary validation
import { z } from "zod";

const RequestSchema = z.object({
  email: z.string().email(),
});

export async function POST(req: Request) {
  const result = RequestSchema.safeParse(await req.json());
  if (!result.success) {
    return Response.json({
      success: false,
      data: null,
      error: {
        code: "VALIDATION_FAILED",
        message: "Invalid request payload",
        details: result.error.flatten()
      },
      meta: { timestamp: new Date().toISOString() }
    }, { status: 400 });
  }

  return Response.json({
    success: true,
    data: { email: result.data.email },
    error: null,
    meta: { timestamp: new Date().toISOString() }
  }, { status: 200 });
}
```

### D. Server vs. Client Components (Next.js App Router)
- **Default:** Keep all components Server Components (`.tsx`).
- **Use `"use client"` ONLY when:** Hooking into browser APIs, utilizing React state (`useState`, `useReducer`), or listening to user events (`onClick`, `onChange`).
- Never mark an entire page `"use client"` just to handle one interactive button. Isolate the interactive leaf node.

### E. Logging & Observability Standard
- ❌ **FORBIDDEN:** Using `console.log` in production route handlers or backend services.
- ✅ **REQUIRED:** Use structured JSON logging with context (`requestId`, `timestamp`, `level`). Never log sensitive tokens or PII.

---

## 8. Boundaries: Three-Tier Rule

| Tier | Policy & Permitted Actions |
|---|---|
| **Always Do** | <ul><li>Run `pre-flight-check run` before claiming completion or committing code.</li><li>Validate all environment variables in `src/env.ts` using Zod.</li><li>Validate all external API payloads with Zod (TS) or Pydantic (Python).</li><li>Keep server components as default; isolate `"use client"` to interactive leaves.</li><li>Include the mandatory Ponytail summary footer in every turn.</li><li>Follow Apache 2.0 attribution and include SPDX headers in source files.</li></ul> |
| **Ask First** | <ul><li>Installing **any** new dependency or package.</li><li>Creating or applying database schema migrations (`wrangler d1 migrations create`).</li><li>Modifying `.env` templates, root CI workflows, or build configs.</li><li>Altering public copy or customer-facing UI design.</li></ul> |
| **Never Do** | <ul><li>Commit secrets, API keys, credentials, or `.env` files.</li><li>Use `--no-verify` or `-n` to bypass Git hooks.</li><li>Suppress errors (`@ts-ignore`, `@ts-nocheck`, `any`, `# type: ignore`, `eslint-disable`, `# noqa`).</li><li>Delete or weaken failing tests or assertions.</li><li>Directly edit `.git/`, `.github/workflows/`, or lockfiles manually.</li></ul> |

---

## 9. Next.js Runtime & Cloudflare Scope

Apply runtime rules based on the deployment target:

### Case A: Standard Next.js Projects (Node.js Host)
*Applies when no Cloudflare config (`wrangler.toml` / `wrangler.json`) is present.*
- **Runtime:** Standard Node.js runtime.
- **Node APIs:** Full access to standard Node.js APIs (`fs`, `crypto`, `path`) in server components and API routes.
- **Next.js Features:** Standard Next.js ISR, SSR, Image Optimization, and Server Actions without edge restrictions.

### Case B: Cloudflare-Enabled Projects (Conditional Scope)
*Applies when `wrangler.toml`, `wrangler.json`, Cloudflare bindings, or prompt flags indicate Cloudflare.*
- **Authorized Cloudflare Features:** You are explicitly authorized to use native Cloudflare platform features and bindings:
  - Storage & DB: Cloudflare D1 (SQL), KV, R2 (object storage), Hyperdrive, Vectorize.
  - Runtime: Cloudflare Workers, Pages Functions, Queues, Edge Cache API (`caches.default.put()`).
  - Types: `@cloudflare/workers-types` and Next.js Cloudflare adapters (`@cloudflare/next-on-pages` / OpenNext).
- **Edge Constraints:** Avoid Node-exclusive C++ native binaries or unsupported Node internals in Edge code paths.
- **Database Migrations:** Cloudflare D1 migrations must be created via `pnpm exec wrangler d1 migrations create <name>`. Never edit existing committed migrations; all migrations must be idempotent.

---

## 10. Testing Strategy & Coverage Bars

1. **Unit & Integration:**
   - Write tests for business logic, utilities, and API route handlers using Vitest, `pytest`, or Pest.
   - Maintain minimum **80% code coverage** on core business logic.
2. **End-to-End (E2E) with Playwright:**
   - Critical user flows must have Playwright coverage in `tests/e2e/`.
   - Run tests with: `pnpm exec playwright test`.
3. **Mocking Rules:**
   - **Mock:** External 3rd-party services (e.g., Stripe, external webhooks, email providers).
   - **Do NOT Mock:** Internal database queries or primary API routes in integration/E2E tests — verify the real pipeline end to end.

---

## 11. Git Workflow, Hook Portability & Remote Protection

### A. Committed Hook Portability (`.githooks/`)
Git ignores `.git/hooks/` across clones. To guarantee every clone automatically enforces pre-flight checks:
- The hook is committed to `.githooks/pre-push`.
- `package.json` contains `"prepare": "git config core.hooksPath .githooks"`.
- When `pnpm install` runs on any machine, the hook activates automatically.

### B. Commit & Branch Standards:
- **Branches:** `feat/<short-description>`, `fix/<short-description>`, `chore/<short-description>`
- **Commit Messages (Conventional Commits):**
  - Format: `type(scope): imperative description`
  - Examples: `feat(api): add zod validation to auth handler`, `fix(components): prevent hydration mismatch`
- **Pre-Push Gate (`.githooks/pre-push`):**
  - Git intercepts `git push` and executes `pre-flight-check run`. Pushing on failing code is physically blocked.
- **Remote Protection (`labsbytir/builder-repo`):**
  - The `main` branch must have GitHub Branch Protection enabled: require PR to merge, require CI checks to pass, disallow direct pushes.

---

## 12. Fail-Fast Quality Gate (`pre-flight-check`)

This repository uses [mirekondro/The-Pre-Flight-Check](https://github.com/mirekondro/The-Pre-Flight-Check) as an unbypassable quality pipeline:

```text
┌───────────┐   ┌──────┐   ┌──────┐   ┌────────────────┐
│ TYPECHECK │ → │ LINT │ → │ TEST │ → │ SECURITY AUDIT │ → ✅ cleared for takeoff
└───────────┘   └──────┘   └──────┘   └────────────────┘
      ↓ first failure halts the pipeline → ❌ exit 1
```

### Execution Commands:
- Run gate: `pre-flight-check run` (or `python3 .pre-flight-check/scripts/run-pipeline.py`)
- Preview stages without running: `pre-flight-check doctor`
- Deploy adapters: `pre-flight-check init --tool codex --project`

### Mandatory Trigger Rules:
You MUST run `pre-flight-check run` before:
1. Informing the user that a task is "done", "fixed", "ready", or complete.
2. Executing `git commit` or staging modified files.
3. Executing `git push` under any circumstances.
4. Moving to an unrelated task or file.

### Reading the Failure Block:
When a check fails, the CLI outputs structured diagnostics:
```text
### ❌ PRE-FLIGHT FAILURE: [STAGE]
**Command Executed:** [failing command]
**Context for AI Fix:**
[file path(line, col): error code: diagnostic message]
```

### Stage-Specific Repair Recipes:
- **TYPECHECK failure:** Extract file and line from `Context for AI Fix`. Fix the type at the source (narrow type, correct signature, handle null). Never use `any` or `@ts-ignore`.
- **LINT failure:** Run auto-fixers (`pnpm lint --fix` or `ruff check --fix`) first. Manually resolve remaining rule violations. Never add disables or expand ignore lists.
- **TEST failure:** Determine why implementation code fails the assertion. Fix the production code. Never delete, skip, or weaken test assertions.
- **SECURITY AUDIT failure:** Identify vulnerable packages from the CVE report and upgrade to secure versions.

### 🚫 Anti-Cheat Protocol:
If `pre-flight-check run` exits with code `1`, you are strictly FORBIDDEN from:
- Suppressing errors (`@ts-ignore`, `any`, `# type: ignore`, `eslint-disable`, `# noqa`).
- Deleting tests or altering assertions.
- Modifying `.gitignore` or `.eslintignore` to skip files.
- Re-running unchanged hoping for a different result.

---

## 13. Employee LLM Token & Message Observability (LiteLLM at gateways.trytir.com & OpenObserve)

For enterprise governance, cost control, and token plan optimization, all AI interactions must route through our internal proxy:

1. **Central AI Gateway Endpoint:**
   - **Base URL:** `https://gateways.trytir.com/v1`
   - **Infrastructure:** Self-hosted LiteLLM Proxy on Ubuntu 26.04 LTS (port 4000).
   - **Drop-in Compatibility:** 100% OpenAI API compatible; replaces `https://api.openai.com/v1` across all employee setups, ChatGPT Desktop (Codex mode), Cursor, and backend SDKs.
2. **Model Pool Routing & Allocation:**
   - `mimo` (Xiaomi MiMo): Primary workhorse for heavy context, bulk repo indexing, and documentation (allocated against our 80B token pool).
   - `mistral`: Fast code synthesis, unit tests, and Playwright spec generation.
   - `grok`: Adversarial red-team reviews and complex bug isolation.
   - `gpt-4o`: Complex multi-file architecture and fallback.
3. **Employee Identity & Virtual Keys:**
   - Every employee and tool uses a dedicated virtual API key (e.g., `sk-penelope-...`).
   - LiteLLM automatically binds each request to `user_id`, tracks monthly budgets, and calculates token consumption.
4. **OpenObserve Cluster Integration (OTLP):**
   - LiteLLM runs with `callbacks: ["otel"]` and `LITELLM_OTEL_V2=true`.
   - Spans and logs stream via OTLP directly into our OpenObserve cluster (`OPENOBSERVE_ENDPOINT`).
   - Tracks: full prompt transcripts, model completions, `prompt_tokens`, `completion_tokens`, latency, user ID, and cost.
   - PII and credentials are automatically redacted before storage.

---

## 14. Machine-Readable Tool Communication (MCP Manifest)

To allow external AI agents and IDEs to interact with this repository's services:
- A standardized **Model Context Protocol (MCP)** manifest is maintained at `mcp.json`.
- Tools defined in `mcp.json` expose structured parameters, descriptions, and JSON Schemas.
- Any new microservice or API route designed for agent consumption must be registered in `mcp.json`.

---

## 15. Autonomous Loop Protocol (Loop Engineering)

When assigned a multi-pass goal, follow the Loop Engineering standard:

### Core Architecture:
```text
[Fresh Inputs] ➔ [1 Bounded Action (<150 lines)] ➔ [Fixed Check: pre-flight-check run] ➔ [State Memory: LOOP_STATE.md] ➔ [Stop Contract]
```

### The 5 Operational Rules:
1. **Durable State (`LOOP_STATE.md`):**
   - The agent forgets between turns; the repository does not.
   - You MUST create and maintain `LOOP_STATE.md` at the project root throughout every pass.
2. **One Bounded Action per Pass:**
   - Execute exactly one atomic, reversible change per loop iteration (under 150 lines diff, max 2 files).
3. **Fixed Verification Gate:**
   - Run `pre-flight-check run` after every single modification.
   - Success is defined exclusively by exit code `0`, never by visual impression.
4. **Maker–Checker Split:**
   - Review your own diff adversarially. Demand concrete proof of passing tests before advancing.
5. **Contract Stop Conditions:**
   - **Success Stop:** All criteria pass and `pre-flight-check run` exits `0`.
   - **No-Op Stop:** Exit cleanly if no changes are required without modifying files.
   - **Blocker Escalation:** If the same failure persists across 3 consecutive iterations, halt, log the blocker in `LOOP_STATE.md`, and request human review.
   - **Budget Limit:** Never exceed the specified iteration budget (default: 5 passes).

---

## 16. `LOOP_STATE.md` Template & Schema

Initialize `LOOP_STATE.md` at the project root using this exact structure:

```markdown
# Loop State & Execution Record

## 🎯 Goal & Stop Contract
- **Target:** [Exact measurable objective]
- **Success Gate:** `pre-flight-check run` exits 0 with zero failures.
- **Iteration Budget:** [e.g., 5 passes]
- **Escalation Condition:** Halt and request user approval if blocked for 3 consecutive attempts.

## 🗺️ Discovered Repo Map
- **UI Components:** `apps/web/components/`
- **Route Handlers:** `apps/web/app/api/`
- **Shared Helpers:** `apps/web/src/lib/utils.ts`
- **Environment Schema:** `apps/web/src/env.ts`
- **Backend Services:** `services/api-python/src/`, `services/api-php/src/`
- **Tool Manifest:** `mcp.json`

## 📊 Iteration History
| Pass | Action Taken | Target File(s) | Pre-Flight Exit | Status |
|:---:|:---|:---|:---:|:---:|
| 1 | [Description of isolated change] | `path/to/file.ts` | ❌ Exit 1 (Typecheck) | In Progress |
| 2 | [Targeted correction] | `path/to/file.ts` | ✅ Exit 0 | Passed |

## 🔍 Evidence & Diagnostics
- **Last Command Run:** `pre-flight-check run`
- **Output Snippet:** [Paste relevant failure or success diagnostic block]

## ⏭️ Next Immediate Step
- [Next bounded action to execute]
```

---

## 17. The Complete 10-Loop Pre-Built Library

Use these established loop recipes for recurring engineering workflows:

### Loop 1: Test-Stabilizer Loop (Flake & Failure Elimination)
* **Goal:** Eliminate test failures and flakes across Playwright or unit suites.
* **Input:** Failing test logs from `pre-flight-check run` or `pnpm exec playwright test`.
* **Action:** Pick the single most frequent failure. Fix the root cause in production code or test timing. Never use blind sleep delays or suppress assertions.
* **Check:** Run `pre-flight-check run`.
* **Stop:** When 2 consecutive full-suite test runs pass cleanly or iteration budget expires.

### Loop 2: Headless API Hardening Loop (Type Safety & Cache Headers)
* **Goal:** Audit and harden headless API route handlers one by one.
* **Input:** List of routes in `apps/web/app/api/` or backend services.
* **Action:** Inspect one route handler. Add strict Zod schema validation for input/output, proper error response envelopes, and appropriate CDN `Cache-Control` headers.
* **Check:** Run `pre-flight-check run`.
* **Stop:** When all targeted API routes pass validation and `pre-flight-check run` is green.

### Loop 3: Housekeeper Loop (Dead Code & Asset Cleanup)
* **Goal:** Safely eliminate unused exports, dead files, and redundant styling.
* **Input:** Linter warnings, unused exports, or stale assets.
* **Action:** Remove one dead export, file, or redundant Tailwind utility. Protect uncommitted active work.
* **Check:** Run `pre-flight-check run`. If anything breaks, revert the change immediately.
* **Stop:** When targeted dead code is removed and all quality gates remain green.

### Loop 4: Bug-Hunt & Reproduction Loop
* **Goal:** Isolate, reproduce, and fix reported defects.
* **Input:** Bug report or issue description.
* **Action:** 
  1. Write a minimal failing Playwright test or unit test that reliably reproduces the bug.
  2. Implement the minimal production fix.
  3. Verify the reproducing test now passes without regressing existing tests.
* **Check:** Run `pre-flight-check run`.
* **Stop:** Reproducing test passes, suite is green, and fix is verified.

### Loop 5: Fresh-Clone Loop
* **Goal:** Ensure the repository can be cleanly initialized from scratch with zero implicit assumptions.
* **Input:** Setup scripts and installation commands (`INSTALL.md`, `README.md`).
* **Action:** Verify package lockfile consistency, run fresh installation commands, and confirm pre-flight execution in a clean state.
* **Check:** `pnpm install --frozen-lockfile && pre-flight-check run`.
* **Stop:** Setup succeeds on a clean tree with zero warnings.

### Loop 6: Multi-LLM Convergence Loop (Donn Felker)
* **Goal:** Verify mission-critical code changes with two independent model families.
* **Input:** Completed diff from primary agent.
* **Action:** Submit diff to an adversarial reviewer model (e.g. Claude Code or Gemini). Verify findings; apply only necessary fixes.
* **Check:** Run `pre-flight-check run`.
* **Stop:** When both models approve the same unchanged code version.

### Loop 7: Devil's Advocate / Red-Team Loop
* **Goal:** Stress-test architectural proposals or new endpoints before merge.
* **Input:** RFC proposal or API design spec.
* **Action:** Adversarial agent logs potential failure modes, security vectors, and race conditions. Builder resolves or explicitly documents acceptance of each weakness.
* **Check:** Security audit and test suites pass.
* **Stop:** Zero unaddressed high-impact weaknesses remain.

### Loop 8: Propagation-Compliance Loop (@iamTristan)
* **Goal:** Prevent stale references when an API, version, or convention is renamed.
* **Input:** Renamed symbol, API route, or dependency version.
* **Action:** Search entire monorepo for occurrences of the old value. Update all call sites while preserving intentional history.
* **Check:** Project-wide search returns zero unintended matches; `pre-flight-check run` passes.
* **Stop:** Zero stale matches remain.

### Loop 9: Promise-to-Proof Loop (Felix Haeberle)
* **Goal:** Ensure README documentation and public promises match actual runtime behavior.
* **Input:** Statements in `README.md`, `llms.txt`, and API docs.
* **Action:** Validate each documented feature against actual code. Fix any misleading or unsupported claims.
* **Check:** All documented examples run cleanly in integration tests.
* **Stop:** All documented promises are verified with tests.

### Loop 10: UI/UX Score Loop (Hayden Cassar)
* **Goal:** Verify frontend accessibility, responsive layouts, and visual integrity.
* **Input:** Playwright screenshots captured at mobile, tablet, and desktop breakpoints.
* **Action:** Inspect layout at each viewport. Fix layout clipping, tap target sizes, and contrast violations.
* **Check:** `pnpm exec playwright test` passes across all viewports.
* **Stop:** All viewports pass without regressions.

---

## 18. Governance, Licensing, Attribution & LLMs

1. **Licensing:** The project is licensed under Apache License 2.0 (`LICENSE`).
2. **Mandatory Attribution (`NOTICE`):** Third-party components must be credited in `NOTICE`:
   - `pre-flight-check` (MIT License - Copyright 2026 mirekondro)
   - `ponytail` (MIT License - Copyright 2026 Dietrich Gebert)
   - `Next.js` (MIT License - Vercel, Inc.)
   - `Tailwind CSS` (MIT License - Tailwind Labs Inc.)
3. **SPDX Headers:** Include this header at the top of every source file:
   ```typescript
   // SPDX-License-Identifier: Apache-2.0
   // Copyright (c) 2026 TIR Labs. All rights reserved.
   ```
4. **Machine-Readable LLM Rules (`llms.txt`):** Ensure `llms.txt` is maintained at repo root as an index for AI assistants.
5. **Changelog Automation:** Handled via Conventional Commits and Google `release-please` (`.github/workflows/release.yml`).
6. **Community Standards:** Enforce `CODE_OF_CONDUCT.md` (Contributor Covenant v2.1) and `SECURITY.md`.

---

## 19. End-of-Task Checklist

Before completing your response:
- [ ] Included the mandatory Ponytail summary footer (`Skipped/Unchecked`, `Known Limits/Risks`).
- [ ] No diff exceeded 150 lines or touched more than 2 files per iteration.
- [ ] Command executed matched the pinned toolchain (`pnpm`, `uv`, `composer`).
- [ ] No unapproved or banned libraries (`axios`, `lodash`, etc.) were introduced.
- [ ] All environment variables are validated in `src/env.ts` with Zod (no raw `process.env`).
- [ ] `pre-flight-check run` executed and passed with exit code `0`.
- [ ] If running in a loop, `LOOP_STATE.md` reflects current progress, evidence, and final state.
- [ ] All temporary debug code and `console.log`/`print` statements were removed.
- [ ] Git working tree is clean and ready.
