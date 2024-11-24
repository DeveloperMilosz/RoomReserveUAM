FROM python:3.12.6-slim

# Install system dependencies
RUN apt update && apt install -y libpq-dev python3-dev gcc postgresql-common

# Install requirements
ARG REQUIREMENTS_FILE=dev.txt
ADD requirements/${REQUIREMENTS_FILE} requirements.txt
RUN pip install pip --upgrade && pip install -r requirements.txt

# Copy project
ADD /app /src/app

# Set final workdir
WORKDIR /src/app

# Command to run when image started
CMD python manage.py runserver 0.0.0.0:8000
