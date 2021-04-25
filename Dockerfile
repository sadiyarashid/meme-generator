FROM python:3.9.4-buster

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y poppler-utils

EXPOSE 8000

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]