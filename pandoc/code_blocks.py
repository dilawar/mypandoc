#!/usr/bin/env python3

from __future__ import print_function

"""
Pandoc filter to process code blocks with class "graphviz", "chemfig",
"standalone" into pdf images.

Dependencies:
    - pygraphviz
    - lualatex
"""

import os
import sys
import re
import subprocess

from pandocfilters import toJSONFilter, Para
from pandocfilters import Image, get_filename4code, get_caption, get_extension
from pandocfilters import RawBlock

# expand filename to absolute.
import expand_file_name


def latex( x ):
    return RawBlock( 'latex',  x)

def print1( *msg ):
    print( '\n'.join(msg), file=sys.stderr )

def replace_ext( filename, newext = 'tex' ):
    oldExt = filename.split( '.' )[-1]
    return re.sub( r'(.+?)\.%s$' % oldExt, '\1\.%s' % newext )

def gen_standalone( code, dest ):
    # prepare variables.
    dest = os.path.realpath( dest )
    ext = dest.split( '.' )[-1]
    dirname = os.path.dirname( dest )
    basename = os.path.basename( dest )
    nameWE = '.'.join( basename.split( '.' )[:-1] )
    texFile = os.path.join( dirname, nameWE + '.tex' )

    tex = [ '\\RequirePackage{luatex85,shellesc}' ]
    tex += [ '\\documentclass[preview,multi=false,tikz]{standalone}' ]
    tex += [ '\\usepackage{amsmath,amssymb,siunitx}' ]
    tex += [ '\\usepackage[sfdefault]{FiraSans}' ]
    tex += [ '\\usepackage[small,euler-digits]{eulervm}' ]
    tex += [ '\\usepackage{chemfig}' ]
    tex += [ '\\usetikzlibrary{shapes,arrows,arrows.meta,positioning,calc}' ]
    tex += [ '\\usepackage{pgfplots}' ]
    tex += [ '\\usepackage{pgfplotstable}' ]
    tex += [ '\\usepgfplotslibrary{units}' ]
    if r'\begin{document}' not in code:
        tex += [ '\\begin{document}' ]
    tex += [ code ]
    if r'\end{document}' not in code:
        tex += [ '\\end{document}']


    # Write file
    texText =  expand_file_name.replace_in_text( '\n'.join( tex ) )
    with open( texFile, 'w' ) as f:
        f.write( texText )
    print1('[INFO] Wrote standalone file: %s' % texFile)
    res1 = subprocess.check_output( 
            [ 'lualatex', '-shell-escape', texFile ]
            , shell=False, stderr = subprocess.STDOUT 
            , cwd = dirname
            )

    if ext != 'pdf':
        pdfFile = os.path.join( dirname, nameWE + '.pdf' )
        outfile = os.path.join( dirname, nameWE + '.%s' % ext )
        print1( pdfFile, outfile )
        opts = '-density 300 -antialias -quality 100'. split( )
        res = subprocess.check_output( 
                [ 'convert', pdfFile ] + opts + [ outfile ]
                , shell=False
                , stderr = subprocess.STDOUT
                , cwd = dirname
                )

    assert os.path.isfile( dest ), "%s could not be generated." % dest
    

def codeblocks(key, value, format, _):
    if key == 'CodeBlock':
        return process( value, format )

def process( value, format ):
    [[ident, classes, keyvals], code] = value
    if "graphviz" in classes:
        caption, typef, keyvals = get_caption(keyvals)
        filetype = get_extension(format, "png")
        dest = get_filename4code("graphviz", code, filetype)
        if not os.path.isfile(dest):
            import pygraphviz
            g = pygraphviz.AGraph(string=code)
            g.layout()
            g.draw(dest)
            sys.stderr.write('Created image ' + dest + '\n')

        return Para([Image([ident, [], keyvals], caption, [dest, typef])])

    elif "standalone" in classes:
        caption, typef, keyvals = get_caption(keyvals)
        filetype = get_extension(format, "png", html="png", latex="pdf")
        dest = get_filename4code("standalone", code, filetype)
        if not os.path.isfile(dest):
            gen_standalone(code, dest)
        else:
            print1('[INFO] Image file %s already generated' % dest )
        return Para([Image([ident, [], keyvals], caption, [dest, typef])])

if __name__ == "__main__":
    toJSONFilter( codeblocks )
