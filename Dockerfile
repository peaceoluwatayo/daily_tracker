# Use official Python slim image as base
FROM python:3.10-slim

# Install dependencies for ODBC Driver
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    apt-transport-https \
    build-essential \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Add Microsoft package signing key and repo
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Install the ODBC Driver 18
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Set working directory
WORKDIR /app

# Copy your app files to the container
COPY . /app

# Install Python dependencies (make sure you have requirements.txt)
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "home.py", "--server.port=8501", "--server.address=0.0.0.0"]
