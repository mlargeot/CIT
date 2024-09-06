FROM python:3.12.5

# Application workdir creation
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy app files in the container
COPY ./app/ /code/app/

# Run of FastAPI with use of uvicorn
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
