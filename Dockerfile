FROM python:3.6

ENV PYTHONBUFFERED 1

RUN mkdir /scrumhelper

WORKDIR /scrumhelper

ADD . /scrumhelper/

RUN pip install -r requirements.txt