# Use the official Python image as the base image
FROM python:3.10.17-alpine3.20
# FROM python:3.10-slim


# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask application
# CMD ["flask", "run"]
CMD ["uvicorn", "app.routes:app", "--host", "0.0.0.0", "--port", "5000"]