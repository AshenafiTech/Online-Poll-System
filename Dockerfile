
# Python base image
FROM python:3.11-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev netcat-openbsd curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install gunicorn

# Create non-root user
RUN useradd -m appuser


# Ensure staticfiles directory exists and is owned by appuser
RUN mkdir -p /app/staticfiles && chown -R appuser:appuser /app/staticfiles

# Copy project files
COPY . /app/

# Copy and set permissions for entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

USER appuser

ENTRYPOINT ["/app/entrypoint.sh"]
# Use DJANGO_ENV to switch between dev and prod
CMD ["/bin/bash", "-c", "if [ '$DJANGO_ENV' = 'production' ]; then exec gunicorn config.wsgi:application --bind 0.0.0.0:8000; else exec python manage.py runserver 0.0.0.0:8000; fi"]
