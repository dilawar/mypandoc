#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Convert pandoc source code to PDF file.
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import re
from pandoc import helper
import subprocess

script_dir = os.path.dirname( os.path.realpath( __file__ ) )

def main( args, extra ):
    args.output = args.output or '%s.pdf' % args.input
    texfile = args.output.rstrip( '.pdf'  ) +  '.tex'
    filters = [ ' -F %s' % f for f in helper.generic_filters( ) ]

    base = '%s %s' % ( helper.pandoc_cmd(), ''.join(filters) )
    #  base += ' --pdf-engine lualatex --pdf-engine-opt=-shell-escape'
    base += ' --template %s ' % helper.default_tex_template( )

    if args.verbose:
        base += ' --verbose '

    base += ' %s' % ' '.join( extra )

    if args.tex:
        helper.log( "Generating TeX for our review." )
        res = helper.run( '%s -o %s %s ' % (base, texfile, args.input) )

    # Generate pdf.
    res = helper.run( '%s -o %s %s ' % (base, args.output, args.input) )

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''pandoc to pdf.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--input', '-i'
        , required = True
        , help = 'Input file (pandoc)'
        )
    parser.add_argument('--output', '-o'
        , required = False
        , help = 'Output file'
        )
    parser.add_argument('--verbose', '-v'
        , required = False, default = False, action = 'store_true'
        , help = 'Enable verbose mode.'
        )
    parser.add_argument('--tex', '-t'
        , required = False, default = False, action = 'store_true'
        , help = 'Genarte TeX also.'
        )
    args, extra = parser.parse_known_args( )
    main( args, extra )

