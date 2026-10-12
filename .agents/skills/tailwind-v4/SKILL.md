---
name: tailwind-v4
description: Tailwind CSS v4 CSS-first theming, utility patterns, and component composition.
---

# Tailwind CSS v4 Playbook

## Guidelines
1. **Zero Config Files:** Never create `tailwind.config.js`. Tailwind v4 is CSS-first.
2. **Theming:** Defined in `apps/web/app/globals.css` using `@import "tailwindcss";` and `@theme`.
3. **Class Merging:** Always use `cn(...)` from `apps/web/src/lib/utils.ts` (`clsx` + `tailwind-merge`) when writing reusable React components.
4. **Server Components:** Keep styling in Server Components; isolate client state to interactive leaves.
