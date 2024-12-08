# Use the official Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the current directory into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8001

# Run the application
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8001"]
