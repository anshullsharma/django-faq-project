# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y gcc python3-dev

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Collect static files (if needed)
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["gunicorn", "faq_project.wsgi:application", "--bind", "0.0.0.0:8000"]
