FROM python:3.9-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LOG_LEVEL=info

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ src/

# Copy documentation
COPY docs/ docs/

# Copy sample data
COPY data/persistent/ data/persistent/

# Copy configuration files
COPY log_config.json .

# Create necessary directories
RUN mkdir -p data/uploads

# Expose the port the app runs on
EXPOSE 8081

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8081", "--log-config", "log_config.json"] 