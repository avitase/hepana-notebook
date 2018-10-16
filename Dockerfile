FROM jupyter/scipy-notebook:latest

ARG USERNAME=jovyan

USER root
RUN apt-get update -yqq && \
apt-get install -yqq apt-utils
RUN apt-get install -yqq \
gnuplot \
texlive-full \
ghostscript imagemagick
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

USER ${USERNAME}

RUN pip install --upgrade pip && pip install \
uncertainties iminuit sympy

RUN conda update conda && \
conda install -c conda-forge jupyter_nbextensions_configurator && \
conda install -c conda-forge jupyter_contrib_nbextensions
RUN jupyter nbextension enable spellchecker/main

RUN mkdir -p $HOME/scripts
COPY --chown=jovyan:users scripts/* ${HOME}/scripts/
ENV PATH="$HOME/scripts:$PATH" \
PYTHONPATH="$HOME/scripts:$PYTHONPATH" \
TEXINPUTS="$HOME/scripts:$TEXINPUTS"

WORKDIR ${HOME}/work/
