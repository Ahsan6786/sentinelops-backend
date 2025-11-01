# Use official Python image as base
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (agar app.py me flask ya fastapi run kar raha hai)
EXPOSE 5000

# Command to run your app
CMD ["python", "app.py"]
