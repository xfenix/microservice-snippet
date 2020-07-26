FROM python:3.8.5-slim-buster

WORKDIR /srv/www/

COPY . .

RUN pip install pipenv &&\
    pipenv install --deploy --system
