# Use the official Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN apt-get update && apt-get install -y build-essential libffi-dev libpq-dev
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the app runs
EXPOSE 8000

# Set the command to run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
