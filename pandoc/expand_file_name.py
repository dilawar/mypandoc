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

def main( filename, outfile = None ):
    filedir = os.path.dirname( os.path.realpath(filename) )
    with open( filename, 'r' ) as f:
        text = f.read( )
    text = expand_in_text( text, filedir )

    if outfile is not None:
        with open(outfile, 'w') as f:
            f.write(text)
    return text

def expand_in_text( text, filedir ):
    dir2search = [filedir, os.path.join(filedir, '..')]
    replaceDict = {}
    for m in re.finditer( r'\.?\/(\S+?\.\w+)', text ):
        # The file could be in same directory of one spep up.
        for dirname in dir2search:
            path = os.path.join( dirname, m.group(1) )
            # replace it with absolute path.
            if os.path.isfile( path ):
                replaceDict[m.span()] = path
                break
        else:
            # This file does not exists or most likely it is not a file in first
            # place.
            pass

    newText = [ ]
    end = 0
    for a, b in replaceDict:
        v = replaceDict[(a,b)]
        print('x',a, b, v)
        newText.append(text[end:a])
        newText.append(v)
        end = b
    newText.append( text[end:] )
    text = ''.join(newText)

    return text

if __name__ == '__main__':
    outfile = None
    if len(sys.argv) > 2:
        outfile = sys.argv[2]
    text = main(sys.argv[1], outfile)
    print(text)
