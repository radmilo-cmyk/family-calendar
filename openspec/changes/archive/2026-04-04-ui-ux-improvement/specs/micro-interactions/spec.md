## ADDED Requirements

### Requirement: All interactive elements have transition-based hover states
Buttons, nav links, calendar day cells, and the delete button SHALL transition color/background changes over 150–200ms using `transition: ... 150ms ease`.

#### Scenario: Button hover transition
- **WHEN** user hovers over the primary action button
- **THEN** background color transitions smoothly (not instant) to `--color-primary-dark`

### Requirement: Animations respect prefers-reduced-motion
All CSS transitions and animations SHALL be wrapped in a `@media (prefers-reduced-motion: no-preference)` block OR set to `transition: none` inside `@media (prefers-reduced-motion: reduce)`.

#### Scenario: Reduced motion respected
- **WHEN** the OS accessibility setting "Reduce Motion" is enabled
- **THEN** no transitions or animations play

### Requirement: All clickable elements declare cursor-pointer
Every interactive element (links, buttons, nav items, calendar day links) SHALL have `cursor: pointer` in its CSS rule.

#### Scenario: Cursor on calendar day
- **WHEN** user moves the mouse over a calendar day link
- **THEN** cursor changes to a pointer hand

### Requirement: Nav links have underline-on-hover feedback
Header navigation links SHALL show an underline on hover using a CSS transition, not a raw `text-decoration`.

#### Scenario: Nav link hover
- **WHEN** user hovers over a nav link in the header
- **THEN** an underline animates in within 150ms
