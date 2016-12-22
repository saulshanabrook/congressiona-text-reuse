FROM jupyter/datascience-notebook

USER root  
RUN apt-get update && apt-get install -y \
		libffi-dev \
	&& rm -rf /var/lib/apt/lists/*
USER jovyan

WORKDIR /code/

RUN conda update -y --all

COPY requirements.conda.txt /code/requirements.conda.txt
RUN conda install -y --channel conda-forge --file requirements.conda.txt

COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY govtrackdata /code/govtrackdata
