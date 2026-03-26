
## 2024-05-20 - Frictionless Context Switching via Inline Modals and Macro Injection

**Learning:** When navigating between multiple digital identities (accounts) in a restrictive ecosystem (like Riot Client), creating a distinct "Login Screen" introduces cognitive friction and breaks application momentum. Inline credential management combined with asynchronous macro injection (e.g., auto-typing) bridges the gap between secure local storage and closed systems without requiring complex API circumventions.

**Action:** For closed-loop client launchers that lack API support, manage authentication state visually within the primary interaction context (e.g., the sidebar). Use simple, deterministic macro sequences executed on a background thread (`daemon=True`) to maintain the application's responsiveness (The 100ms Law) while bridging the systemic gap.

## Omni Architecture Principles

**Learning:** The interface is an extension of the user's nervous system. Every pixel, state transition, and asynchronous operation must reduce entropy and preserve momentum.

**Action:**
- **pnpm Supremacy:** Only pnpm is valid. No npm, no yarn. Dependency graphs must remain deterministic.
- **The 100ms Law:** Interaction feedback must occur within 100ms. If backend latency exceeds this, implement Optimistic UI updates.
- **Accessibility Is Structural:** Accessibility is architecture, not a feature. WCAG AAA baseline, semantic HTML first, keyboard-first interaction model.
- **Entropy Reduction Doctrine:** Every change must reduce complexity, increase clarity, and strengthen type guarantees.
- **Execution:** Strict TypeScript only. No implicit any, no magic numbers, no silent fallthrough.
