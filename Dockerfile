FROM jupyter/scipy-notebook:latest

ARG USERNAME=jovyan

USER root
RUN apt-get update -yq && \
apt-get install -yq apt-utils
RUN apt-get install -yq \
texlive \
texlive-latex-extra \
texlive-luatex \
texlive-pictures \
texlive-pstricks \
texlive-science
RUN apt-get install -yq \
gnuplot \
ghostscript imagemagick \
vim
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
ADD fixpolicy.sh /
RUN /fixpolicy.sh && rm /fixpolicy.sh

USER ${USERNAME}

RUN pip install --upgrade pip && pip install \
uncertainties iminuit sympy gpy gpyopt scikit-optimize

RUN conda update -n base conda && \
conda install -c conda-forge jupyter_nbextensions_configurator && \
conda install -c conda-forge jupyter_contrib_nbextensions
RUN jupyter nbextension enable spellchecker/main

RUN mkdir -p $HOME/scripts
COPY --chown=jovyan:users scripts/* ${HOME}/scripts/
ENV PATH="$HOME/scripts:$PATH" \
PYTHONPATH="$HOME/scripts:$PYTHONPATH" \
TEXINPUTS="$HOME/scripts:$TEXINPUTS"

WORKDIR ${HOME}/work/
