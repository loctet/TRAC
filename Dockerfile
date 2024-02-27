
# Use the official Python image with version 3.10
FROM python:3.10

# Set the working directory in the container
WORKDIR /home/TRAC

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir z3-solver matplotlib numpy plotly networkx pandas

# Install OpenJDK-11
RUN apt-get update && \
    apt-get -y install default-jre && \
    apt-get install -y nano && \
    apt-get clean;

# Install gedit
RUN apt-get update && apt-get install -y gedit

# Set up the 'll' command alias
RUN echo 'alias ll="ls -l"' >> ~/.bashrc



# Make port 80 available to the world outside this container
# EXPOSE 80

# Define environment variable
ENV TRAC DAFSMs

# Set the default command to Bash
CMD ["bash"]