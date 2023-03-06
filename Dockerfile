FROM ubuntu:latest

RUN mkdir -p /usr/app/src/cards

RUN apt update
RUN apt install python3 -y

RUN apt-get -y install python3-pip
RUN pip3 install beautifulsoup4

RUN pip3 install mysql-connector-python

WORKDIR /usr/app/src

COPY ./main.py ./
