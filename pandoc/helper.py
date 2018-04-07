"""filters.py: 

Find all available filters.

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2017-, Dilawar Singh"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import sys
import os
import shutil
import subprocess
import re

script_dir_ = os.path.dirname( os.path.realpath( __file__ ) )

# Third party filters_ I use.
# citeproc must come after crossref.
filters_ = [ 
        'pandoc-crossref', 'pandoc-citeproc'
        , 'pandoc-imagine', 'pantable'
    ]

def path_of_filters( filters = filters_ ):
    paths = [ shutil.which( f ) for f in filters ]
    return [ p for p in paths if p is not None ]


def generic_filters( filters = None ):
    if not filters:
        filters = filters_
    flts = path_of_filters ( filters )
    flts.append( os.path.join( script_dir_, 'dilawar.py' ) )
    return flts

def pandoc_cmd( ):
    path = shutil.which( 'pandoc' )
    if path is None:
        log( "`red Could not find pandoc.`", 'ERROR' )
        quit( -1 )
    return path

def run( cmd ):
    log( "Executing `blue %s`" % cmd )
    cmd = cmd.split( )
    cmd = [ x for x in cmd if x.strip() ]
    res = subprocess.run(cmd, shell=False
            , stderr=subprocess.PIPE 
            , universal_newlines = True
            )
    if res.returncode != 0:
        log( '⚠ Previous command may have failed.' )
    return res

def default_tex_template( ):
    return os.path.join( script_dir_, 'templates', 'default.latex' )

def log( msg, level = 'INFO' ):
    try:
        from sty import ef, fg, rs
        boldPat = re.compile( r'(\*\*)(?P<text>.+?)(\*\*)', re.DOTALL )
        itPat = re.compile( r'(\*)(?P<text>.+?)(\*)', re.DOTALL )
        colorPat = re.compile( r'`(?P<color>\w+)\s+(?P<text>.+?)\`', re.DOTALL )

        # bold 
        for m in boldPat.finditer( msg ):
            msg = msg.replace( m.group(0), ef.b + m.group('text') + rs.b )

        # italics
        for m in itPat.finditer( msg ):
            msg = msg.replace( m.group(0), ef.i + m.group('text') + rs.i )

        # Insert colors.
        for m in colorPat.finditer( msg ):
            c, t = m.group('color'), m.group( 'text' )
            msg = msg.replace( m.group(0), '%s%s' % (getattr(fg,c), t) + fg.rs )

    except ImportError as e:
        print( e, file = sys.stderr )

    print( '[%3s] %s' % (level, msg ) )

def test( ):
    log( '`blue *Hellow* kitty`. `red how are you __today__`. I am _fine_.' )

if __name__ == '__main__':
    test()
