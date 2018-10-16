#!/bin/bash

docker run --rm -it -p 8888:8888 -v "$PWD":/home/jovyan/work avitase/hepana-notebook:latest
