FROM python:3.10-slim

# Install required packages (e.g., cron)
RUN apt-get update && apt-get install -y build-essential libffi-dev libpq-dev cron

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

RUN pip install -r requirements.txt

# Create the script directory
RUN mkdir -p /scripts

# Copy your cron script into the container
COPY command.sh /scripts/

# Make the script executable
RUN chmod +x /scripts/command.sh

# Set up a cron job to run the script daily at midnight
COPY crontab /etc/cron.d/crontab

RUN chmod 0644 /etc/cron.d/crontab

RUN crontab /etc/cron.d/crontab

CMD ["cron", "-f"]
