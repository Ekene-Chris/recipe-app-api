# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=app.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate

# Create a non-root user
RUN adduser --disabled-password --gecos '' myuser

# Change ownership of the app files to the non-root user
RUN chown -R myuser:myuser /app

# Switch to non-root user
USER myuser

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]