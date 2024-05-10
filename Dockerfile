# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY update_godaddy_ip.py .

# Install required libraries
RUN pip install requests

# Set the command to run the Python script
CMD ["python", "update_godaddy_ip.py"]

