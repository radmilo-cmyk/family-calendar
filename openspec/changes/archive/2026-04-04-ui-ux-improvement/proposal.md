## Why

The current family calendar app works functionally but feels bare and generic — flat colors, no visual warmth, emojis used as icons, and no micro-interactions. Since this is a personal family tool used daily, the UI should feel friendly, polished, and pleasant to use on both desktop and mobile.

## What Changes

- Replace the flat blue color scheme with a warm teal palette (primary `#0D9488`, background `#F0FDFA`, text `#134E4A`)
- Add Google Fonts: Caveat (headings) + Quicksand (body) for a personal, friendly feel
- Replace emoji icons (📅 🧹 💬 ✕) with SVG icons from Lucide
- Add micro-interactions: hover transitions on calendar days, buttons, and entry items
- Improve calendar grid: taller cells, better entry dot indicators, today highlight
- Improve day view: stronger section card design, better empty states, cleaner add-entry form
- Improve login page: softer background, better card styling
- Add `cursor-pointer` and visible `focus` states to all interactive elements
- Add `prefers-reduced-motion` support

## Capabilities

### New Capabilities
- `visual-design-system`: New CSS custom properties (variables), Google Fonts import, teal color palette, typography scale — applied globally via `base.html` and `style.css`
- `calendar-ux`: Improved calendar grid — larger cells, today highlight ring, entry dot indicators instead of background fill, smooth day hover transitions
- `day-view-ux`: Redesigned day view cards with SVG icons per entry type, improved empty states, polished add-entry form with focus ring and submit feedback
- `micro-interactions`: CSS transitions on buttons, nav links, calendar cells, and entry items; loading state on form submit button

### Modified Capabilities
- `user-auth`: Login page visual refresh only (layout, colors, typography) — no auth logic changes

## Impact

- `app/static/style.css` — full rewrite
- `app/templates/base.html` — add Google Fonts link, replace emoji site-title icon with SVG
- `app/templates/calendar.html` — update day cells for dot indicators and today highlight
- `app/templates/day.html` — replace emoji icons with SVG, add JS for button loading state
- `app/templates/login.html` — visual refresh only
- No backend changes required
