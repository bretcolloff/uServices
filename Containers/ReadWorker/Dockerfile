FROM tiangolo/uwsgi-nginx:latest

MAINTAINER Bret Colloff <bret.colloff@gmail.com>

ENV HOSTLOC localhost

RUN pip install flask
RUN pip install flask-restful
RUN pip install pika

COPY nginx.conf /etc/nginx/conf.d/

RUN echo ${HOSTLOC} >> /app/config.txt

COPY ./app /app
