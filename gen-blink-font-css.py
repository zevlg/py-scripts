#!/usr/bin/env python3
#
# Generates font CSS file for use by Blink
# (https://github.com/blinksh/blink)
#
import os
import sys
import base64

__version__ = '0.3'


def usage():
    print('Version: %s' % __version__)
    print('usage: %s <FONT_NAME> [<STYLE>:<WEIGHT>:<FILENAME>]*' % sys.argv[0])
    print('Example: %s "Ricty Diminished L" '
          'normal:normal:RictyDiminishedL-Regular.ttf '
          'normal:bold:RictyDiminishedL-Bold.ttf '
          'italic:normal:RictyDiminishedL-Oblique.ttf '
          'italic:bold:RictyDiminishedL-BoldOblique.ttf' % sys.argv[0])
    sys.exit(0)


def font_desc(spec):
    style, weight, fname = spec.split(':')
    with open(fname, 'rb') as f:
        return style, weight, fname, base64.b64encode(f.read())

def data_desc(fname):
    DATA_DESCS = {'.ttf': 'truetype', '.otf': 'opentype'}
    _, ext = os.path.splitext(fname)
    try:
        return DATA_DESCS[ext]
    except KeyError:
        print('Unsupported extension "%s", only %s are supported' % (
              ext, ', '.join(DATA_DESCS.keys())), file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()

    for style, weight, fname, b64font in map(font_desc, sys.argv[2:]):
        print('@font-face {',
              'font-family: "%s";' % sys.argv[1],
              'font-style: %s;' % style,
              'font-weight: %s;' % weight, sep='\n')
        print('src: url(data:font/%s;charset-utf-8;base64,' % data_desc(fname),
              b64font.decode(), ');\n}', sep='')
