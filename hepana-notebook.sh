#!/bin/bash

if [ $# -eq 1 ]; then
    port=$1
else
    port=8888
fi
echo "Starting notebook at 'localhost:$port' ..."

docker run --rm -it -p $port:8888 -v "$PWD":/home/jovyan/work avitase/hepana-notebook:latest
