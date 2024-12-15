FROM python:3.12-slim

# Set the working directory
WORKDIR /app
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt
