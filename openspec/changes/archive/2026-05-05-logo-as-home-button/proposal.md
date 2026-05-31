## Why

A dedicated "Calendar" button on the top right is redundant — the logo already occupies the top-left corner and is a conventional navigation anchor. Removing the button reduces chrome and makes the header cleaner without losing any navigation capability.

## What Changes

- Logo (top-left) becomes a clickable link that returns to the calendar home view
- "Calendar" button removed from the top-right header area

## Capabilities

### New Capabilities

- `logo-home-nav`: Logo in the top-left corner acts as the primary home/back navigation target across all views

### Modified Capabilities

- `calendar-ux`: Navigation bar requirement changes — Calendar button removed, logo becomes the home nav element

## Impact

- `index.html` or equivalent layout template — header/nav markup
- CSS for logo hover/click affordance
- Any view that renders the header with the Calendar button
