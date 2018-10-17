FROM jupyter/datascience-notebook:latest

LABEL maintainer = "milkcocholate"
LABEL titile     = "Jupyter"

# jupyterlabをインストールする
RUN pip install --upgrade pip
RUN pip install jupyterlab jsonify
RUN pip install --upgrade google-cloud-storage
RUN jupyter serverextension enable --py jupyterlab
RUN python3 -m pip install PyMySQL


EXPOSE 8888
COPY ./work /home/jovyan/work/
RUN cd /home/jovyan/work/ && pwd && ls

ENTRYPOINT start.sh jupyter lab --NotebookApp.password='sha1:c5b53f77b829:c9a1bb2b62071482b4d09cf99fc0f5baffe57755'
