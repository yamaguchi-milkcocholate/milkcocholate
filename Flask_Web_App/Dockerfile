FROM ubuntu:latest

LABEL maintainer = "milkcocholate"
LABEL titile     = "FlaskWebApp"

RUN apt-get update -y && apt-get install -y python-pip python-dev build-essential
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT python /home/app/app.py
