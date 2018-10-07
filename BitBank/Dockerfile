FROM ubuntu:latest

LABEL maintainer = "milkcocholate"
LABEL titile     = "BitBank"

RUN apt-get update -y && apt-get install -y python-pip python-dev build-essential git
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/bitbankinc/python-bitbankcc.git

EXPOSE 10080
COPY . /home/bitbank/
RUN cd /home/bitbank/ && pwd && ls
ENTRYPOINT python /home/bitbank/bitbank.py

