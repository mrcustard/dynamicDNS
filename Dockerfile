# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY update_godaddy_ip.py .

# Create the current_ip.txt file if it doesn't exist
RUN touch /app/current_ip.txt

# Install required libraries
RUN pip install requests

# Set the command to run the Python script
CMD ["python", "update_godaddy_ip.py"]
