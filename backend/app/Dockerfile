FROM python:3.6-stretch

COPY . /app
WORKDIR /app

RUN pip install spacy
RUN python -m spacy download en
RUN apt-get update
