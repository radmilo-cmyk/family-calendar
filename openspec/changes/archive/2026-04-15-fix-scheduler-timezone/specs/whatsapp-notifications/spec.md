## MODIFIED Requirements

### Requirement: A daily digest is sent to both users at 8am Amsterdam time
The system SHALL send a Telegram message to both configured chat IDs every day at 08:00 Europe/Amsterdam time. The scheduler's `CronTrigger` SHALL be explicitly configured with `timezone="Europe/Amsterdam"` — it MUST NOT rely on the scheduler-level timezone default, which does not propagate to triggers. The digest covers today and tomorrow.

#### Scenario: Digest sent at 8am Amsterdam time
- **WHEN** the clock reaches 08:00 Europe/Amsterdam (regardless of server timezone)
- **THEN** the system sends one Telegram message to each configured chat ID

#### Scenario: Digest includes today and tomorrow
- **WHEN** the digest is sent
- **THEN** the message contains all entries for today and all entries for tomorrow, grouped by day and then by type

#### Scenario: No entries on either day
- **WHEN** both today and tomorrow have no entries
- **THEN** the digest is still sent with a message indicating both days are clear

#### Scenario: Digest job execution is visible in logs
- **WHEN** the scheduled job fires
- **THEN** the system logs "send_digest() triggered" at the start, and logs success or error per recipient after sending

#### Scenario: Message build failure is logged
- **WHEN** building the digest message raises an exception
- **THEN** the error is logged and no send is attempted — the app continues running normally
