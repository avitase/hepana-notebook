set terminal epslatex size 2.8, 2.1 monochrome standalone "" 9 header '\newcommand{\mevcc}{\ensuremath{\mathrm{Me\kern -0.1em V\!/}c^2}} \newcommand{\mevc}{\ensuremath{\mathrm{Me\kern -0.1em V\!/}c}} \newcommand{\gevcc}{\ensuremath{\mathrm{Ge\kern -0.1em V\!/}c^2}} \newcommand{\gevc}{\ensuremath{\mathrm{Ge\kern -0.1em V\!/}c}} \newcommand{\MagUp}{\ensuremath{\mathrm{\textit{Mag\kern -0.05em Up}}}} \newcommand{\MagDown}{\ensuremath{\mathrm{\textit{MagDown}}}} \newcommand{\tev}{\ensuremath{\mathrm{Te\kern -0.1em V}}} \newcommand{\invfb}{\ensuremath{\mathrm{fb}^{-1}}} \newcommand{\Lb}{\ensuremath{\Lambda_b^0}} \newcommand{\Lz}{\ensuremath{\Lambda}} \newcommand{\Dz}{\ensuremath{D^0}} \newcommand{\Ks}{\ensuremath{K_s}} \newcommand{\jpsi}{\ensuremath{J\mskip -3mu/\mskip -2mu\psi\mskip 2mu}}'
set output 'cos.tex'
load '/home/jovyan/scripts/parula.pal'
set datafile separator ','

set macros
set loadpath '/home/jovyan/scripts'

set title 'The Infamous $\cos x$ Function'
set samples 200
set xrange [0:4*pi]
set xtics pi
set mxtics 2
set format x '%.0P$\pi$'
set ytics .5
set grid
plot cos(x) lw 2 notitle