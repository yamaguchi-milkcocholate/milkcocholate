FROM python:3.6

LABEL maintainer = "milkcocholate"
LABEL titile     = "FlaskWebApp"

RUN apt-get update -y && apt-get install -y python-pip python-dev build-essential
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000
COPY . /home/app/
RUN cd /home/app/ && pwd && ls
ENTRYPOINT python /home/app/app.py
