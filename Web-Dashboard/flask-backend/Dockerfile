# Use Python official image as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt



# Expose port 5050 for the Flask/SocketIO app
EXPOSE 5050

# Run via python so socketio.run() is used (flask run doesn't support SocketIO properly)
CMD ["python", "app.py"]
