## 1. Design Tokens & Fonts

- [x] 1.1 Rewrite `app/static/style.css` — add `:root` block with all CSS custom properties (colors, fonts, radius, shadows)
- [x] 1.2 Add Google Fonts `<link>` for Caveat + Quicksand in `app/templates/base.html`
- [x] 1.3 Update `body` rule in CSS to use `--font-body`, `--color-bg`, `--color-text`, `line-height: 1.6`
- [x] 1.4 Replace emoji site-title `📅` in `base.html` header with an inline Lucide calendar SVG

## 2. Header & Global Layout

- [x] 2.1 Update `header` CSS to use `--color-primary` background and `--font-heading` for site title
- [x] 2.2 Add `cursor-pointer` and hover transition to nav links in header
- [x] 2.3 Ensure `main` max-width and padding are unchanged (600px, 16px)

## 3. Calendar Grid

- [x] 3.1 Update `table.calendar td` min-height to 56px and center content with flexbox
- [x] 3.2 Add today-highlight style: ring border in `--color-primary`, bold day number (requires `td.today` class in template)
- [x] 3.3 Update `calendar.html` to add `today` class to the current day's `<td>`
- [x] 3.4 Replace `.has-entries` background fill with a dot indicator: small `::after` pseudo-element (6px circle, `--color-secondary`)
- [x] 3.5 Add hover state to day cells: light teal tint background + `cursor-pointer`, transition 150ms
- [x] 3.6 Update calendar header nav-buttons to use `--color-primary` border and hover state

## 4. Day View

- [x] 4.1 Replace emoji icons in `day.html` entry_list calls with inline Lucide SVGs (calendar, brush, message-circle)
- [x] 4.2 Replace `✕` delete button character with Lucide `x` SVG and add `aria-label="Delete entry"`
- [x] 4.3 Update empty state copy to "Nothing here yet." in `--color-text-muted`
- [x] 4.4 Add visible focus ring (2px `--color-primary` outline) to select and textarea in add-entry form CSS
- [x] 4.5 Add inline `<script>` to `day.html` for submit button loading state (disable + "Adding…" on submit)
- [x] 4.6 Update `.entry-section` card CSS to use `--shadow-sm`, `--radius`, `--color-border`

## 5. Login Page

- [x] 5.1 Update `.login-wrapper` CSS to use `--shadow-md`, `--radius`, `--color-surface`
- [x] 5.2 Update login page background to use `--color-bg`
- [x] 5.3 Update login `h1` to use `--font-heading` (Caveat) at a larger size (1.8rem)
- [x] 5.4 Update login button to use `--color-primary`, add hover transition to `--color-primary-dark`
- [x] 5.5 Add focus ring to login inputs

## 6. Micro-interactions & Accessibility

- [x] 6.1 Wrap all transitions in `@media (prefers-reduced-motion: no-preference)` or add a `reduce` override block
- [x] 6.2 Verify all buttons and links have `cursor: pointer`
- [x] 6.3 Verify color contrast: `--color-text` on `--color-bg` ≥ 4.5:1 (check with browser DevTools)
- [x] 6.4 Test all three pages at 375px, 768px, and 1024px — no horizontal scroll
