FROM jupyter/datascience-notebook:latest

LABEL maintainer "milkcocholate"
LABEL titile     "DataScience"

# jupyterlabをインストールする
RUN pip install --upgrade pip
RUN pip install jupyterlab
RUN jupyter serverextension enable --py jupyterlab

EXPOSE 8080
