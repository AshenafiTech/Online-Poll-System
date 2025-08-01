# Online Poll System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.0+-green.svg)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://postgresql.org)

A scalable backend API for creating and managing online polls with real-time voting and results.

## Features

- **Poll Management**: Create polls with multiple options and expiry dates
- **Voting System**: Secure voting with duplicate prevention
- **Real-time Results**: Efficient vote counting and result computation
- **API Documentation**: Interactive Swagger/OpenAPI documentation
- **Database Optimization**: Optimized PostgreSQL schemas for scalability

## Tech Stack

- **Backend**: Django REST Framework
- **Database**: PostgreSQL
- **Documentation**: Swagger/OpenAPI
- **Deployment**: Docker support

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL 13+
- pip

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
   - Update PostgreSQL credentials in `settings.py`
   - Or set environment variables:
     ```bash
     export DB_NAME=your_db_name
     export DB_USER=your_db_user
     export DB_PASSWORD=your_db_password
     export DB_HOST=localhost
     export DB_PORT=5432
     ```

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

8. Access the API:
   - API Base URL: http://localhost:8000/api/
   - Swagger Documentation: http://localhost:8000/api/docs/
   - Admin Panel: http://localhost:8000/admin/

## API Usage

### Create a Poll
```bash
curl -X POST http://localhost:8000/api/polls/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Your favorite programming language?",
    "options": ["Python", "JavaScript", "Go", "Rust"],
    "expiry": "2025-12-31T23:59:59Z"
  }'
```

### Vote on a Poll
```bash
curl -X POST http://localhost:8000/api/polls/{poll_id}/vote/ \
  -H "Content-Type: application/json" \
  -d '{"option_id": 2}'
```

### Get Poll Results
```bash
curl http://localhost:8000/api/polls/{poll_id}/results/
```

## Docker Deployment

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. Access the application:
   - API: http://localhost:8000/api/
   - Documentation: http://localhost:8000/api/docs/

## Project Structure

```
Online-Poll-System/
├── polls/              # Main Django app
├── config/             # Django settings
├── requirements.txt    # Python dependencies
├── docker-compose.yml  # Docker configuration
├── Dockerfile         # Docker image
└── manage.py          # Django management script
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you have any questions or issues, please open an issue on GitHub.
