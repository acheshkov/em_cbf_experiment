FROM jupyter/datascience-notebook
USER root
RUN sudo apt-get update && apt install -y default-jre
USER $NB_UID

COPY . .

ENTRYPOINT ["python3", "-m", "unittest", "discover", "-s", "tests"]