#!/bin/bash -
#===============================================================================
#
#          FILE: pandoc_find_filters.sh
#
#         USAGE: ./pandoc_find_filters.sh
#
#   DESCRIPTION: 
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Dilawar Singh (), dilawars@ncbs.res.in
#  ORGANIZATION: NCBS Bangalore
#       CREATED: 03/30/2018 06:25:32 PM
#      REVISION:  ---
#===============================================================================

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Order of filters are important.

PANDOC_FILTERS=''
for FILTER in pantable pandoc-imagine pandoc-crossref pandoc-citeproc; do
    if [ -x "$(command -v $FILTER)" ]; then
        PANDOC_FILTERS="$PANDOC_FILTERS -F $(which $FILTER)"
    fi
done

PANDOC_FILTERS="$PANDOC_FILTERS -F $SCRIPT_DIR/pandoc/dilawar.py "
echo $PANDOC_FILTERS
