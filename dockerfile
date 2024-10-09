# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt (or manually install dependencies) into the container
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Alternatively, if you are not using requirements.txt, install dependencies manually
# RUN pip install pandas==1.5.3 numpy==1.21.6

# Copy the current directory contents (your script and files) into the container at /app
COPY . /app

# Expose port (if necessary for communication outside the container)
# EXPOSE 5000

# Create a folder for the input files
RUN mkdir -p /app/input_data

# Create a folder for the output files
RUN mkdir -p /app/output_data

# Set the environment variable to indicate input and output folder paths
ENV INPUT_FOLDER=/app/input_data
ENV OUTPUT_FOLDER=/app/output_data

# Command to run the Python script, passing the folder paths and number of files to process
CMD ["python", "outliers.py", "/app/input_data", "2"]
