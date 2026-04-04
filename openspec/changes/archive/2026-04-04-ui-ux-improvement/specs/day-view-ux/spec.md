## ADDED Requirements

### Requirement: Entry type sections use SVG icons
Each entry section heading (Events, Chores, Messages) SHALL display an inline Lucide SVG icon instead of an emoji. Icons: `calendar` for Events, `brush` (or `sparkles`) for Chores, `message-circle` for Messages.

#### Scenario: SVG icon renders in section heading
- **WHEN** the day view page loads
- **THEN** each section heading shows a 20×20px SVG icon with `--color-primary` fill/stroke, followed by the section label text

### Requirement: Delete button uses SVG X icon
The delete entry button SHALL use a Lucide `x` SVG icon instead of the ✕ character emoji, with `aria-label="Delete entry"`.

#### Scenario: Delete button accessible
- **WHEN** a screen reader focuses the delete button
- **THEN** it reads "Delete entry"

### Requirement: Empty state has friendly copy
When a section has no entries, the empty state text SHALL read "Nothing here yet." instead of the generic "No [label] for this day."

#### Scenario: Empty state text
- **WHEN** a section has zero entries
- **THEN** the paragraph reads "Nothing here yet." in `--color-text-muted` at 0.875rem

### Requirement: Add-entry form has visible focus rings
All form inputs (select, textarea) and the submit button SHALL show a visible `outline` focus ring using `--color-primary` when focused by keyboard.

#### Scenario: Focus ring on textarea
- **WHEN** user tabs into the textarea
- **THEN** a 2px `--color-primary` outline is visible around the input

### Requirement: Submit button shows loading state
When the add-entry form is submitted, the submit button SHALL be disabled and display "Adding…" until the page reloads.

#### Scenario: Button disables on submit
- **WHEN** user clicks the "Add" button
- **THEN** the button is immediately disabled and text changes to "Adding…"
