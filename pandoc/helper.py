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
from sty import ef, fg, rs

script_dir_ = os.path.dirname( os.path.realpath( __file__ ) )

# Third party filters_ I use.
filters_ = [ 'pandoc-citeproc', 'pandoc-crossref', 'pandoc-imagine', 'gandu' ]

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
        print( "[ERROR] Could not find pandoc." )
        quit( -1 )
    return path

def run( cmd ):
    print( ef.bold + "[INFO ] Excuting " + fg.blue + "%s" % cmd  
            + fg.rs + rs.bold )
    cmd = cmd.split( )
    cmd = [ x for x in cmd if x.strip() ]
    res = subprocess.run( cmd, shell =False, check = True )
    if res.returncode != 0:
        print( "[WARN ] Failuer. %s" % res.stderr )
    return res

