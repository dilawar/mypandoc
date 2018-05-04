#!/usr/bin/env python3
"""expand_file_name.py: 

Expand filepath in given file. Write new text to stdout.

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

def main( filename ):
    filedir = os.path.dirname( os.path.realpath(filename) )
    with open( filename, 'r' ) as f:
        text = f.read( )
    text = replace_in_text( text )
    print(text, file = sys.stdout)

def replace_in_text( text ):
    for m in re.finditer( r'\.?\/(\S+?\.\w+)', text ):
        path = os.path.join( filedir, m.group(1) )
        # replace it with absolute path.
        if os.path.isfile( path ):
            text = text.replace( m.group(0), path )
    return text

if __name__ == '__main__':
    main( sys.argv[1] )
