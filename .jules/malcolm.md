## 2024-03-26 - Visual Consistency with Custom Components
**Learning:** Standard OS or default GUI components (like `CTkSwitch`) break visual immersion when placed alongside highly stylized, custom components (like Riot-themed `LolToggle`).
**Action:** When auditing or implementing UI features, prioritize extending and utilizing existing custom design system components over mixing default components, ensuring a cohesive and immersive user experience.
## 2024-03-27 - Inline Confirmations for Destructive Actions
**Learning:** Using inline, timed confirmations (where a button changes text and color briefly before allowing the action) avoids popup fatigue and keeps the user in their context, while still preventing accidental clicks for destructive actions like resetting settings. Coupling the successful action with a delightful feedback loop (like a Confetti Toast) makes the interaction satisfying rather than purely utilitarian.
**Action:** Default to inline, timed confirmation states for medium-risk actions (like reset, clear history, or bulk changes) instead of modal dialogues to preserve UX fluidity and increase engagement through micro-interactions.
