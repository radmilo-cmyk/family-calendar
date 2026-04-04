## ADDED Requirements

### Requirement: Login page visual presentation
The login page SHALL use the updated design token colors and typography: `--color-bg` as page background, `--color-surface` as card background, `--font-heading` for the page title, and `--font-body` for labels and inputs. The card SHALL use `--shadow-md` and `--radius`. The submit button SHALL use `--color-primary` background with `--color-cta` as hover alternative for contrast. All auth logic and form fields remain unchanged.

#### Scenario: Login card renders with new palette
- **WHEN** an unauthenticated user visits the login page
- **THEN** the page background is `#F0FDFA`, the card is white with a teal-tinted shadow, the heading is in Caveat font, and inputs have a visible focus ring in `--color-primary`

#### Scenario: Error message still visible
- **WHEN** the user submits incorrect credentials
- **THEN** the error message renders in the existing red error style, still clearly visible against the new background
