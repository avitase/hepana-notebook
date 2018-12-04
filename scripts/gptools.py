import os

size_small = (2.8, 2.1)
size_medium = (4.0, 3.0)

preamble = [
    r'''\usepackage{ifthen}''',
    r'''\newboolean{uprightparticles}''',
    r'''\setboolean{uprightparticles}{false}''',
]
with open(os.path.expanduser('~') + '/scripts/lhcb-symbols-def.tex', 'r') as f:
    lines = [line.strip() for line in f.readlines()]
    non_empty_or_comment = lambda x: len(x) > 0 and not x.startswith('%')
    preamble += [line for line in lines if non_empty_or_comment(line)]

    def remove_in_line_comments(x):
        pos = x.find('%')
        if pos < 0 or pos+1 == len(x) or (pos > 0 and x[pos-1] == '\\'):
            return x
        else:
            return x[:pos]
    preamble = [remove_in_line_comments(line) for line in preamble]
    preamble = [line.replace('\\', '\\\\') for line in preamble]
    preamble = [line.replace('\"', '\\\"') for line in preamble]
    preamble = [line.replace('\'', '\\\'') for line in preamble]

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
        f.write('set terminal epslatex size {}, {} {} standalone "" 9 header \\\n'.format(*size, color_type))
        f.write('"{}"\n'.format('\\n'.join(preamble)))

        f.write('set output \'{}\'\n'.format(texfile_name))
        f.write('load \'/home/jovyan/scripts/parula.pal\'\n')
        f.write('set datafile separator \',\'\n\n')
        if lumi_and_sqrts_line:
            f.write('set label \'\\footnotesize{{{}}}\' right at graph 1.,{}\n\n'.format(lumi_and_sqrts_line, sqrts_ypos_on_graph))

        macros = '/home/jovyan/scripts'
        f.write('set macros\nset loadpath \'{}\'\n\n'.format(macros))

        f.write(code.strip())

    return 'gp2png.sh {} {} {}'.format(gpfile_name, texfile_name, color_type)
