## Context

The family calendar is a Flask + Jinja2 app with a single hand-written `style.css`. There is no CSS framework. The current CSS uses a flat blue (`#3a7bd5`) palette with system fonts and no custom properties. All templates extend `base.html`. The ui-ux-pro-max design system recommended a warm teal palette (Micro-interactions style), Caveat + Quicksand fonts, and SVG icons over emojis.

## Goals / Non-Goals

**Goals:**
- Introduce CSS custom properties as a design token layer so colors and typography are changed in one place
- Swap Google Fonts (Caveat for headings, Quicksand for body) via a single `<link>` in `base.html`
- Replace every emoji icon in templates with an inline SVG from Lucide (calendar, broom, message-circle, x)
- Improve calendar grid readability: taller cells, entry dot indicator, today ring highlight
- Improve day view: card spacing, SVG icons per section, empty state copy, add-entry form polish
- Add micro-interactions via CSS transitions (no JS required except the submit-button loading state)
- Meet the ui-ux-pro-max pre-delivery checklist: `cursor-pointer`, focus rings, 4.5:1 contrast, `prefers-reduced-motion`

**Non-Goals:**
- No backend or database changes
- No JavaScript framework or bundler introduced
- No dark mode (out of scope for this iteration)
- No change to authentication logic or session handling

## Decisions

### D1: CSS custom properties, no framework
**Decision:** Rewrite `style.css` using CSS custom properties (`--color-primary`, `--font-heading`, etc.) as a token layer. Do not introduce Tailwind or any framework.

**Why:** The app already has a single CSS file. Introducing a framework adds build complexity that isn't justified for a small personal app. CSS variables give us the token layer benefits (one-place color changes) without new tooling.

**Alternative considered:** Tailwind via CDN. Rejected — it would require rewriting all templates and adds an external CDN dependency for a tool the user isn't familiar with yet.

### D2: Lucide SVG icons inlined in templates
**Decision:** Replace emoji icons with inline SVG (Lucide) directly in Jinja2 templates.

**Why:** Emojis render inconsistently across OS/browsers, can't be styled with CSS (color, size), and violate the ui-ux-pro-max "no-emoji-icons" rule. Inline SVG needs no extra dependency.

**Alternative considered:** Icon font (Font Awesome CDN). Rejected — adds an extra network request and is harder to customize per instance.

### D3: Submit button loading state via vanilla JS
**Decision:** A small `<script>` tag on the day view page disables the submit button and shows "Adding…" text on form submit.

**Why:** Prevents double-submissions and provides clear feedback. Requires ~5 lines of JS — no framework needed.

## Risks / Trade-offs

- **Google Fonts network dependency** → If offline, fonts fall back to system fonts gracefully (CSS `font-family` fallback stack included). Risk: low.
- **Full CSS rewrite** → Any undiscovered edge-case styles may be lost. Mitigation: test all three pages (login, calendar, day view) after rewrite.
- **Caveat + Quicksand readability** → Handwritten-style fonts can be less legible at small sizes. Mitigation: Caveat used only for the site title and page headings (≥1.1rem); Quicksand for body text is highly legible.
