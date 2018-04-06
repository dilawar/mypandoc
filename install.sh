#!/bin/bash -
#===============================================================================
#
#          FILE: install.sh
#
#         USAGE: ./install.sh
#
#   DESCRIPTION: 
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Dilawar Singh (), dilawars@ncbs.res.in
#  ORGANIZATION: NCBS Bangalore
#       CREATED: Friday 06 April 2018 10:02:35  IST
#      REVISION:  ---
#===============================================================================

set -o nounset                                  # Treat unset variables as an error

# create symbolic links to $HOME/.local/bin
echo "Installing dependencies"
pip install -r ./requirements.txt --user

echo "Creating links to $HOME/.local/bin"
ln -s pandoc2* $HOME/.local/bin

