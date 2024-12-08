FROM python:3.10-slim

WORKDIR /app

COPY ./api /app/api
COPY ./app_secrets /app/app_secrets
COPY ./application /app/application
COPY ./config /app/config
COPY ./controller /app/controller
COPY ./repository /app/repository
COPY ./service /app/service
COPY main.py /app
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]