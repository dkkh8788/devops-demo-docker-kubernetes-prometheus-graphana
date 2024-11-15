# Use a Python base image
FROM python:3.9

# Create a working directory within the container
WORKDIR /app

# Copy the application code
COPY main.py .

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Set the command to run the application on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
