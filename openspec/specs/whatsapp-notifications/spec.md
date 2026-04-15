# whatsapp-notifications Specification

## Purpose
TBD - created by archiving change family-calendar-app. Update Purpose after archive.
## Requirements
### Requirement: A daily digest is sent to both users at 8am Amsterdam time
The system SHALL send a WhatsApp message to both configured phone numbers every day at 08:00 Europe/Amsterdam time via the Twilio API. The digest covers today and tomorrow. The CronTrigger MUST be explicitly configured with `timezone="Europe/Amsterdam"` — relying on a scheduler-level default timezone is not permitted.

#### Scenario: Digest sent at 8am
- **WHEN** the clock reaches 08:00 Europe/Amsterdam
- **THEN** the system sends one WhatsApp message to each configured phone number

#### Scenario: CronTrigger timezone is explicit
- **GIVEN** the scheduler is configured
- **WHEN** the CronTrigger for the daily digest is defined
- **THEN** it includes `timezone="Europe/Amsterdam"` as an explicit parameter, not relying on any scheduler-level default

#### Scenario: Digest includes today and tomorrow
- **WHEN** the digest is sent
- **THEN** the message contains all entries for today and all entries for tomorrow, grouped by day and then by type

#### Scenario: No entries on either day
- **WHEN** both today and tomorrow have no entries
- **THEN** the digest is still sent with a message indicating both days are clear

### Requirement: Digest message is clearly formatted
The system SHALL format the digest message so it is easy to read in WhatsApp. Each day SHALL be a clearly labelled section. Within each day, entries SHALL be grouped by type (events, chores, messages) with the author shown per entry.

#### Scenario: Message format
- **WHEN** the digest is generated for a day with entries
- **THEN** the message uses a structure like: date header → type label → entry content (author)

### Requirement: Phone numbers and Twilio credentials are stored in config
The system SHALL read Twilio account SID, auth token, WhatsApp sender number, and both recipient phone numbers from environment variables (`.env` file). No credentials SHALL be hardcoded in source code.

#### Scenario: Missing credentials
- **WHEN** a required Twilio environment variable is not set at startup
- **THEN** the system logs a clear error and the scheduler does not start

### Requirement: Digest failures are logged and do not crash the app
The system SHALL catch any errors from the Twilio API call, log them, and continue running. A failed digest SHALL NOT stop the web application.

#### Scenario: Twilio API error
- **WHEN** the Twilio API returns an error during digest sending
- **THEN** the error is logged and the application continues serving requests normally

