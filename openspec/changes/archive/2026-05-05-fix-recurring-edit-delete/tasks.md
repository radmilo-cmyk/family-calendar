## 1. Fix Edit Button

- [x] 1.1 Replace inline `onclick` parameters on the recurring edit button with `data-*` attributes (`data-action`, `data-rule-id`, `data-date`, `data-content`, `data-author`, `data-ts`, `data-te`) using `|e` filter for string values
- [x] 1.2 Change edit button `onclick` to `openRecurringModal(this)`

## 2. Fix Delete Button

- [x] 2.1 Replace inline `onclick` parameters on the recurring delete button with `data-*` attributes (`data-action`, `data-rule-id`, `data-date`) using `|e` filter
- [x] 2.2 Change delete button `onclick` to `openRecurringModal(this)`

## 3. Update JavaScript

- [x] 3.1 Update `openRecurringModal(btn)` to read all values from `btn.dataset` instead of function parameters
