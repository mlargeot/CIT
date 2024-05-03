FROM python:3.9-slim

# Application workdir creation
WORKDIR /app

# Copy app files in the container
COPY . /app

# Python libraries installation
RUN pip install fastapi uvicorn requests

# Run of FastAPI with use of uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
