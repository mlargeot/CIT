FROM python:3.9-slim

# Application workdir creation
WORKDIR /app

# Copy app files in the container
COPY . /app

# Python libraries installation
RUN pip install fastapi uvicorn requests selenium beautifulsoup4

# Run of FastAPI with use of uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
