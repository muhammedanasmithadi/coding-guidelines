# 28 Frontend architecture

- Component boundaries: one component owns one UI concept; container/view split only when state sharing demands it; no prop drilling beyond 2 levels.
- State: server state via query cache with explicit stale/invalidation; local UI state stays local; global state minimal and typed.
- Rendering budgets: no render-blocking work; memoize expensive computations; virtualize long lists; avoid layout thrash; profile rendering with the chosen framework's tools.
- Accessibility is a gate: real elements, focus, `aria-live`, keyboard paths (see `docs/18-a11y.md`).
- Internationalization per `docs/19-i18n.md`; pseudo-loc and RTL in CI.
- Performance: bundle budgets (`checks/performance-budgets.md`), Lighthouse CWV, route-level code splitting, images with dimensions + modern formats.
- Check: `tsc --noEmit`, eslint/oxlint, component tests (Testing Library or equivalent) with a JS runner, Playwright E2E for critical journeys, axe 0 critical/serious, Lighthouse a11y category, bundle analyzer and pseudo-loc/RTL snapshots in CI.
- Sources: MDN https://developer.mozilla.org/en-US/docs/Web, Web.dev https://web.dev/, WCAG 2.2 https://www.w3.org/TR/WCAG22/
- Waivers: `docs/waivers.md`.

## Examples

- `examples/good-vs-bad/ai-slop.md` (agent failure modes in this area)

- `examples/good-vs-bad/a11y-i18n.md` (WCAG, ICU, UTC)
- `examples/good-vs-bad/typescript.md` (narrowing, strict)
- `examples/good-vs-bad/typescript-robust.md` (caller tests, exhaustive `never`)
- `checks/performance-budgets.md` (bundle, CWV)

Sources: MDN https://developer.mozilla.org/en-US/docs/Web, Web.dev https://web.dev/, WCAG 2.2 https://www.w3.org/TR/WCAG22/
