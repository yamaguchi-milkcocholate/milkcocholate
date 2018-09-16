FROM ubuntu:latest

LABEL maintainer "milkcocholate"
LABEL titile     "FlaskWebApp"

RUN apt-get update -y && apt-get install -y python-pip python-dev

ENV DOCKERDIRPATH /docker/flask
ENV SRCDIRPATH /src/flask
COPY $DOCKERDIRPATH/requirements.txt ./code/requirements.txt

# ./routeにapp.pyをコピーする
# app.pyのコピーからビルドしないとvolumesが邪魔してしまうから
COPY $SRCDIRPATH/app.py ./route/app.py


COPY .$SRCDIRPATH /code
WORKDIR ./code

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR ../route

CMD ["python", "app.py"]
