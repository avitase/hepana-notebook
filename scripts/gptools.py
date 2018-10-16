import os

size_small = (2.8, 2.1)
size_medium = (4.0, 3.0)

preamble = [
    r'''\newcommand{\mevcc}{\ensuremath{\mathrm{Me\kern -0.1em V\!/}c^2}}''',
    r'''\newcommand{\mevc}{\ensuremath{\mathrm{Me\kern -0.1em V\!/}c}}''',
    r'''\newcommand{\gevcc}{\ensuremath{\mathrm{Ge\kern -0.1em V\!/}c^2}}''',
    r'''\newcommand{\gevc}{\ensuremath{\mathrm{Ge\kern -0.1em V\!/}c}}''',
    r'''\newcommand{\MagUp}{\ensuremath{\mathrm{\textit{Mag\kern -0.05em Up}}}}''',
    r'''\newcommand{\MagDown}{\ensuremath{\mathrm{\textit{MagDown}}}}''',
    r'''\newcommand{\tev}{\ensuremath{\mathrm{Te\kern -0.1em V}}}''',
    r'''\newcommand{\invfb}{\ensuremath{\mathrm{fb}^{-1}}}''',
    r'''\newcommand{\Lb}{\ensuremath{\Lambda_b^0}}''',
    r'''\newcommand{\Lz}{\ensuremath{\Lambda}}''',
    r'''\newcommand{\Dz}{\ensuremath{D^0}}''',
    r'''\newcommand{\Ks}{\ensuremath{K_s}}''',
    r'''\newcommand{\jpsi}{\ensuremath{J\mskip -3mu/\mskip -2mu\psi\mskip 2mu}}''',
]

def prepend_preamble(cmd):
    return [cmd, ] + preamble

def append_preamble(cmd):
    return preamble + [cmd, ]

def create(file_name,
           code,
           size=size_small,
           preamble=preamble,
           monochrome=True,
           lumi='',
           sqrts='',
           data_type='',
           sqrts_ypos_on_graph=None):

    basename = file_name.split('.')[0]
    gpfile_name = '{}.{}'.format(basename, 'gp')
    texfile_name = '{}.{}'.format(basename, 'tex')

    if lumi: lumi = r'${}\,\invfb$'.format(lumi)
    if sqrts: sqrts = r'(${}\,\tev$)'.format(sqrts)
    lumi_and_sqrts_line = r'{} {} {}'.format(data_type, lumi, sqrts).strip()

    if not sqrts_ypos_on_graph:
        if size == size_medium:
            sqrts_ypos_on_graph = 1.025
        else:
            sqrts_ypos_on_graph = 1.04

    with open(os.path.join('img', gpfile_name), 'w') as f:
        color_type = 'monochrome' if monochrome else 'color'
        f.write('set terminal epslatex size {}, {} {} standalone "" 9 header \'{}\'\n'
                .format(*size, color_type, ' '.join(preamble)))

        f.write('set output \'{}\'\n'.format(texfile_name))
        f.write('load \'/home/jovyan/scripts/parula.pal\'\n')
        f.write('set datafile separator \',\'\n\n')
        if lumi_and_sqrts_line:
            f.write('set label \'\\footnotesize{{{}}}\' right at graph 1.,{}\n\n'.format(lumi_and_sqrts_line, sqrts_ypos_on_graph))

        macros = '/home/jovyan/scripts'
        f.write('set macros\nset loadpath \'{}\'\n\n'.format(macros))

        f.write(code.strip())

    return 'gp2png.sh {} {} {}'.format(gpfile_name, texfile_name, color_type)
