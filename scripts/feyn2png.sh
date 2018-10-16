#!/bin/bash

if [ $# -eq 0 ]; then
    echo Usage $0 [file.tex]
    exit 1
fi

textemp=$1
texfile=${1%.*}-tmp.tex

if [ ! -f $textemp ]; then
    echo Error: File \'$textemp\' not found!
    exit 1
fi

cp $HOME/scripts/feynhead.tex $texfile
cat $textemp >> $texfile
echo "\\end{fmffile}" >> $texfile
echo "\\end{document}" >> $texfile

latex -interaction=nonstopmode $texfile
if [ $? -ne 0 ]; then
    rm -f ${texfile%.*}.{aux,dvi,log,pdf} $texfile
    exit 1
fi

mps=`ls *.mp`
for f in $mps; do mpost $f; done
pdflatex -interaction=nonstopmode $texfile

if [ $? -ne 0 ]; then
    exit 1
fi

convert -monochrome -density 600 -units -trim PixelsPerInch ${texfile%.*}.pdf ${textemp%.*}.png

rm -f ${texfile%.*}.{aux,dvi,log,pdf} $texfile
for f in $mps; do rm -f ${f%.*}.{1,t1,log,mp}; done

mkdir -p img
mv ${textemp%.*}.png img/
