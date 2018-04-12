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
EXT=${2:-docx}

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PANDOC_FILTERS="$($SCRIPT_DIR/./pandoc_find_filters.sh)"
cat $TEXFILE | $SCRIPT_DIR/preprocess_of_docx.py | \
    pandoc -f latex $PANDOC_FILTERS -o $TEXFILE.$EXT
