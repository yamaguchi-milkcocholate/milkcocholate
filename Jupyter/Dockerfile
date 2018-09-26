FROM jupyter/datascience-notebook:latest

LABEL maintainer "milkcocholate"
LABEL titile     "DataScience"

# jupyterlabをインストールする
RUN pip install --upgrade pip
RUN pip install jupyterlab jsonify
RUN jupyter serverextension enable --py jupyterlab
