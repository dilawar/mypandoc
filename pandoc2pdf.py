#!/usr/bin/env python3
"""pandoc2pdf.py: 

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import re
from pandoc import filters
import subprocess

def main( args ):
    pandocSrc = args.input
    pdf = args.output
    myf = filters.generic_filters( )
    print( myf )
    

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''pandoc2pdf.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--input', '-i'
        , required = True
        , help = 'Input file (pandoc)'
        )
    parser.add_argument('--output', '-o'
        , required = False
        , help = 'Output file'
        )
    parser.add_argument( '--debug', '-d'
        , required = False
        , default = 0
        , type = int
        , help = 'Enable debug mode. Default 0, debug level'
        )
    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)
    main( args )

