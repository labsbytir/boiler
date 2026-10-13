# builder-repo

> **Canonical Template:** [https://github.com/labsbytir/builder-repo](https://github.com/labsbytir/builder-repo)  
> High-performance headless web platform on Next.js 15, React 19, Tailwind CSS v4, and Cloudflare CDN, consuming decoupled APIs across Node.js, Python, and PHP services.

---

## ⚡ Quick Start

```bash
# 1. Install dependencies & register Git pre-push hooks automatically
pnpm install

# 2. Run the deterministic pre-flight check gate (Typecheck → Lint → Test → Audit)
pnpm run lint

# 3. Start development
pnpm run dev
```

---

## 🤖 Agentic Architecture & Governance

- **Agent guidance:** See [AGENTS.md](AGENTS.md) for concise active rules.
- **Quality gate:** The full gate runs in CI and the user-triggered pre-push hook.
- **Anti-Slop Protocol:** Enforces [DietrichGebert/ponytail](https://github.com/dietrichgebert/ponytail) lazy senior dev heuristics.
- **Machine-Readable API:** Defined via [mcp.json](mcp.json).
- **AI Documentation Index:** See [llms.txt](llms.txt).
- **Licensing:** Licensed under Apache License 2.0 (see [LICENSE](LICENSE) and [NOTICE](NOTICE)).
