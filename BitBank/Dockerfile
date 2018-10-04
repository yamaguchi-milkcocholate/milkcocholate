FROM ubuntu:latest

LABEL maintainer = "milkcocholate"
LABEL titile     = "BitBank"

RUN apt-get update -y && apt-get install -y python-pip python-dev build-essential git
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/bitbankinc/python-bitbankcc.git

CMD . /home/bitbank/
EXPOSE 10080

ENTRYPOINT python /home/bitbank/bitbank.py

