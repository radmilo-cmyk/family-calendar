## ADDED Requirements

### Requirement: Logo navigates to calendar home
The app logo in the top-left corner SHALL be wrapped in an anchor element that navigates to the calendar home view when clicked.

#### Scenario: Logo click returns to home
- **WHEN** user clicks the logo from any view
- **THEN** browser navigates to the calendar home URL

#### Scenario: Logo has pointer cursor on hover
- **WHEN** user hovers over the logo
- **THEN** cursor changes to pointer, indicating it is clickable

### Requirement: Calendar navigation button removed
The dedicated "Calendar" button in the header SHALL be removed from all views.

#### Scenario: Calendar button absent
- **WHEN** any page renders the header
- **THEN** no "Calendar" label button appears in the top-right area
