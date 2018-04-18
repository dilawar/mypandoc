#!/usr/bin/env bash
#===============================================================================
#   DESCRIPTION: Generate DOCX from pandoc.
#        AUTHOR: Dilawar Singh (), dilawars@ncbs.res.in
#  ORGANIZATION: NCBS Bangalore
#       CREATED: Monday 26 February 2018 05:46:00  IST
#      REVISION:  ---
#===============================================================================

set -e
set -o nounset                                  # Treat unset variables as an error

TEXFILE="$1"
EXT=${2:-odt}

echo "Converting $EXT from $TEXFILE"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PANDOC_FILTERS="$($SCRIPT_DIR/./pandoc_find_filters.sh)"
cat $TEXFILE | $SCRIPT_DIR/pandoc_preprocess_doc_html.py | \
    pandoc -f latex -t $EXT $PANDOC_FILTERS -o $TEXFILE.$EXT
