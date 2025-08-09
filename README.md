# Online Poll System

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2+-green.svg)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-blue.svg)](https://postgresql.org)

A scalable backend API for creating and managing online polls with real-time voting and results.


## Features

- **Poll Management**: Create, update, and manage polls with multiple options and expiry dates.
- **Voting System**: Secure voting for authenticated and guest users, with duplicate prevention.
- **Poll Analytics**: Track poll views and analytics via the `/api/poll-views/` endpoint.
- **Real-time Results**: Efficient vote counting and result computation.
- **API Documentation**: Interactive Swagger/OpenAPI documentation at `/api/swagger/`.
- **Database Optimization**: Optimized PostgreSQL schemas for scalability.

## Tech Stack

- **Backend**: Django REST Framework
- **Database**: PostgreSQL
- **Documentation**: Swagger/OpenAPI
- **Deployment**: Docker support

## Quick Start

### Choose How to Run

You can run the project either locally (with your own Python and PostgreSQL) or using Docker Compose (recommended for easy setup).

---

## 1. Local Development

### Prerequisites

- Python 3.12+
- Django 5.2+
- PostgreSQL 16+
- pip

### Environment Variables

Copy `.env.example` to `.env` and fill in your values:
```bash
cp .env.example .env
```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AshenafiTech/Online-Poll-System.git
   cd Online-Poll-System
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure database:
   - Create a PostgreSQL database and user matching your `.env` values.
   - Ensure PostgreSQL is running.

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

7. Start development server:
   ```bash
   python manage.py runserver
   ```

---

## 2. Docker Compose (Recommended)

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Copy `.env.example` to `.env` and fill in your values (or use defaults):
   ```bash
   cp .env.example .env
   ```

2. Build and run:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - API: http://localhost:8000/api/
   - Swagger Docs: http://localhost:8000/api/swagger/
   - Admin: http://localhost:8000/admin/

---


## Accessing the Application & API

- **API Base URL:** [http://localhost:8000/api/](http://localhost:8000/api/)
- **Swagger Documentation:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **ReDoc Documentation:** [http://localhost:8000/redoc/](http://localhost:8000/redoc/)
- **Admin Panel:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

> These URLs are the same for both local and Docker setups (unless you change the ports).

**Example:**  
Open [http://localhost:8000/api/](http://localhost:8000/api/) in your browser to see the API root.

**Note:**  
Most API endpoints require authentication. See the [Authentication](#authentication) section for details on obtaining and using JWT tokens.

## API Usage

### Authentication

Most endpoints require authentication using JWT tokens. Obtain a token with:

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

Response:
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

Use the access token in the `Authorization` header for protected endpoints:

```bash
-H "Authorization: Bearer <access_token>"
```

---


### API Endpoints Summary

| Endpoint                        | Method     | Auth Required | Description                                 |
|----------------------------------|------------|--------------|---------------------------------------------|
| /api/token/                     | POST       | No           | Obtain JWT token                            |
| /api/token/refresh/             | POST       | No           | Refresh JWT token                           |
| /api/polls/                     | GET/POST   | Yes          | List or create a poll                       |
| /api/polls/{poll_id}/vote/      | POST       | No           | Vote on a poll (auth or guest)              |
| /api/polls/{poll_id}/results/   | GET        | No           | Get poll results                            |
| /api/guest-votes/               | GET/POST   | No           | List or create guest votes                  |
| /api/poll-views/                | GET        | No           | List poll analytics (views/statistics)      |
| /api/register/                  | POST       | No           | Register a new user                         |
| /api/profile/                   | GET        | Yes          | Get user profile                            |

## Running Tests

To run tests locally:
```bash
python manage.py test
```

To run tests in Docker:
```bash
docker-compose run web python manage.py test
```

## Troubleshooting

- **Database Connection Issues:** Ensure your `.env` file has the correct database host, user, and password. For local development, you can use SQLite by updating your Django settings.
- **Missing Dependencies:** Activate your virtual environment and run `pip install -r requirements.txt`.
- **URL Not Found:** If you add new endpoints, restart the server and check the registered URLs.

## Support & Contact

If you have any questions, issues, or suggestions, please open an issue on GitHub or contact the maintainer via the repository.

---

### Create a Poll
```bash
curl -X POST http://localhost:8000/api/polls/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "question": "Your favorite programming language?",
    "options": ["Python", "JavaScript", "Go", "Rust"],
    "expires_at": "2025-12-31T23:59:59Z"
  }'
```
Response:
```json
{
  "id": 1,
  "question": "Your favorite programming language?",
  "options": [
    {"id": 1, "option_text": "Python"},
    {"id": 2, "option_text": "JavaScript"},
    {"id": 3, "option_text": "Go"},
    {"id": 4, "option_text": "Rust"}
  ],
  "expires_at": "2025-12-31T23:59:59Z"
}
```


### Vote on a Poll (Authenticated or Guest)

#### Authenticated User
```bash
curl -X POST http://localhost:8000/api/polls/{poll_id}/vote/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"option": 1}'
```
Response:
```json
{
  "detail": "Vote recorded."
}
```

#### Guest User
```bash
curl -X POST http://localhost:8000/api/polls/{poll_id}/vote/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=guest-session-1" \
  --header "X-Forwarded-For: 1.2.3.4" \
  -d '{"option": 1}'
```
Response:
```json
{
  "detail": "Vote recorded (guest)."
}
```

### Get Poll Results
```bash
curl http://localhost:8000/api/polls/{poll_id}/results/
```
Response:
```json
{
  "question": "Your favorite programming language?",
  "results": [
    {"option": "Python", "votes": 10},
    {"option": "JavaScript", "votes": 5},
    {"option": "Go", "votes": 2},
    {"option": "Rust", "votes": 3}
  ]
}
```

---


### Error Handling

- If you provide invalid credentials or an expired token, you'll receive:
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid"
}
```
- If you try to vote without required fields:
```json
{
  "detail": "Option ID is required."
}
```
- If a guest tries to vote without session or IP:
```json
{
  "detail": "Session ID and IP address are required for guest voting."
}
```




## Running Tests

To run tests locally:
```bash
python manage.py test
```

To run tests in Docker (if you have a test service configured):
```bash
docker-compose run web python manage.py test
```


## Project Structure

```
Online-Poll-System/
├── polls/           # Django app (polls logic, API, models)
├── config/          # Django settings and URLs
├── requirements.txt # Python dependencies
├── Dockerfile       # Docker image
├── docker-compose.yml # Docker Compose config
└── manage.py        # Django management script
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Support & Contact

If you have any questions, issues, or suggestions, please open an issue on GitHub or contact the maintainer via the repository.
