#!/usr/bin/env python3

"""
Pandoc filter to process raw latex tikz environments into images.
Assumes that pdflatex is in the path, and that the standalone
package is available.  Also assumes that ImageMagick's convert
is in the path. Images are put in the tikz-images directory.

CREDIT: Did I write this? Or downloaded it from somewhere? Oh the mystery.
"""

import os
import re
import shutil
import sys
import functools
import subprocess
import hashlib
import requests
import mimetypes
import glob

from pandocfilters import toJSONFilters, Para, Image, get_filename4code, get_extension
from tempfile import mkdtemp

script_dir = os.path.dirname( __file__ )
sys.path.append( script_dir )
import theorem
import code_blocks

incomment = False

def log( *msg ):
    print( *msg, file = sys.stderr )

def get_filename( text ):
    m = hashlib.sha256( text.encode() ).hexdigest( )
    return '%s' % m


def download_image_from_url( url ):
    basename = get_filename4code( '_downloaded_from_url', url, '' )
    log( 'basename', basename )
    if os.path.isdir( basename ):
        # Return first file from this directory
        return  glob.glob( '%s/*' % basename )[0]
    try:
        r = requests.get( url, stream = True, timeout = 4)
    except Exception as e:
        return url

    ext = mimetypes.guess_extension( r.headers['content-type'] ) or url.split('.')[-1]
    if '.jpe' in ext:
        ext = '.jpg'

    os.makedirs( basename )
    filename = os.path.join( basename, 'downloaded_img' + ext )
    if not os.path.exists( filename ):
        with open( filename, 'wb' ) as f:
            f.write( r.content )
    return filename

def tikz2image(tikz_src, filetype, outfile):
    tmpdir = mkdtemp()
    olddir = os.getcwd()
    os.chdir(tmpdir)

    # remove math \[ and ]/ from tikz_src 
    tikz_src = tikz_src.strip()
    tikz_src = tikz_src.rstrip( r'\]' )
    tikz_src = tikz_src.lstrip( r'\[' )
    tikz_src += "\% auto generated using filter \n"

    basename = get_filename4code("tikz", tikz_src)
    texfile = os.path.join( tmpdir, basename + '.tex' )
    pdffile = os.path.join( tmpdir, basename + '.pdf' )

    pre, post, text = [], [], []
    if r'\documentclass' not in tikz_src:
        pre = [ "\\RequirePackage{luatex85,shellesc}"
                , "\\documentclass[trim,multi=false,tikz]{standalone}"
                , "\\usepackage[sfdefault]{FiraSans}"
                , "\\usepackage[small,euler-digits]{eulervm}"
                , "\\usepackage{pgfplots}"
                , "\\pgfplotslibrary[]{units,groupplots}"
                , "\\begin{document}" ] 
        post = [ "\\end{document}" ]

    with open( texfile, 'w') as f:
        log( 'Writing', tikz_src )
        f.write( '\n'.join( pre + [ tikz_src ] + post ) )

    helper.run( 'latexmk -pdf -lualatex --shell-escape %s' % texfile )
    os.chdir(olddir)
    if filetype == 'pdf':
        shutil.copyfile(pdffile, os.path.join(olddir, basename + '.pdf'))
    else:
        subprocess.call(["convert", pdffile, os.path.join(olddir, basename+'.png')])
    shutil.rmtree(tmpdir)

def tikz_code_to_image( code, format ):
    if not os.path.isfile(src):
        try:
            tikz2image(code, filetype )
        except Exception as e:
            log( "Failed to create image", e )
            return 'FAILED'

def tikz(key, value, format, _):
    if key == 'RawBlock':
        [fmt, code] = value
        if fmt == "latex" and re.match( r'\begin{tikzpicture}', code):
            path = tikz_code_to_image( code, format )
            return Para([Image(['', [], []], [], [path, ""])])

def comment(k, v, fmt, meta):
    global incomment
    if k == 'RawBlock':
        fmt, s = v
        if fmt == "html":
            if re.search("<!-- BEGIN COMMENT -->", s):
                incomment = True
                return []
            elif re.search("<!-- END COMMENT -->", s):
                incomment = False
                return []
    if incomment:
        return []  # suppress anything in a comment

def image_with_url( k, v, fmt, meta ):
    if k == 'Image':
        urlOrPath = v[2][0]
        if 'http' in urlOrPath:
            url = urlOrPath
            path = download_image_from_url( url )
            log( "[INFO ] Replacing url %s with downloaded file %s" % (url, path) )
            v[2][0] = path
            return Image( *v )

def image_with_standalone( k, v, fmt, meta ):
    if k == 'Image':
        desc = v[2][0]
        if r'\documentclass' in desc:
            code = desc
            outfile = get_filename4code("tikz", code)
            filetype = get_extension(format, "png", html="png", latex="pdf")
            src = outfile + '.' + filetype
            if not os.path.isfile(src):
                tikz2image(code, filetype, outfile)
            return Para([Image(['', [], []], [], [src, ""])])

if __name__ == "__main__":
    toJSONFilters( 
        [ 
            image_with_url, image_with_standalone
            , comment, theorem.theorems
            , code_blocks.codeblocks 
            # This one is fragile.
            #  , table.do_filter
        ]
    ) 
