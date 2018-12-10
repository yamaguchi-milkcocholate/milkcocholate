FROM python:3.6

LABEL maintainer = "milkcocholate"
LABEL titile     = "BitBank"

RUN apt-get update -y && apt-get install -y python-pip python-dev build-essential git
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python3 -m pip install PyMySQL
RUN pip install git+https://github.com/bitbankinc/python-bitbankcc.git

COPY . /home/bitbank/
ENTRYPOINT python
