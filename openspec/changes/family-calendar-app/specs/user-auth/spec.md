## ADDED Requirements

### Requirement: Two hardcoded user accounts exist
The system SHALL have exactly two user accounts defined in a configuration file (`.env`). No registration flow exists. Credentials consist of a username and a hashed password.

#### Scenario: Valid login
- **WHEN** a user submits correct username and password
- **THEN** the system creates a session and redirects to the calendar view

#### Scenario: Invalid login
- **WHEN** a user submits an incorrect username or password
- **THEN** the system displays an error message and stays on the login page

#### Scenario: Empty credentials
- **WHEN** a user submits the login form with empty fields
- **THEN** the system displays a validation error and does not attempt authentication

### Requirement: Protected routes require authentication
The system SHALL redirect unauthenticated users to the login page when they attempt to access any route other than `/login`.

#### Scenario: Unauthenticated access to calendar
- **WHEN** an unauthenticated user visits `/`
- **THEN** the system redirects them to `/login`

#### Scenario: Authenticated access
- **WHEN** an authenticated user visits any protected route
- **THEN** the system serves the requested page normally

### Requirement: Users can log out
The system SHALL provide a logout action that clears the session.

#### Scenario: Logout
- **WHEN** a logged-in user triggers logout
- **THEN** the system clears their session and redirects to the login page

### Requirement: Current user identity is available in session
The system SHALL store the logged-in user's username in the session so it can be used as the author on any entry they create.

#### Scenario: Author attribution
- **WHEN** a logged-in user creates an entry
- **THEN** the entry's author field is set to their username from the session
