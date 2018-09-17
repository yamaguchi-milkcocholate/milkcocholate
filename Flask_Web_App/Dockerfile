FROM ubuntu:latest

LABEL maintainer "milkcocholate"
LABEL titile     "FlaskWebApp"

RUN apt-get update -y && apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt



ENTRYPOINT ["python"]
CMD ["app.py"]
