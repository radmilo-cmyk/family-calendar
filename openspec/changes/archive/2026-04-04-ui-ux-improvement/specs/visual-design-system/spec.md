## ADDED Requirements

### Requirement: CSS design tokens via custom properties
The stylesheet SHALL define all colors, fonts, and spacing as CSS custom properties on `:root` so any future change touches one place only.

Tokens to define:
- `--color-primary: #0D9488`
- `--color-primary-dark: #0f766e`
- `--color-secondary: #14B8A6`
- `--color-cta: #F97316`
- `--color-bg: #F0FDFA`
- `--color-surface: #ffffff`
- `--color-text: #134E4A`
- `--color-text-muted: #4B7F78`
- `--color-border: #CCEDE9`
- `--font-heading: 'Caveat', cursive`
- `--font-body: 'Quicksand', sans-serif`
- `--radius: 12px`
- `--shadow-sm: 0 1px 4px rgba(0,0,0,0.07)`
- `--shadow-md: 0 4px 16px rgba(0,0,0,0.10)`

#### Scenario: Token drives button color
- **WHEN** `--color-primary` is changed in `:root`
- **THEN** all buttons, header background, and link colors update without touching other rules

### Requirement: Google Fonts loaded in base template
The `base.html` template SHALL include a `<link>` tag loading Caveat (400–700) and Quicksand (300–700) from Google Fonts.

#### Scenario: Fonts load on page render
- **WHEN** the browser loads any page
- **THEN** headings render in Caveat and body text renders in Quicksand

### Requirement: Body uses token-based styles
The `body` element SHALL use `--font-body`, `--color-bg` for background, `--color-text` for text, and `line-height: 1.6`.

#### Scenario: Body contrast passes accessibility check
- **WHEN** `--color-text` (`#134E4A`) is rendered on `--color-bg` (`#F0FDFA`)
- **THEN** contrast ratio SHALL be at least 4.5:1
