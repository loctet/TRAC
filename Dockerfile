
# Use the official Python image with version 3.10
FROM python:3.10

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir z3-solver matplotlib numpy plotly networkx pandas

# Install OpenJDK-11
RUN apt-get update && \
    apt-get -y install default-jre && \
    apt-get clean;

# Make port 80 available to the world outside this container
# EXPOSE 80

# Define environment variable
ENV TRAC World

# Run app.py when the container launches
CMD ["python", "./src/Main.py"]
