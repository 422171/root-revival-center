# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . ./

# Expose the listening port
ENV PORT=5000
EXPOSE 5000

# Launch the app with Gunicorn
ENTRYPOINT ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]