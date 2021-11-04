FROM python:3.8-slim

ENV PYTHONUNBUFFERED True

COPY code/requirements.txt /
RUN pip3 install -r /requirements.txt 

COPY /code /app
WORKDIR /app

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app

