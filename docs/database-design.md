# Database Design – Poll System

This document describes the normalized database schema for the Poll System application. It includes explanations of each table, relationships, constraints, and design rationale.

---

## Entity-Relationship Diagram

![ER Diagram](./er-diagram.png)

> Diagram generated using [dbdiagram.io](https://dbdiagram.io) – stored in `/docs/er-diagram.png`

---

## Tables and Descriptions

### 1. `users`

Stores information about registered users.

| Field         | Type      | Description                             |
|---------------|-----------|-----------------------------------------|
| `id`          | Integer   | Primary Key                             |
| `username`    | Varchar   | Unique username                         |
| `email`       | Varchar   | Unique email address                    |
| `password_hash` | Varchar | Hashed password                         |
| `is_active`   | Boolean   | Whether the user account is active      |
| `created_at`  | Timestamp | Time of registration                    |
| `updated_at`  | Timestamp | Time of last profile update             |

---

### 2. `polls`

Represents individual polls/questions created by users.

| Field               | Type      | Description                                    |
|---------------------|-----------|------------------------------------------------|
| `id`                | Integer   | Primary Key                                    |
| `title`             | Varchar   | Poll title                                     |
| `description`       | Text      | Optional description                           |
| `pub_date`          | Timestamp | Publication time                               |
| `end_date`          | Timestamp | Expiration date (if any)                       |
| `allow_multiple_votes` | Boolean | Whether multiple votes are allowed            |
| `is_active`         | Boolean   | Whether the poll is visible and open           |
| `created_by`        | Integer   | FK → `users.id` (poll author)                 |
| `created_at`        | Timestamp | Time of creation                               |
| `updated_at`        | Timestamp | Time of last update                            |

---

### 3. `choices`

Available answer options for each poll.

| Field        | Type      | Description                        |
|--------------|-----------|------------------------------------|
| `id`         | Integer   | Primary Key                        |
| `poll_id`    | Integer   | FK → `polls.id`                    |
| `choice_text`| Varchar   | Text of the choice                 |
| `created_at` | Timestamp | Time of choice creation            |

---

### 4. `votes`

Stores authenticated or anonymous votes cast by users.

| Field        | Type      | Description                                 |
|--------------|-----------|---------------------------------------------|
| `id`         | Integer   | Primary Key                                 |
| `poll_id`    | Integer   | FK → `polls.id`                             |
| `choice_id`  | Integer   | FK → `choices.id`                           |
| `user_id`    | Integer   | FK → `users.id` (nullable for guests)       |
| `session_id` | Varchar   | Used for guest identification (optional)    |
| `ip_address` | Varchar   | Tracks guest IP                             |
| `voted_at`   | Timestamp | Time the vote was cast                      |

**Constraints:**
- Unique vote per `(poll_id, user_id)` if authenticated
- Guests are tracked via `ip_address` and `session_id`

---

### 5. `guest_votes`

Used when a vote is cast by an unauthenticated user.

| Field        | Type      | Description                            |
|--------------|-----------|----------------------------------------|
| `id`         | Integer   | Primary Key                            |
| `poll_id`    | Integer   | FK → `polls.id`                        |
| `choice_id`  | Integer   | FK → `choices.id`                      |
| `ip_address` | Varchar   | Guest IP address                       |
| `session_id` | Varchar   | Guest session or browser identifier    |
| `voted_at`   | Timestamp | Time the vote was cast                 |

**Constraint:** unique vote per guest per poll

---

### 6. `poll_views`

Tracks which users or guests have viewed which polls.

| Field        | Type      | Description                            |
|--------------|-----------|----------------------------------------|
| `id`         | Integer   | Primary Key                            |
| `poll_id`    | Integer   | FK → `polls.id`                        |
| `user_id`    | Integer   | FK → `users.id` (nullable)             |
| `ip_address` | Varchar   | Viewer’s IP address                    |
| `session_id` | Varchar   | Guest/session identifier               |
| `viewed_at`  | Timestamp | Time the poll was viewed               |

---

## Normalization and Integrity

- All tables follow **3rd Normal Form (3NF)** to avoid redundancy and maintain clean relationships.
- Use of foreign keys ensures **referential integrity**.
- Timestamps provide **auditing and tracking** capabilities.
- Optional fields allow **guest access** without sacrificing user-based features.

---

